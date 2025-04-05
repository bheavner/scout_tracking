import pytest
import os
from scout_tracking.load_patrol_data import load_patrol_data

@pytest.fixture
def patrol_data_file():
    return os.path.join(os.path.dirname(__file__), 'test_patrol_data.tsv')

def test_load_patrol_data(patrol_data_file):
    patrol_data = load_patrol_data(patrol_data_file)
    assert patrol_data['ivan alexander'] == 'purple people'
    assert patrol_data['max francis'] == 'paw'
