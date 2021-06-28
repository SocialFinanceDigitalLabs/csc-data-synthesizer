import datetime
import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict
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

        c.episodes = [deepcopy(e) for e in c.episodes if start_date < e.start_date < end_date or start_date < e.end_date < end_date]
        for episode in c.episodes:
            if episode.end_date > end_date:
                episode.end_date = None


    return children

def create_header(children: List[Child]) -> pd.DataFrame:
    return pd.DataFrame({
        'CHILD': [c.child_id for c in children],
        'SEX': [c.sex for c in children],
        'DOB': [c.dob.strftime('%d/%m/%Y') for c in children],
        'ETHNIC': [c.ethnicity for c in children],
        'UPN': [c.upn for c in children],
        'MOTHER': [1 if c.mother_child_dob is not None else None for c in children],
        'MC_DOB': [c.mother_child_dob.strftime('%d/%m/%Y') if c.mother_child_dob is not None else None for c in children],
    })

def create_episodes(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)

    for child in children:
        for episode in child.episodes:
            data['CHILD'].append(child.child_id)
            data['DECOM'].append(episode.start_date.strftime('%d/%m/%Y'))
            data['RNE'].append(episode.reason_for_new_episode)
            data['LS'].append(episode.legal_status)
            data['CIN'].append(episode.cin)
            data['PLACE'].append(episode.place)
            data['PLACE_PROVIDER'].append(episode.place_provider)
            data['DEC'].append(episode.end_date.strftime('%d/%m/%y') if episode.end_date is not None else None)
            data['REC'].append(episode.reason_end)
            data['REASON_PLACE_CHANGE'].append(episode.reason_place_change)
            data['HOME_POST'].append(episode.home_postcode)
            data['PL_POST'].append(episode.place_postcode)
            data['URN'].append(episode.urn)

    return pd.DataFrame(data)

def create_uasc(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)

    for child in children:
        if child.date_uasc_ceased is not None:
            data['CHILD'].append(child.child_id)
            data['SEX'].append(child.sex)
            data['DOB'].append(child.dob.strftime('%d/%m/%Y'))
            data['DUC'].append(child.date_uasc_ceased.strftime('%d/%m/%Y'))

    return pd.DataFrame(data)

