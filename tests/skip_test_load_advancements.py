import pytest
import os
import tempfile
from scout_tracking.advancements import load_advancement_data

@pytest.fixture
def mock_advancement_file():
    # Create a temporary CSV file to use for the test
    data = "Name,Advancement Info,Date Completed\n"  # Header row
    data += "Dylan Adams,rank scout,11/15/2018\n"
    data += "Dylan Adams,scout rank requirement 1a,4/30/2019\n"
    data += "Dylan Adams,scout rank requirement 1b,7/10/2019\n"
    data += "Dylan Adams,scout rank requirement 2a,1/19/2021\n"
    data += "Dylan Adams,scout rank requirement 2c,6/1/2022\n"
    data += "Dylan Adams,scout rank requirement 5x,7/22/2023\n"
    data += "Ivan Alexander,rank scout,5/22/2020\n"
    data += "Ivan Alexander,scout rank requirement 3a,8/10/2020\n"
    data += "Malcolm Blair,scout rank requirement 1c,10/5/2021\n"
    data += "Malcolm Blair,scout rank requirement 7,12/1/2021\n"
    data += "Zachary Wesner,scout rank requirement 9,2/22/2023\n"

    # Create a temporary file and write the data to it
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as f:
        f.write(data)
        f.close()  # Close file so it can be accessed in the test
    
    # Return the file path to the test file
    yield f.name
    
    # Cleanup: delete the temporary file after test is done
    os.remove(f.name)

def test_load_advancement_data(mock_advancement_file):
    # Load the advancement data using the mock file
    advancement_data = load_advancement_data(mock_advancement_file)
    
    # Check that the correct scouts are in the data
    assert 'dylan adams' in advancement_data
    assert 'ivan alexander' in advancement_data
    assert 'malcolm blair' in advancement_data
    assert 'zachary wesner' in advancement_data
    
    # Check that each scout has the correct advancements
    assert 'rank scout' in [adv.lower() for adv in advancement_data['dylan adams']]
    assert 'scout rank requirement 1a' in [adv.lower() for adv in advancement_data['dylan adams']]
    assert 'scout rank requirement 1b' in [adv.lower() for adv in advancement_data['dylan adams']]
    assert 'scout rank requirement 2a' in [adv.lower() for adv in advancement_data['dylan adams']]
    assert 'scout rank requirement 2c' in [adv.lower() for adv in advancement_data['dylan adams']]
    assert 'scout rank requirement 5x' in [adv.lower() for adv in advancement_data['dylan adams']]
    
    # Check that Ivan Alexander has the correct advancements
    assert 'rank scout' in [adv.lower() for adv in advancement_data['ivan alexander']]
    assert 'scout rank requirement 3a' in [adv.lower() for adv in advancement_data['ivan alexander']]
    
    # Check that multiple advancements for the same scout are handled (e.g., Dylan Adams)
    assert len(advancement_data['dylan adams']) == 6
    
    # Ensure that invalid or unexpected data (if any) is not present
    assert 'invalid advancement' not in advancement_data

