import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Episode:
    start_date: datetime.datetime
    end_date: datetime.datetime
    reason_for_new_episode: str
    legal_status: str
    cin: str
    place: str
    place_provider: str
    home_postcode: str
    place_postcode: str
    reason_end: str
    reason_place_change: Optional[str] = None
    urn: Optional[str] = None


@dataclass
class Missing:
    missing_type: str
    start_date: datetime.datetime
    end_date: datetime.datetime


@dataclass
class Review:
    review_code: str
    review_date: datetime.datetime

@dataclass
class LeavingCareData:
    accom: str
    in_touch: str
    activ: str

@dataclass
class AdoptionData:
    start_date: datetime.datetime
    end_date: datetime.datetime
    reason_ceased: str
    foster_care: str
    number_adopters: str
    sex_adopter: str
    ls_adopter: str

@dataclass
class Child:
    upn: str
    child_id: int
    sex: int
    ethnicity: str
    dob: datetime.datetime
    episodes: List[Episode]
    reviews: List[Review]
    leaving_care_data: Optional[LeavingCareData] = None
    mother_child_dob: Optional[datetime.datetime] = None
    previous_permanent: str = 'Z1'
    prev_permanent_date: Optional[datetime.datetime] = None
    missing_periods: Optional[List[Missing]] = None
    date_uasc_ceased: Optional[datetime.datetime] = None
    adoption_data: Optional[AdoptionData] = None

@dataclass
class Probabilities:
    """
    Probability set for generating the data.

    The default values are estimated (roughly) from real 903 data.

    :param is_uasc: The probability that any given child in care is UASC.
    :param is_mother: The probability that a female in care will be a mother at any point.
    :param daily_episode_ending: The daily probability of a LAC period ending.
    :param daily_episode_changing: The daily probability of a LAC period changing (placement/legal status/carer)
    :param extra_episode_rate: The average rate of extra periods of care (beyond 1), modelled as 1 + Poisson(rate)
    :param reason_for_episode_change: A dict with the episode change keys, and associated probability weights (sum to 1)
    :param review_frequency: The daily frequency of reviews
    """
    is_uasc: float = 0.05
    is_mother: float = 0.01
    is_adopted: float = 0.05
    daily_episode_ending: float = 1 / 1000  # Average care length is around 1000 days
    daily_episode_changing: float = 1 / 300   # Average episode length is around 300 days
    average_extra_episode_rate: float = 0.15  
    reason_for_episode_change: Dict[str, int] = field(default_factory=lambda: {
            'B': 0.02,
            'L': 0.27,
            'P': 0.605,
            'T': 0.1,
            'U': 0.005,
        })
    review_frequency: float = 1 / 365