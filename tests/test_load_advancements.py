import pytest
import os
import tempfile
from scout_tracking.load_advancements import load_advancements

@pytest.fixture
def patrol_structure():
    # Assuming initialize_full_structure works as expected
    # Create a mock patrol structure similar to your real data
    return {
        'purple people': {
            'ivan alexander': {'advancements': [], 'requirements': {}},
            'zachary wesner': {'advancements': [], 'requirements': {}}
        },
        'paw': {
            'max francis': {'advancements': [], 'requirements': {}},
            'truman bonlender': {'advancements': [], 'requirements': {}}
        }
    }

@pytest.fixture
def requirements_data():
    return [
        {'requirement': 'rank scout', 'alt_text': 'Scout Rank'},
        {'requirement': 'scout rank requirement 1a', 'alt_text': 'Scout 1a (Oath/Law/Motto/Slogan)'},
        {'requirement': 'scout rank requirement 1b', 'alt_text': 'Scout 1b (Scout Spirit)'},
        {'requirement': 'scout rank requirement 2a', 'alt_text': 'Scout 2a (First Aid)'}
    ]

@pytest.fixture
def advancement_file():
    # Return a temporary file or mock data for advancements
    data = "Name,Advancement Info,Date Completed\n"
    data += "Ivan Alexander,rank scout,11/15/2018\n"
    data += "Zachary Wesner,scout rank requirement 1a,4/30/2019\n"
    data += "Max Francis,scout rank requirement 3a,10/20/2020\n"  # Additional requirement for 'paw' patrol
    data += "Unknown Scout,scout rank requirement 1b,5/22/2021\n"  # Additional scout

    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as f:
        f.write(data)
        f.close()  # Close file so it can be accessed in the test

    return f.name

def test_load_advancements(patrol_structure, requirements_data, advancement_file):
    # Load the advancements into the patrol structure
    updated_structure, additional_scouts, additional_requirements = load_advancements(advancement_file, patrol_structure, [req['requirement'] for req in requirements_data])

    # Check that the advancements are correctly added
    assert 'rank scout' in updated_structure['purple people']['ivan alexander']['advancements']
    assert 'scout rank requirement 1a' in updated_structure['purple people']['zachary wesner']['advancements']

    # Check that additional scout is tracked
    assert 'unknown scout' in additional_scouts

    # Check that additional requirement is tracked
    assert 'scout rank requirement 3a' in additional_requirements
    assert len(additional_requirements) == 1  # Ensure only unique requirements are added

