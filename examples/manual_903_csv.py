import os
import datetime
from cscsynth import ChildrenGenerator
from cscsynth.census import snapshot_children_for_period
from cscsynth.csv import create_csv

start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2020, 1 ,1)

gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

all_children = gen.generate(num_children=5000)

census_start = datetime.datetime(2017, 4, 1)
census_end = datetime.datetime(2018, 4, 1)
children = snapshot_children_for_period(census_start, census_end, all_children)

output_dir = os.path.join(os.path.dirname(__file__), 'output')
create_csv(children, output_dir)