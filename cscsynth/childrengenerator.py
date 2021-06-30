import datetime
import random
from typing import List
from .types import Probabilities, Child
from .generators import (
    generate_ethnicity,
    generate_upn,
    generate_child_id,
    generate_dob,
    generate_motherhood_date,
    generate_uasc_ceased_date,
    generate_episodes,
    generate_reviews,
)


class ChildrenGenerator:
    def __init__(self, start_date: datetime.datetime, end_date: datetime.datetime, probabilities: Probabilities = None):
        self.start_date = start_date
        self.end_date = end_date

        if probabilities is None:
            # Use the defaults in the class
            probabilities = Probabilities()

        self.probabilities = probabilities

    def generate(self, num_children: int) -> List[Child]:
        upn_generator = generate_upn()
        child_id_generator = generate_child_id()

        children = []
        for _ in range(num_children):
            child_id = next(child_id_generator)
            upn = next(upn_generator)
            dob = generate_dob(self.start_date)
            sex = random.randint(1, 2)

            mother_child_dob = generate_motherhood_date(self.probabilities.is_mother, sex, dob)

            date_uasc_ceased = generate_uasc_ceased_date(self.probabilities.is_uasc, dob)
            
            episodes = generate_episodes(self.start_date, dob, self.probabilities)

            reviews = generate_reviews(episodes, self.probabilities.review_frequency)

            # TODO: Generate a set of missing episodes
            missing_periods = []
            
            child = Child(
                upn=upn,
                child_id=child_id,
                dob=dob,
                sex=sex,
                ethnicity=generate_ethnicity(),
                episodes=episodes,
                reviews=reviews,
                mother_child_dob=mother_child_dob,
                missing_periods=missing_periods,
                date_uasc_ceased=date_uasc_ceased,
            )

            children.append(child)

        return children
