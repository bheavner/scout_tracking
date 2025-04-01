import csv
import argparse
import os

def load_advancement_data(filename):
    advancement_data = {}
    unassigned_scouts = set()  # Track scouts that are not assigned to a patrol
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            scout, requirement, date = row
            if scout not in advancement_data:
                advancement_data[scout] = []
            advancement_data[scout].append((requirement, date))
            unassigned_scouts.add(scout)  # Add scout to unassigned set initially
    return advancement_data, unassigned_scouts

def load_patrol_membership(filename):
    patrol_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            scout, patrol = row
            if patrol not in patrol_data:
                patrol_data[patrol] = []
            patrol_data[patrol].append(scout)
    return patrol_data

def load_requirements(filename):
    requirements = set()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            requirements.add(row[0])  # Assumes first column is the requirement name
    return requirements

def generate_report(advancement_data, patrol_data, requirements, patrol_name):
    scouts_in_patrol = patrol_data.get(patrol_name, [])
    report = []
    
    # Add the header row with the requirement names and patrol members
    header = ['Requirement'] + scouts_in_patrol
    report.append(header)
    
    # For each requirement, check if each scout has completed it
    for req in requirements:
        row = [req]  # First column will be the requirement name
        for scout in scouts_in_patrol:
            completed = '✔' if any(r == req for r, _ in advancement_data.get(scout, [])) else ''
            row.append(completed)
        report.append(row)
    
    return report

def save_report_to_tsv(report, patrol_name, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the path for the TSV file
    output_file = os.path.join(output_dir, f"{patrol_name}_report.tsv")
    
    # Write the report to the TSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(report)

    print(f"Report for patrol '{patrol_name}' saved to {output_file}.")

def generate_unassigned_report(unassigned_scouts, patrol_data, requirements, advancement_data, output_dir):
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
    
    # Add requirements not in the requirements list
    unlisted_requirements = set()
    for scout, requirements_completed in advancement_data.items():
        for requirement, _ in requirements_completed:
            if requirement not in requirements:
                unlisted_requirements.add(requirement)
    
    # Add unlisted requirements to the report
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
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (TSV format).")
    parser.add_argument('patrols_file', type=str, help="Path to the patrol membership file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    parser.add_argument('output_dir', type=str, help="Directory where the reports will be saved.")
    
    args = parser.parse_args()

    # Load the data
    advancement_data, unassigned_scouts = load_advancement_data(args.advancement_file)
    patrol_data = load_patrol_membership(args.patrols_file)
    requirements = load_requirements(args.requirements_file)

    # Generate the report for each patrol and save it as a TSV file
    for patrol_name in patrol_data:
        report = generate_report(advancement_data, patrol_data, requirements, patrol_name)
        save_report_to_tsv(report, patrol_name, args.output_dir)

    # Generate the unassigned scouts and unlisted requirements report
    generate_unassigned_report(unassigned_scouts, patrol_data, requirements, advancement_data, args.output_dir)

if __name__ == "__main__":
    main()

