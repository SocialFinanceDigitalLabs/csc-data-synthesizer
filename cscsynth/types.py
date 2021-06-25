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
    child_id: int
    missing_type: str
    start_date: datetime.datetime
    end_date: datetime.datetime


@dataclass
class Review:
    child_id: int
    review_code: str
    review_date: datetime.datetime


@dataclass
class Child:
    upn: str
    child_id: int
    sex: int
    ethnicity: str
    dob: datetime.datetime
    episodes: List[Episode]
    mother_child_dob: Optional[datetime.datetime] = None
    previous_permanent: str = 'Z1'
    prev_permanent_date: Optional[datetime.datetime] = None
    missing_periods: Optional[List[Missing]] = None
    date_uasc_ceased: Optional[datetime.datetime] = None

@dataclass
class Probabilities:
    """
    Probability set for generating the data.

    The default values are estimated (roughly) from real 903 data.
    """
    is_uasc: float = 0.05
    is_mother: float = 0.01
    daily_episode_ending: float = 1 / 1000  # Average care length is around 1000 days
    daily_episode_changing: float = 1 / 300   # Average episode length is around 300 days
    average_extra_episode_rate: float = 0.15  # Modelled as 1 + Poisson(rate)
    reason_for_care: Dict[str, int] = field(default_factory=lambda: {
            'B': 0.02,
            'L': 0.27,
            'P': 0.605,
            'T': 0.1,
            'U': 0.005,
        })