import pytest
import os
import csv
from report import generate_patrol_report_csv

# Define a pytest fixture to set up the test data
@pytest.fixture
def setup_data():
    patrol_structure = {
        'paw': {
            'max francis': {'advancements': ['Rank Scout']},
            'truman bonlender': {'advancements': ['Scout Rank Requirement 1a']}
        },
        'purple people': {
            'ivan alexander': {'advancements': ['Rank Scout', 'Scout Rank Requirement 1a']},
            'zachary wesner': {'advancements': ['Scout Rank Requirement 1a', 'Scout Rank Requirement 2a']}
        }
    }
    requirements = ['Rank Scout', 'Scout Rank Requirement 1a', 'Scout Rank Requirement 2a']
    output_dir = '/tmp/test_patrol_reports'
    return patrol_structure, requirements, output_dir

# Test the generation of CSV reports for all patrols
def test_generate_reports_for_all_patrols(setup_data):
    patrol_structure, requirements, output_dir = setup_data

    # Generate reports for all patrols
    generate_patrol_report_csv(patrol_structure, requirements, output_dir)

    # Check that CSV files for all patrols have been created
    paw_report = os.path.join(output_dir, 'paw_report.csv')
    purple_report = os.path.join(output_dir, 'purple_people_report.csv')

    assert os.path.exists(paw_report), "The 'paw' patrol report was not generated."
    assert os.path.exists(purple_report), "The 'purple people' patrol report was not generated."

    # Verify the content of the 'paw' patrol report
    with open(paw_report, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Check the header
        assert rows[0] == ['Requirement', 'max francis', 'truman bonlender'], "Header row mismatch in 'paw' report."

        # Check that the requirements and advancements are correctly marked
        assert rows[1] == ['Rank Scout', 'X', ''], "Row for 'Rank Scout' in 'paw' report is incorrect."
        assert rows[2] == ['Scout Rank Requirement 1a', '', 'X'], "Row for 'Scout Rank Requirement 1a' in 'paw' report is incorrect."

    # Verify the content of the 'purple people' patrol report
    with open(purple_report, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Check the header
        assert rows[0] == ['Requirement', 'ivan alexander', 'zachary wesner'], "Header row mismatch in 'purple people' report."

        # Check that the requirements and advancements are correctly marked
        assert rows[1] == ['Rank Scout', 'X', ''], "Row for 'Rank Scout' in 'purple people' report is incorrect."
        assert rows[2] == ['Scout Rank Requirement 1a', 'X', 'X'], "Row for 'Scout Rank Requirement 1a' in 'purple people' report is incorrect."
        assert rows[3] == ['Scout Rank Requirement 2a', '', 'X'], "Row for 'Scout Rank Requirement 2a' in 'purple people' report is incorrect."

# Test the generation of reports for a specific patrol ('purple people' only)
def test_generate_reports_for_specific_patrol(setup_data):
    patrol_structure, requirements, output_dir = setup_data

    # Generate reports for the 'purple people' patrol only
    generate_patrol_report_csv(patrol_structure, requirements, output_dir, patrol_names=['purple people'])

    # Check that only the 'purple people' patrol report is created
    purple_report = os.path.join(output_dir, 'purple_people_report.csv')
    assert os.path.exists(purple_report), "The 'purple people' patrol report was not generated."

    # Ensure that the 'paw' patrol report does not exist
    paw_report = os.path.join(output_dir, 'paw_report.csv')
    assert not os.path.exists(paw_report), "The 'paw' patrol report was incorrectly generated."

    # Verify the content of the 'purple people' patrol report
    with open(purple_report, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Check the header
        assert rows[0] == ['Requirement', 'ivan alexander', 'zachary wesner'], "Header row mismatch in 'purple people' report."

        # Check that the requirements and advancements are correctly marked
        assert rows[1] == ['Rank Scout', 'X', ''], "Row for 'Rank Scout' in 'purple people' report is incorrect."
        assert rows[2] == ['Scout Rank Requirement 1a', 'X', 'X'], "Row for 'Scout Rank Requirement 1a' in 'purple people' report is incorrect."
        assert rows[3] == ['Scout Rank Requirement 2a', '', 'X'], "Row for 'Scout Rank Requirement 2a' in 'purple people' report is incorrect."

# Test the case where no reports should be generated if there are no scouts
def test_no_scouts_in_patrol(setup_data):
    patrol_structure, requirements, output_dir = setup_data

    # Generate reports for a patrol with no scouts
    patrol_structure_with_no_scouts = {
        'no_scouts': {}
    }

    generate_patrol_report_csv(patrol_structure_with_no_scouts, requirements, output_dir, patrol_names=['no_scouts'])

    # Check that no report is generated for this patrol
    no_scouts_report = os.path.join(output_dir, 'no_scouts_report.csv')
    assert not os.path.exists(no_scouts_report), "Report was incorrectly generated for the 'no_scouts' patrol."

# Test the creation of the output directory if it doesn't exist
def test_create_output_directory(setup_data):
    patrol_structure, requirements, output_dir = setup_data

    # Ensure the directory doesn't exist before the test
    if os.path.exists(output_dir):
        os.rmdir(output_dir)

    # Generate reports for all patrols
    generate_patrol_report_csv(patrol_structure, requirements, output_dir)

    # Check if the directory was created
    assert os.path.exists(output_dir), "Output directory was not created."

    # Clean up by removing the directory after the test
    os.rmdir(output_dir)

