import xml.etree.ElementTree as ET
from functools import partial
from copy import deepcopy
from typing import List
from .types import Child

def create_xml(children: List[Child], file_name: str) -> ET:
    def _make_node_with_text(root, node_name, node_text):
        el = ET.SubElement(root, node_name)
        el.text = node_text
        return el

    root = ET.Element('EXPSSDA903')
    for child in children:
        c_root = ET.SubElement(root, 'CHILD')

        header = ET.SubElement(c_root, 'HEADER')
        header_add = partial(_make_node_with_text, header)

        header_add('CHILDID', str(child.child_id))
        header_add('UPN', child.upn)
        header_add('SEX', str(child.sex))
        header_add('DOB', child.dob.strftime('%d/%m/%Y'))
        header_add('ETHNIC', child.ethnicity)
        header_add('UASC', str(1) if child.date_uasc_ceased is not None else None)
        # TODO: Add adoption
        # TODO: Add missing episodes

        for review in child.reviews:
            reviews_node = ET.SubElement(header, 'AREVIEW')
            _make_node_with_text(reviews_node, 'REVIEW', review.review_date.strftime('%d/%m/%Y'))
            _make_node_with_text(reviews_node, 'REVIEW_CODE', review.review_code)

        header_add('MOTHER', str(1) if child.mother_child_dob is not None else None)
        header_add('MC_DOB', child.mother_child_dob.strftime('%d/%m/%Y') if child.mother_child_dob is not None else None)
        # TODO: Add previous permanance info
        # TODO: Add OC2

        for episode in child.episodes:
            e_root = ET.SubElement(c_root, 'EPISODE')
            episodes_add = partial(_make_node_with_text, e_root)

            episodes_add('DECOM', episode.start_date.strftime('%d/%m/%Y'))
            episodes_add('RNE', episode.reason_for_new_episode)
            episodes_add('LS', episode.legal_status)
            episodes_add('CIN', episode.cin)
            episodes_add('PL', episode.place)
            episodes_add('PL_POST', episode.place_postcode)
            episodes_add('HOME_POST', episode.home_postcode)
            episodes_add('URN', str(episode.urn))
            episodes_add('PLACE_PROVIDER', episode.place_provider)
            episodes_add('DEC', episode.end_date.strftime('%d/%m/%Y') if episode.end_date is not None else None)
            episodes_add('REC', episode.reason_end)
            episodes_add('REASON_PLACE_CHANGE', episode.reason_place_change)

    ET.ElementTree(element=root).write(file_name, xml_declaration=True)
