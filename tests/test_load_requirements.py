import pytest
import os
from scout_tracking.load_requirements import load_requirements

@pytest.fixture
def requirements_file():
    return os.path.join(os.path.dirname(__file__), 'test_requirements.tsv')

def test_load_requirements(requirements_file):
    requirements_data = load_requirements(requirements_file)
    
    # Test if specific requirements are loaded correctly
    assert 'rank scout' in requirements_data
    assert requirements_data['rank scout'] == 'Scout Rank'
    
    assert 'scout rank requirement 1a' in requirements_data
    assert requirements_data['scout rank requirement 1a'] == 'Scout 1a (Oath/Law/Motto/Slogan)'
    
    assert 'scout rank requirement 4b' in requirements_data
    assert requirements_data['scout rank requirement 4b'] == 'Scout 4b (Whip and Fuse Rope)'

