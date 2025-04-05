import pytest
import os
import csv
import shutil
from scout_tracking.report import generate_patrol_report_csv
from scout_tracking.load_requirements import load_requirements

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
    # Define the path to the requirements file (adjust the path as needed)
    requirements_file_path = os.path.join(os.path.dirname(__file__), 'test_requirements.tsv')

    # Load the requirements using the function
    requirements = load_requirements(requirements_file_path)

    #debug: check requirements structure
    print("Loaded requirements:")
    print(requirements)
 
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

        # Debugging: print the rows read from the 'paw' report
        print("\nPaw Report Rows:")
        for row in rows:
            print(row)

        # Check the header
        assert rows[0] == ['Requirement', 'max francis', 'truman bonlender'], "Header row mismatch in 'paw' report."

        # Check that the requirements and advancements are correctly marked (use Alt Text values)
        assert rows[1] == ['Scout Rank', 'X', ''], "Row for 'Scout Rank' in 'paw' report is incorrect."
        assert rows[2] == ['Scout 1a (Oath/Law/Motto/Slogan)', '', 'X'], "Row for 'Scout 1a (Oath/Law/Motto/Slogan)' in 'paw' report is incorrect."

    # Verify the content of the 'purple people' patrol report
    with open(purple_report, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Debugging: print the rows read from the 'purple people' report
        print("\nPurple People Report Rows:")
        for row in rows:
            print(row)

        # Check the header
        assert rows[0] == ['Requirement', 'ivan alexander', 'zachary wesner'], "Header row mismatch in 'purple people' report."

        # Check that the requirements and advancements are correctly marked (use Alt Text values)
        assert rows[1] == ['Scout Rank', 'X', ''], "Row for 'Scout Rank' in 'purple people' report is incorrect."
        assert rows[2] == ['Scout 1a (Oath/Law/Motto/Slogan)', 'X', 'X'], "Row for 'Scout 1a (Oath/Law/Motto/Slogan)' in 'purple people' report is incorrect."
        assert rows[5] == ['Scout 2a (First Aid)', '', 'X'], "Row for 'Scout 2a (First Aid)' in 'purple people' report is incorrect."

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
        # Check that the requirements and advancements are correctly marked (use Alt Text values)
        assert rows[1] == ['Scout Rank', 'X', ''], "Row for 'Scout Rank' in 'purple people' report is incorrect."
        assert rows[2] == ['Scout 1a (Oath/Law/Motto/Slogan)', 'X', 'X'], "Row for 'Scout 1a (Oath/Law/Motto/Slogan)' in 'purple people' report is incorrect."
        assert rows[5] == ['Scout 2a (First Aid)', '', 'X'], "Row for 'Scout 2a (First Aid)' in 'purple people' report is incorrect."

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
        shutil.rmtree(output_dir)

    # Generate reports for all patrols
    generate_patrol_report_csv(patrol_structure, requirements, output_dir)

    # Check if the directory was created
    assert os.path.exists(output_dir), "Output directory was not created."

    # Clean up by removing the directory after the test
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

