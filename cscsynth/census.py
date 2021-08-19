import datetime
from copy import deepcopy
from typing import List
from .types import Child

def snapshot_children_for_period(start_date: datetime.datetime, end_date: datetime.datetime, all_children: List[Child]):
    # Keep any children who have their first interaction before the end date, and haven't totally finished with care
    children = [
        deepcopy(c) for c in all_children 
        if min(e.start_date for e in c.episodes) < end_date and max(e.end_date for e in c.episodes) > start_date
    ]

    # Any future events need to be removed (or set to None)
    for c in children:
        if c.mother_child_dob is not None and c.mother_child_dob > end_date:
            c.mother_child_dob = None

        # Only include leaving data for those over 17.
        if (end_date - c.dob).days / 365 <= 17:
            c.leaving_care_data = None

        c.episodes = [deepcopy(e) for e in c.episodes if start_date < e.start_date < end_date or start_date < e.end_date < end_date]
        for episode in c.episodes:
            if episode.end_date > end_date:
                episode.end_date = None


    return children
