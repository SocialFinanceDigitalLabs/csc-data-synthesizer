import random
import numpy as np
import string
import itertools
import datetime
from typing import Optional, List, Dict, Tuple
from scipy.stats import nbinom
from copy import deepcopy
from .types import Probabilities, Episode

def generate_child_id() -> int:
    seen_child_ids = set()
    while True:
        child_id = random.randint(0, 1_000_000)
        if child_id not in seen_child_ids:
            seen_child_ids.add(child_id)
            yield child_id

def generate_upn() -> str:
    seen_upns = set()
    while True:
        first_letter = random.choice(string.ascii_uppercase)
        rest_of_upn = str(random.randint(1, int(1e11))).zfill(12)
        upn = first_letter + rest_of_upn

        if upn not in seen_upns:
            seen_upns.add(upn)
            yield upn

def generate_dob(current_date: datetime.datetime, age_start: int = 1, age_end: int = 14) -> datetime.datetime:
    age_at_start_in_days = random.randint(365 * age_start, 365 * age_end)
    return current_date - datetime.timedelta(days=age_at_start_in_days)

def generate_ethnicity() -> str:
    # TODO: Maybe weight this?
    return random.choice([
        'WBRI', 'WIRI', 'WOTH', 'WIRT', 'WROM', 'MWBC', 'MWBA', 'MWAS', 'MOTH', 'AIND', 'APKN', 
        'ABAN', 'AOTH', 'BCRB', 'BAFR', 'BOTH', 'CHNE', 'OOTH', 'REFU', 'NOBT'
    ])

def generate_motherhood_date(prob_is_mother: float, sex: int, dob: datetime.datetime) -> Optional[datetime.datetime]:
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
    is_uasc = random.random() < prob_is_uasc
    date_uasc_ceased = None
    if is_uasc:
        date_uasc_ceased = dob + datetime.timedelta(days=18 * 365)
        # TODO: Find cases where this should be less than 18 - when checked all values are set to 18th birthday

    return date_uasc_ceased

def generate_episodes(start_date, dob, probabilities: Probabilities) -> List[Episode]:
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
                list(probabilities.reason_for_care.keys()), 
                weights=list(probabilities.reason_for_care.values())
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
    # TODO: These should probably not be picked randomly
    return random.choice(['C1', 'C2', 'D1', 'E1', 'V2', 'V3', 'V4', 'L1', 'L2', 'L3', 'J1', 'J2', 'J3'])

def _generate_reason_end() -> str:
    """
    Picks a reason for an episode to end - this can be any from the codeset except X1
    """
    # TODO: These should probably not be picked randomly
    return random.choice([
        'E11', 'E12', 'E2', 'E3', 'E4A', 'E4B', 'E13', 'E41', 'E45', 'E46', 'E47', 'E48', 'E5',
        'E6', 'E7', 'E9', 'E14', 'E15', 'E16', 'E17', 'E8'
    ])

def generate_reason_place_change() -> str:
    # TODO: These should probably not be picked randomly
    return random.choice([
        'CARPL', 'CLOSE', 'ALLEG', 'STAND', 'APPRR', 'CREQB', 'CREQO', 'CHILD', 'LAREQ', 'PLACE', 'CUSTOD', 'OTHER'
    ])

def _generate_new_placement() -> Tuple[str, str, str, str, str]:
    # TODO: These should not be random
    placement_type = random.choice([
        'A3', 'A4', 'A5', 'A6', 'H5', 'K1', 'K2', 'P1', 'P2', 'P3', 'R1', 'R2', 'R3', 'R5',
        'S1', 'T0', 'T1', 'T2', 'T3', 'T4', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'Z1'
    ])

    # TODO: This should depend on placement type
    placement_code = random.choice([f'PR{i}' for i in range(6)])

    home_postcode = _generate_postcode()
    place_postcode = _generate_postcode()
    urn = random.randint(1000000, 9999999)
    
    return placement_type, placement_code, home_postcode, place_postcode, urn

def _generate_postcode() -> str:
    #TODO: Actually generate valid postcodes

    first_letter = random.choice(string.ascii_uppercase)
    numbers = random.randint(1, 30)
    last_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))

    return first_letter + str(numbers) + ' ' + last_letters