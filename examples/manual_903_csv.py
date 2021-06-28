import datetime
from cscsynth import ChildrenGenerator
from cscsynth.census import create_episodes, create_header, create_uasc

start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2020, 1 ,1)

gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

children = gen.generate(num_children=5000)

census_start = datetime.datetime(2017, 4, 1)
census_end = datetime.datetime(2018, 4, 1)

header_df = create_header(census_start, census_end, children)
episodes_df = create_episodes(census_start, census_end, children)
uasc_df = create_uasc(census_start, census_end, children)

header_df.to_csv('header.csv', index=False)
episodes_df.to_csv('episodes.csv', index=False)
uasc_df.to_csv('uasc.csv', index=False)
