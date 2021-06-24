import datetime
import pandas as pd
from copy import deepcopy
from typing import List
from .types import Child

def filter_children_for_period(start_date: datetime.datetime, end_date: datetime.datetime, all_children: List[Child]):
    # Keep any children who have their first interaction before the end date, and haven't totally finished with care
    children = [
        deepcopy(c) for c in all_children 
        if min(e.start_date for e in c.episodes) < end_date and max(e.end_date for e in c.episodes) > start_date
    ]

    for c in children:
        if c.mother_child_dob is not None and c.mother_child_dob > end_date:
            c.mother_child_dob = None

    return children

def create_header(start_date: datetime.datetime, end_date: datetime.datetime, all_children: List[Child]) -> pd.DataFrame:
    children = filter_children_for_period(start_date, end_date, all_children)

    return pd.DataFrame({
        'CHILD': [c.child_id for c in children],
        'SEX': [c.sex for c in children],
        'DOB': [c.dob.strftime('%d/%m/%Y') for c in children],
        'ETHNIC': [c.ethnicity for c in children],
        'UPN': [c.upn for c in children],
        'MOTHER': [1 if c.mother_child_dob is not None else None for c in children],
        'MC_DOB': [c.mother_child_dob for c in children],
    })
