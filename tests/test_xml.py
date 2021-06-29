import os
import datetime
from lxml import etree
from cscsynth import ChildrenGenerator
from cscsynth.census import create_xml, snapshot_children_for_period

def test_xml_schema(tmpdir):
    base_path = os.path.join(os.path.dirname(__file__), 'data')
    xmlschema = etree.XMLSchema(etree.parse(os.path.join(base_path, 'CLA.xsd')))

    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2020, 1 ,1)

    gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

    all_children = gen.generate(num_children=500)

    census_start = datetime.datetime(2017, 4, 1)
    census_end = datetime.datetime(2018, 4, 1)
    children = snapshot_children_for_period(census_start, census_end, all_children)

    output_path = os.path.join(base_path, 'generated_903.xml')
    create_xml(children, output_path)
    
    created_xml = etree.parse(output_path)

    xmlschema.assert_(created_xml)
