import csv
import argparse
import os

def load_advancement_data(filename):
    advancement_data = {}  # This should be a dictionary, not a list
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=',')  # Assuming CSV format with commas
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) != 3:  # Ensure the row has 3 columns
                print(f"Skipping invalid row: {row}")  # Debugging invalid rows
                continue
            scout, advancement_info, date_completed = row
            scout = scout.strip().lower()  # Normalize scout name to lowercase

            if scout not in advancement_data:
                advancement_data[scout] = []  # Initialize list for new scouts

            # Append the (advancement_info, date_completed) tuple
            advancement_data[scout].append((advancement_info.strip(), date_completed.strip()))

    print(f"Finished loading advancement data: {advancement_data}")  # Debugging
    return advancement_data

def load_patrol_membership(filename):
    """ Load the patrol membership data (scout names and their patrols). """
    patrol_data = {}
    scouts_in_patrols = set()  # Track which scouts belong to patrols
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')  # Assuming TSV delimiter is '\t'
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:  # Validate row structure
                continue
            scout_name, patrol = row
            scout_name = scout_name.strip().lower()  # Normalize to lowercase
            patrol = patrol.strip()
            if patrol not in patrol_data:
                patrol_data[patrol] = []
            patrol_data[patrol].append(scout_name)
            scouts_in_patrols.add(scout_name)
    return patrol_data, scouts_in_patrols

def load_requirements(filename):
    """ Load the list of required advancements and their alternative texts. """
    requirements = []  # Use a list to maintain order
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')  # Assuming TSV delimiter is '\t'
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:  # Validate row structure
                continue
            requirement_name, alt_text = row
            requirements.append((requirement_name.strip().lower(), alt_text.strip()))  # Preserve order
    return requirements

def generate_report(advancement_data, patrol_data, requirements, patrol_name):
    scouts_in_patrol = patrol_data.get(patrol_name, [])
    report = []

    # Add the header row with the requirement names and patrol members
    header = ['Requirement'] + scouts_in_patrol
    report.append(header)

    # For each requirement, check if each scout has completed it
    for req, alt_text in requirements:
        row = [alt_text if alt_text else req]  # Use alternative text if available
        for scout in scouts_in_patrol:
            completed = '✔' if any(r == req for r, _ in advancement_data.get(scout, [])) else ''
            row.append(completed)
        report.append(row)

    return report

def save_report_to_tsv(report, patrol_name, output_dir):
    """ Save the report as a TSV file. """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{patrol_name}_report.tsv")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(report)
    print(f"Report for patrol '{patrol_name}' saved to {output_file}.")

def generate_unassigned_report(unassigned_scouts, patrol_data, advancement_data, requirements, output_dir):
    print(f"Unassigned scouts before report generation: {unassigned_scouts}")  # Debugging

    # Identify unassigned scouts
    assigned_scouts = set(scout for scouts in patrol_data.values() for scout in scouts)
    unassigned_scouts = unassigned_scouts - assigned_scouts
    
    unassigned_report = []
    
    # Add headers
    unassigned_report.append(["Scout", "Requirement", "Date"])
    
    # Add unassigned scouts to the report
    for scout in unassigned_scouts:
        for requirement, date in advancement_data.get(scout, []):
            unassigned_report.append([scout, requirement, date])
    
    # Create a set of valid requirements from the requirements list (from `requirements.tsv`)
    valid_requirements = set(req for req, _ in requirements)

    # Add requirements not in the requirements list
    unlisted_requirements = set()
    for scout, requirements_completed in advancement_data.items():
        for requirement, _ in requirements_completed:
            if requirement not in valid_requirements:
                unlisted_requirements.add(requirement)

    # Add unlisted requirements to the report under "Unknown Scout"
    for requirement in unlisted_requirements:
        unassigned_report.append(["Unknown Scout", requirement, "Not Assigned"])
    
    # Save the report to TSV
    output_file = os.path.join(output_dir, "unassigned_report.tsv")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(unassigned_report)
    
    print(f"Unassigned report saved to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description="Generate a scout advancement report.")
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('patrols_file', type=str, help="Path to the patrol membership file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    parser.add_argument('output_dir', type=str, help="Directory where the reports will be saved.")
    
    args = parser.parse_args()

    # Load the data
    patrol_data, unassigned_scouts = load_patrol_membership(args.patrols_file)
    advancement_data = load_advancement_data(args.advancement_file)  # Ensure it's being assigned correctly
    print(f"Loaded advancement data: {advancement_data}")  # Debugging: print advancement_data structure
    requirements = load_requirements(args.requirements_file)

    # Define scouts_in_patrols: A set of all scouts who are assigned to any patrol
    scouts_in_patrols = set(scout for scouts in patrol_data.values() for scout in scouts)

    # Identify unassigned scouts (scouts in advancement data but not in patrol data)
    unassigned_scouts = set(advancement_data.keys()) - scouts_in_patrols

    # Generate the report for each patrol and save it as a TSV file
    for patrol_name in patrol_data:
        report = generate_report(advancement_data, patrol_data, requirements, patrol_name)
        save_report_to_tsv(report, patrol_name, args.output_dir)

    # Generate the unassigned scouts and unlisted requirements report
    generate_unassigned_report(unassigned_scouts, patrol_data, advancement_data, requirements, args.output_dir)

if __name__ == "__main__":
    main()

