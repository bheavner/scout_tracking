import pytest
import os
from scout_tracking.utilities import get_scout_patrol, report_invalid_advancements

# Fixture to supply the test_patrol_data.tsv file for testing
@pytest.fixture
def test_patrol_data_file():
    return os.path.join(os.path.dirname(__file__), 'test_patrol_data.tsv')

    
    # Test getting the patrol of specific scouts
    assert get_scout_patrol('ivan alexander', patrol_data) == 'purple people'
    assert get_scout_patrol('malcolm blair', patrol_data) == 'paw'
    assert get_scout_patrol('alexis simard', patrol_data) == 'rrd'
    
    # Test when a scout doesn't exist
    assert get_scout_patrol('nonexistent scout', patrol_data) is None

def test_report_invalid_advancements():
    invalid_advancements = [
        ('scout rank requirement 5x', 'ivan alexander'),
        ('scout rank requirement 9', 'malcolm blair')
    ]
    
    # Capture printed output (or logs) of invalid advancements
    invalid_report = report_invalid_advancements(invalid_advancements)
    
    # Test that invalid advancements are correctly reported
    assert 'scout rank requirement 5x' in invalid_report
    assert 'scout rank requirement 9' in invalid_report
