import os
import pandas as pd
from collections import defaultdict
from copy import deepcopy
from typing import List
from .types import Child

def create_csv(children: List[Child], output_dir: str):
    header_df = create_header(children)
    episodes_df = create_episodes(children)
    uasc_df = create_uasc(children)
    reviews_df = create_reviews(children)
    oc3_df = create_oc3(children)
    ad1_df = create_ad1(children)
    sbpfa_df = create_should_be_placed_for_adoption(children)

    header_df.to_csv(os.path.join(output_dir, 'header.csv'), index=False)
    episodes_df.to_csv(os.path.join(output_dir, 'episodes.csv'), index=False)
    uasc_df.to_csv(os.path.join(output_dir, 'uasc.csv'), index=False)
    reviews_df.to_csv(os.path.join(output_dir, 'reviews.csv'), index=False)
    oc3_df.to_csv(os.path.join(output_dir, 'oc3.csv'), index=False)
    ad1_df.to_csv(os.path.join(output_dir, 'ad1.csv'), index=False)
    sbpfa_df.to_csv(os.path.join(output_dir, 'placed_for_adoption.csv'), index=False)

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

def create_reviews(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)

    for child in children:
        for review in child.reviews:
            data['CHILD'].append(child.child_id)
            data['DOB'].append(child.dob.strftime('%d/%m/%Y'))
            data['REVIEW'].append(review.review_date.strftime('%d/%m/%Y'))
            data['REVIEW_CODE'].append(review.review_code)

    return pd.DataFrame(data)

def create_oc3(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)

    for child in children:
        if child.leaving_care_data is not None:
            data['CHILD'].append(child.child_id)
            data['DOB'].append(child.dob.strftime('%d/%m/%Y'))
            data['IN_TOUCH'].append(child.leaving_care_data.in_touch)
            data['ACTIV'].append(child.leaving_care_data.activ)
            data['ACCOM'].append(child.leaving_care_data.accom)

    return pd.DataFrame(data)

def create_ad1(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)
    for child in children:
        if child.adoption_data is not None:
            ad = child.adoption_data
            data['CHILD'].append(child.child_id)
            data['DOB'].append(child.dob.strftime('%d/%m/%Y'))
            data['DATE_INT'].append(ad.start_date.strftime('%d/%m/%Y'))
            data['DATE_MATCH'].append(ad.start_date.strftime('%d/%m/%Y'))
            data['FOSTER_CARE'].append(ad.foster_care)
            data['NB_ADOPTR'].append(ad.number_adopters)
            data['SEX_ADOPTR'].append(ad.sex_adopter)
            data['LS_ADOPTR'].append(ad.ls_adopter)

    return pd.DataFrame(data)

def create_should_be_placed_for_adoption(children: List[Child]) -> pd.DataFrame:
    data = defaultdict(list)
    for child in children:
        if child.adoption_data is not None:
            ad = child.adoption_data
            data['CHILD'].append(child.child_id)
            data['DOB'].append(child.dob.strftime('%d/%m/%Y'))
            data['DATE_PLACED'].append(ad.start_date.strftime('%d/%m/%Y'))
            data['DATE_PLACED_CEASED'].append(ad.end_date.strftime('%d/%m/%Y') if ad.end_date is not None else None)
            data['REASON_PLACED_CEASED'].append(ad.reason_ceased if ad.reason_ceased is not None else None)

    return pd.DataFrame(data)
