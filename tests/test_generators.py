import itertools
import re
from cscsynth.generators import generate_upn

def test_generate_upn():
    generator = generate_upn()

    seen_upns = set()
    for upn in itertools.islice(generator, 1000):
        assert len(upn) == 13
        assert re.match(r'[A-Z][0-9]{12}', upn)

        assert upn not in seen_upns
        seen_upns.add(upn)