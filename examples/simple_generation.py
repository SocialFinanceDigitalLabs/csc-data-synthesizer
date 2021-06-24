import datetime
from cscsynth import ChildrenGenerator

start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2020, 1 ,1)

gen = ChildrenGenerator(start_date=start_date, end_date=end_date)

children = gen.generate(num_children=10)

for c in children:
    print(c.dob)
    for ep in c.episodes:
        print(ep)
    print('')