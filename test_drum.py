#
# to run the code, type the following into  the terminal:
# pytest -v -s test_drum.py
#

import drum
from io import StringIO
import pytest
import re
import sys

# pytest uses fixtures rather than explicit setup/teardown methods
# tests in pytest are generally written as functions rather than as classes
@pytest.fixture()
def new_song():
    return drum.Song("Animal Rights", 128)


def test_add_pattern(new_song):
    new_song.add_pattern("cowbell2", "01010101")
    assert new_song.patterns["cowbell2"] == "01010101"


# Since dictionaries use hashes to store values,
# when we extract values with a for loop in the one_count_gen method
# we could extract the pattern attributes in any order.
# So we use regular expressions to test.
def test_one_count_gen(new_song):
    step = new_song.one_count_gen()
    new_song.add_pattern("cowbell", "01100000")
    new_song.add_pattern("cowbell2", "01010101")
    assert next(step) == "| X "
    regex = re.compile("\| cowbell2? \+ cowbell2? ")
    assert regex.match(next(step))


# We don't need to test as the sysout is writing;
# that would be difficult to do without changing the code.
# Instead we capture sysout in a variable and test that
# variable against our expected output.
@pytest.fixture()
def sys_output(new_song):
    sys.stdout = StringIO()
    drum.play(new_song, stop_time=15)
    return sys.stdout.getvalue()


# It is reasonable to assume we don't have to
# test Python's builtin sleep() function.
# So the only part of the beat timing we need to measure
# is how many counts are in the song
# For 128 BPM, with a 15s play time, we should have
# ((128*2)/60)*15 = 64 counts in our output
# But some very slight variation should be fine.
def test_number_of_counts(sys_output):
    assert (sys_output.count("|") - 64) <= 1.
