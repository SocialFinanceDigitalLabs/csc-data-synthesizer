import os
import datetime
from cscsynth import ChildrenGenerator
from cscsynth.census import snapshot_children_for_period
from cscsynth.csv import create_csv
from pathlib import Path

start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2021, 12 , 31)

gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

all_children = gen.generate(num_children=5000)

census_start = datetime.datetime(2019, 4, 1)
census_end = datetime.datetime(2020, 3, 31)
children = snapshot_children_for_period(census_start, census_end, all_children)

output_path = Path(__file__).parent / "../output"
output_path.mkdir(parents=True, exist_ok=True)
create_csv(children, output_path)