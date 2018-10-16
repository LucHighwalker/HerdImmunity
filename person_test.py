import pytest
import random
import io
import sys
from person import Person

def test_did_survive_infection():
    victim = Person(215, False, True)
    assert victim.did_survive_infection(1) == 1
    survivor = Person(420, False, True)
    assert survivor.did_survive_infection(0) == 0
