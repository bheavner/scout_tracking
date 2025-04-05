import os
import pytest
from scout_tracking.report import generate_additional_report

@pytest.fixture
def setup_data():
    # Example additional scouts and requirements
    additional_scouts = ['alice', 'bob', 'charlie']
    additional_requirements = ['Requirement X', 'Requirement Y', 'Requirement Z']
    output_dir = '/tmp/test_additional_report'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    yield additional_scouts, additional_requirements, output_dir
    # Cleanup after test
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(output_dir)

def test_generate_additional_report(setup_data):
    additional_scouts, additional_requirements, output_dir = setup_data
    
    # Generate the additional report
    generate_additional_report(additional_scouts, additional_requirements, output_dir)
    
    # Check that the report was created
    report_path = os.path.join(output_dir, "additional_report.txt")
    assert os.path.exists(report_path)
    
    # Check the contents of the report
    with open(report_path, 'r') as file:
        content = file.read()
    
    assert "Scouts not in Patrols:" in content
    assert "alice" in content
    assert "bob" in content
    assert "charlie" in content
    assert "Requirements not in requirements list:" in content
    assert "Requirement X" in content
    assert "Requirement Y" in content
    assert "Requirement Z" in content

