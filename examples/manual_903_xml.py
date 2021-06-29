import datetime
from cscsynth import ChildrenGenerator
from cscsynth.census import snapshot_children_for_period
from cscsynth.xml import create_xml

start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2020, 1 ,1)

gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

all_children = gen.generate(num_children=500)

census_start = datetime.datetime(2017, 4, 1)
census_end = datetime.datetime(2018, 4, 1)
children = snapshot_children_for_period(census_start, census_end, all_children)

create_xml(children, 'fake_903.xml')
