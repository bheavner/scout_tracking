import pytest
import os
from scout_tracking.load_patrol_data import load_patrol_data
from scout_tracking.initialize import initialize_patrol_structure

# Fixture to load the patrol data from the test file
@pytest.fixture
def patrol_data_file():
    return os.path.join(os.path.dirname(__file__), 'test_patrol_data.tsv')

@pytest.fixture
def patrol_data(patrol_data_file):
    return load_patrol_data(patrol_data_file)

def test_initialize_patrol_structure(patrol_data):
    patrol_structure = initialize_patrol_structure(patrol_data)
    
    # Test if patrol names are correctly used as keys
    assert 'purple people' in patrol_structure
    assert 'paw' in patrol_structure
    assert 'rrd' in patrol_structure
    
    # Test if scouts are correctly assigned to their patrols
    assert 'ivan alexander' in patrol_structure['purple people']
    assert 'zachary wesner' in patrol_structure['purple people']
    assert 'max francis' in patrol_structure['paw']
    assert 'truman bonlender' in patrol_structure['paw']
    assert 'parker hennessey' in patrol_structure['rrd']
    
    # Test if the advancements list is initialized as empty for each scout
    assert patrol_structure['purple people']['ivan alexander'] == {'advancements': []}  # Updated check

