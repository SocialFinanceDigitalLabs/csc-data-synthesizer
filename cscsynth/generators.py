import random
import numpy as np
import string
import itertools
import datetime
from typing import Optional, List, Dict, Tuple
from scipy.stats import nbinom
from copy import deepcopy
from .types import LeavingCareData, Probabilities, Episode, Review

def generate_child_id() -> int:
    """
    Generator for child IDs (an integer between 0 and 1 million).
    Uniqueness is guaranteed for the life of the generator.

    :returns: A new child id
    """
    seen_child_ids = set()
    while True:
        child_id = random.randint(0, 1_000_000)
        if child_id not in seen_child_ids:
            seen_child_ids.add(child_id)
            yield child_id

def generate_upn() -> str:
    """
    Generator for UPNs. Generates a 13 character UPN with the first character being A-Z, and the
    remaining 12 being digits.
    Uniqueness is guaranteed for the life of the generator.

    :returns: A new unique UPN.
    """
    seen_upns = set()
    while True:
        first_letter = random.choice(string.ascii_uppercase)
        rest_of_upn = str(random.randint(1, int(1e11))).zfill(12)
        upn = first_letter + rest_of_upn

        if upn not in seen_upns:
            seen_upns.add(upn)
            yield upn

def generate_dob(reference_date: datetime.datetime, age_start: int = 1, age_end: int = 14) -> datetime.datetime:
    """
    Given a reference date, this will generate a date of birth such that the age is between age_start and age_end.
    The age is sampled uniformly from the range.

    :param reference_date: Date at which age_start, age_end applies.
    :param age_start: Minimal age at reference_date
    :param age_end: Maximal age at reference_date
    :returns: Generated date of birth.
    """
    age_at_start_in_days = random.randint(365 * age_start, 365 * age_end)
    return reference_date - datetime.timedelta(days=age_at_start_in_days)

def generate_ethnicity() -> str:
    """
    Randomly samples ethnicity from the list of all available ethnicity codes.

    :returns: Ethnicity string.
    """
    return random.choice([
        'WBRI', 'WIRI', 'WOTH', 'WIRT', 'WROM', 'MWBC', 'MWBA', 'MWAS', 'MOTH', 'AIND', 'APKN', 
        'ABAN', 'AOTH', 'BCRB', 'BAFR', 'BOTH', 'CHNE', 'OOTH', 'REFU', 'NOBT'
    ])

def generate_motherhood_date(prob_is_mother: float, sex: int, dob: datetime.datetime) -> Optional[datetime.datetime]:
    """
    This generates a possible motherhood date for a child with given sex and date of birth. 
    The child can be born between age 12 and age 18, and only to female (code = 2) children.
    The given probability is the probability conditioned on being female. The date is then sampled uniformly between 12 and 18.
    A value of None represents no motherhood date.

    :param prob_is_mother: Probability that a female child will become a mother at any point.
    :param sex: Sex code for child (1 = Male, 2 = Female)
    :param dob: Date of birth for child
    :returns: None if no birth, or the date of birth of the new child if this child is a mother.
    """
    mother_child_dob = None
    if sex == 2:
        is_mother = random.random() < prob_is_mother
        if is_mother:
            # A child is born somewhere between the 12th and 18th birthday
            earliest_birth_date = dob + datetime.timedelta(days=12 * 365)
            latest_birth_date = dob + datetime.timedelta(days=18 * 365)

            days_after_start_born = random.randint(0, (latest_birth_date - earliest_birth_date).days)
            mother_child_dob = earliest_birth_date + datetime.timedelta(days=days_after_start_born)

    return mother_child_dob

def generate_uasc_ceased_date(prob_is_uasc: float, dob: datetime.datetime) -> Optional[datetime.datetime]:
    """
    Generates a UASC ceased date. All children who are UASC will have a date, so this function performs two tasks
    - Randomly checks if the child is UASC (using prob_is_uasc)
    - If they are, generates a ceased date. For now this is always set to their 18th birthday.

    :param prob_is_uasc: The probability that any child is UASC.
    :param dob: The date of birth of the child (used for determining the ceased date).
    :returns: None if not UASC, or the date ceased if they are.
    """
    is_uasc = random.random() < prob_is_uasc
    date_uasc_ceased = None
    if is_uasc:
        date_uasc_ceased = dob + datetime.timedelta(days=18 * 365)
        # TODO: Find cases where this should be less than 18 - when checked all values are set to 18th birthday

    return date_uasc_ceased

def generate_episodes(start_date, dob, probabilities: Probabilities) -> List[Episode]:
    """
    Generates a list of all episodes for a given start date, date of birth and set of probabilities for generation.
    These episodes are generated based on the probabilities. The following assumptions are made.
    - All children in data will have at least one LAC period (maybe comprising multiple episodes). Any further LAC periods are sampled from a Poisson distribution.
    - A child can only be LAC between the start date and it's 18th birthday.
    - The individual episode lengths are determined by the daily probability of an episode ending, and are independent.
    - We sample a wait between 0 and 200 days for both the first episode starting, and any subsequent episodes.
    - If the total time (all LAC periods + all waits) is larger than the time til 18, the lengths get ratio'd down to fit in the time.
    
    :param start_date: No episode will have a start date before this date
    :param dob: The date of birth of the child (used for determining the last episode date)
    :param probabilities: A Probabilities object, which is used for
        - average_extra_episode_rate (for determining the number of LAC periods)
        - daily_episode_ending (for determining the length of LAC periods)
        - Passed to generate_care_episode.
    """
    total_num_care_episodes = 1 + np.random.poisson(probabilities.average_extra_episode_rate)

    adult_day = dob + datetime.timedelta(days=18 * 365)
    days_in_which_can_be_lac = (adult_day - start_date).days
    episode_lengths = nbinom.rvs(n=1, p=probabilities.daily_episode_ending, size=total_num_care_episodes)

    # Allow up to 200 days between episodes
    days_before = [random.randint(0, 200) for _ in range(total_num_care_episodes)]

    # We may generate a longer period than there is days before the 18th birthday
    # If this happens, we can ratio down the sizes of each event
    total_period = sum(itertools.chain.from_iterable(zip(days_before, episode_lengths)))
    ratio = min([1, days_in_which_can_be_lac / total_period])
    days_before = [int(d * ratio) for d in days_before]
    episode_lengths = [int(d * ratio) for d in episode_lengths]

    # We can then figure out the start date for each and generate the episodes
    episode_starts = [start_date + datetime.timedelta(days=d + sum(episode_lengths[:i])) for i, d in enumerate(days_before)]

    all_episodes = []
    for episode_start, episode_length in zip(episode_starts, episode_lengths):
        episodes = generate_care_episode(episode_start, episode_length, probabilities)
        all_episodes.append(episodes)

    return list(itertools.chain.from_iterable(all_episodes))

def generate_care_episode(start_date: datetime.datetime, length_of_episode: int, probabilities: Probabilities):
    """
    Generates a specific set of care episodes that directly relate to the same period of care (but with different
    legal status or placements).
    These start at the start_date, run for the length_of_episode, and change randomly based on probabilities.daily_episode_changing.

    The first episode will always have reason for new episode as 'S' (Started). Then for each subsequent episode we
    - Copy details from the old episode.
    - Generate a reason for change.
    - If the reason includes legal status change, sample a new one.
    - If the reason includes placement change, sample a new one.
    - Set a reason_end on the last episode of 'X1' and generate a reason_for_change.
    
    :param start_date: The start date of the episode set
    :param length_of_episode: The overall length of the entire episode set
    :param probabilities: A Probabilities object, used for
        - reason_for_episode_change - A weighted dictionary of reasons for an episode changing, with probabilities.
    :returns: A list of episodes for this period of care.
    """

    place, place_provider, home_postcode, place_postcode, urn = _generate_new_placement()
    start_episode = Episode(
        start_date=start_date,
        end_date=None,
        reason_end=None,
        reason_for_new_episode='S',
        legal_status=_generate_legal_status(),
        cin=random.choice([f'N{i}' for i in range(1, 9)]),
        place=place,
        place_provider=place_provider,
        home_postcode=home_postcode,
        place_postcode=place_postcode,
        urn=urn,
    )

    episodes = [start_episode]
    for i in range(length_of_episode):
        if random.random() < probabilities.daily_episode_changing:
            current_date = start_date + datetime.timedelta(days=i)
            last_episode = episodes[-1]
            last_episode.end_date = current_date
            last_episode.reason_end = 'X1'  # The change of episode code

            new_reason = random.choices(
                list(probabilities.reason_for_episode_change.keys()), 
                weights=list(probabilities.reason_for_episode_change.values())
            )[0]
            
            next_episode = deepcopy(last_episode)
            next_episode.start_date = current_date
            next_episode.end_date = None
            next_episode.reason_for_new_episode = new_reason

            # Change of legal status
            if new_reason in ['L', 'B', 'U']:
                next_episode.legal_status = _generate_legal_status()

            # Change of placement
            if new_reason in ['P', 'T', 'B', 'U']:
                next_episode.place, next_episode.place_provider, next_episode.home_postcode, next_episode.place_postcode, next_episode.urn = _generate_new_placement()
                last_episode.reason_place_change = generate_reason_place_change()

            episodes.append(next_episode)


    episodes[-1].end_date = start_date + datetime.timedelta(days=length_of_episode)
    episodes[-1].reason_end = _generate_reason_end()

    return episodes

def _generate_legal_status() -> str:
    """
    Generates a random legal status from the codeset.

    :returns: Legal status string
    """
    return random.choice(['C1', 'C2', 'D1', 'E1', 'V2', 'V3', 'V4', 'L1', 'L2', 'L3', 'J1', 'J2', 'J3'])

def _generate_reason_end() -> str:
    """
    Picks a reason for an episode to end - this can be any from the codeset except X1

    :returns: Reason for ending string
    """
    return random.choice([
        'E11', 'E12', 'E2', 'E3', 'E4A', 'E4B', 'E13', 'E41', 'E45', 'E46', 'E47', 'E48', 'E5',
        'E6', 'E7', 'E9', 'E14', 'E15', 'E16', 'E17', 'E8'
    ])

def generate_reason_place_change() -> str:
    """
    Generates a random reason for placement change from the codeset.

    :returns: Placement change string
    """
    return random.choice([
        'CARPL', 'CLOSE', 'ALLEG', 'STAND', 'APPRR', 'CREQB', 'CREQO', 'CHILD', 'LAREQ', 'PLACE', 'CUSTOD', 'OTHER'
    ])

def _generate_new_placement() -> Tuple[str, str, str, str, str]:
    """
    Generates all the information for a new placement. Currently
    - Placement type is uniformly sampled from the codeset
    - Placement code is uniformly sampled from the codeset
    - Home and placement postcodes are randomly generated.
    - URN is a random 7-digit number.

    :returns: placement_type, placement_code, home_postcode, place_postcode, urn
    """
    placement_type = random.choice([
        'A3', 'A4', 'A5', 'A6', 'H5', 'K1', 'K2', 'P1', 'P2', 'P3', 'R1', 'R2', 'R3', 'R5',
        'S1', 'T0', 'T1', 'T2', 'T3', 'T4', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'Z1'
    ])

    placement_code = random.choice([f'PR{i}' for i in range(6)])

    home_postcode = _generate_postcode()
    place_postcode = _generate_postcode()
    urn = random.randint(1000000, 9999999)
    
    return placement_type, placement_code, home_postcode, place_postcode, urn

def _generate_postcode() -> str:
    """
    Generates a postcode string. This is not guaranteed to be valid currently, but will
    have the properties of
    - One letter
    - 1 or 2 numbers
    - A space
    - A number and 2 letters.
    
    :returns: Postcode string
    """

    first_letter = random.choice(string.ascii_uppercase)
    numbers = random.randint(1, 30)

    last_number = random.randint(1, 9)
    last_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))

    return first_letter + str(numbers) + ' ' + str(last_number) + last_letters


def generate_reviews(episodes: List[Episode], review_frequency: float) -> List[Review]:
    total_days_in_care = sum((e.end_date - e.start_date).days for e in episodes)

    # Must be at least one review if in care for 20 days or longer
    num_reviews = max([
        total_days_in_care > 20, 
        int(np.random.poisson(review_frequency * total_days_in_care)),
    ])

    review_days = [random.randint(0, total_days_in_care - 1) for _ in range(num_reviews)]

    # We then do a bit of work to get from the days view to the right dates that are inside episodes
    reviews = []
    current_days = 0
    for e in episodes:
        episode_length = (e.end_date - e.start_date).days
        for episode_day in range(episode_length):
            # Check if this is the day selected for review
            for review_day in review_days:
                if review_day == current_days:
                    reviews.append(Review(
                        review_date=e.start_date + datetime.timedelta(days=episode_day),
                        review_code=_generate_review_code(),
                    ))

            current_days += 1

    return reviews

def _generate_review_code() -> str:
    review_code = random.choice([f'PN{i}' for i in range(8)])

    return review_code

        
def generate_leaving_care() -> LeavingCareData:
    return LeavingCareData(
        in_touch=random.choice(['YES', 'NO', 'DIED', 'REFU', 'NREQ', 'RHOM']),
        activ=random.choice(['F1', 'P1', 'F2', 'P2', 'F3', 'P3', 'G4', 'G5', 'G6', '0']),
        accom=random.choice([code + suitability for code in 'BCDEGHKRSTUVWZYZ0' for suitability in '12'])
    )

