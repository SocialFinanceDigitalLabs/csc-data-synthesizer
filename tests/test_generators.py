import re
from cscsynth.generators import generate_upn

def test_generate_upn():
    for i in range(1000):
        upn = generate_upn()

        assert len(upn) == 13
        assert re.match(r'[A-Z][0-9]{12}', upn)