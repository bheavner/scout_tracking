import csv
import os
import argparse
import datetime

def validate_patrol_data(patrol_data):
    # Check for duplicates
    all_scouts = set()
    for patrol, scouts in patrol_data.items():
        for scout in scouts:
            if scout in all_scouts:
                print(f"Duplicate scout '{scout}' found in multiple patrols!")
            all_scouts.add(scout)

# Load patrol data
def load_patrol_data(filename):
    patrol_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            scout, patrol = row
            scout = scout.strip().lower()
            patrol = patrol.strip()
            if patrol not in patrol_data:
                patrol_data[patrol] = []
            patrol_data[patrol].append(scout)
    validate_patrol_data(patrol_data)
    return patrol_data

def validate_requirements_data(requirements_data):
    if not requirements_data:
        print("Warning: Requirements data is empty!")
    
    for req, description in requirements_data.items():
        if not req or not description:
            print(f"Invalid entry: Requirement '{req}' has no description.")
        if req in requirements_data and requirements_data[req] == '':
            print(f"Warning: Requirement '{req}' has an empty description.")

# Load requirements data
def load_requirements(filename):
    requirements_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            requirement, alt_text = row
            requirements_data[requirement.strip()] = alt_text.strip()
    validate_requirements_data(requirements_data)
    return requirements_data

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return False

def validate_advancement_data(advancement_data, requirements_data):
    for scout, requirements in advancement_data.items():
        for req, completed in requirements.items():
            if req not in requirements_data:
                print(f"Warning: '{req}' requirement not found in requirements file for scout '{scout}'.")

# Load advancement data
def load_advancement_data(filename):
    advancement_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:
                continue
            scout, requirement, date_completed = row
            scout = scout.strip().lower()  # Normalize name to lowercase
            if scout not in patrol_data:
                print(f"Warning: Scout '{scout}' not found in patrol data!")
                continue
            
            # Validate date format
            if not validate_date(date_completed):
                continue
            
            if scout not in advancement_data:
                advancement_data[scout] = {}
            advancement_data[scout][requirement.strip()] = True
    
    validate_advancement_data(advancement_data, requirements_data)
    return advancement_data

# Generate the patrol report
def generate_patrol_report(patrol_data, requirements_data, advancement_data, patrol_name):
    # Create the 3D structure: patrol -> scout -> requirements
    report_data = {}
    patrol_scouts = patrol_data.get(patrol_name, [])
    
    for scout in patrol_scouts:
        report_data[scout] = {}
        for requirement, alt_text in requirements_data.items():
            completed = requirement in advancement_data.get(scout, {})
            report_data[scout][requirement] = completed
    
    return report_data

# Save the report to a file
def save_report(report_data, patrol_name, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the path for the TSV file
    output_file = os.path.join(output_dir, f"{patrol_name}_report.tsv")
    
    # Write the report to the TSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write header row with scouts' names
        header = ['Requirement'] + list(report_data.keys())
        writer.writerow(header)

        # Write each requirement row
        for requirement, alt_text in requirements_data.items():
            row = [alt_text if alt_text else requirement]
            for scout in report_data:
                completed = '✔' if report_data[scout].get(requirement, False) else ''
                row.append(completed)
            writer.writerow(row)

    print(f"Report for patrol '{patrol_name}' saved to {output_file}.")

# Main function to parse arguments and generate the report
def main():
    parser = argparse.ArgumentParser(description="Generate a scout advancement report for a specific patrol.")
    
    # Arguments for input files
    parser.add_argument('patrol_file', type=str, help="Path to the patrol data file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    
    # Argument for the output directory
    parser.add_argument('output_dir', type=str, help="Directory where the reports will be saved.")
    
    # Argument for the patrol name to generate the report for
    parser.add_argument('patrol_name', type=str, help="Name of the patrol to generate the report for (e.g., 'Purple People').")
    
    args = parser.parse_args()

    # Load data
    patrol_data = load_patrol_data(args.patrol_file)
    requirements_data = load_requirements(args.requirements_file)
    advancement_data = load_advancement_data(args.advancement_file, patrol_data)

    # Generate the report for the specified patrol
    report_data = generate_patrol_report(patrol_data, requirements_data, advancement_data, args.patrol_name)

    # Save the report
    save_report(report_data, args.patrol_name, args.output_dir)

if __name__ == "__main__":
    main()

