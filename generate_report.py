import csv
import os
import argparse

# Load advancement data
def load_advancement_data(filename):
    advancement_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:  # Ensure the row has 3 columns
                continue
            scout, requirement, _ = row
            scout = scout.strip().lower()  # Normalize name to lowercase
            requirement = requirement.strip()
            if scout not in advancement_data:
                advancement_data[scout] = set()  # Use set to avoid duplicates
            advancement_data[scout].add(requirement)  # Add the completed requirement
    return advancement_data

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
    return patrol_data

# Load requirements data
def load_requirements(filename):
    requirements = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            requirement, alt_text = row
            requirements.append((requirement.strip(), alt_text.strip()))
    return requirements

# Generate the patrol report
def generate_patrol_report(patrol, patrol_data, advancement_data, requirements, output_dir):
    # List of all required requirements
    required_requirements = [req[0].strip() for req in requirements]  # Getting the first column from requirements.tsv
    
    # Prepare the file path for saving the report
    output_file = os.path.join(output_dir, f"{patrol}_report.tsv")

    # Write the header
    with open(output_file, 'w') as file:
        file.write("Requirement\t")
        file.write("\t".join(patrol_data[patrol]) + "\n")
        
        # Iterate through the requirements and list them in order
        for req in required_requirements:
            file.write(req + "\t")
            for scout in patrol_data[patrol]:
                scout_lower = scout.lower()
                # If the scout has completed the requirement, indicate the completion date
                if scout_lower in advancement_data:
                    completed_requirements = [r[0].lower() for r in advancement_data[scout_lower]]
                    if req.lower() in completed_requirements:
                        completed_date = next(r[1] for r in advancement_data[scout_lower] if r[0].lower() == req.lower())
                        file.write(completed_date + "\t")
                    else:
                        file.write("\t")
                else:
                    file.write("\t")
            file.write("\n")
    print(f"Patrol report for {patrol} saved to {output_file}")

# Save the report to a file
def save_report(report, patrol_name, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the path for the TSV file
    output_file = os.path.join(output_dir, f"{patrol_name}_report.tsv")
    
    # Write the report to the TSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(report)

    print(f"Report for patrol '{patrol_name}' saved to {output_file}.")

# Main function to parse arguments and generate reports
def main():
    parser = argparse.ArgumentParser(description="Generate a scout advancement report for a specific patrol or all patrols.")
    
    # Arguments for input files
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('patrol_file', type=str, help="Path to the patrol membership file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    
    # Argument for the output directory
    parser.add_argument('output_dir', type=str, help="Directory where the reports will be saved.")
    
    # Argument for the patrol names to generate reports for (can specify multiple patrols, or 'all' for all patrols)
    parser.add_argument('patrols', type=str, nargs='*', default=['all'], help="Names of the patrols to generate reports for (space-separated), or 'all' for all patrols.")

    args = parser.parse_args()

    # Load data
    advancement_data = load_advancement_data(args.advancement_file)
    patrol_data = load_patrol_data(args.patrol_file)
    requirements = load_requirements(args.requirements_file)

    # If 'all' is specified, generate reports for all patrols
    if 'all' in args.patrols:
        args.patrols = list(patrol_data.keys())

    # Generate reports for the specified patrols
    for patrol_name in args.patrols:
        if patrol_name in patrol_data:
            report = generate_patrol_report(advancement_data, patrol_data, requirements, patrol_name)
            save_report(report, patrol_name, args.output_dir)
        else:
            print(f"Warning: Patrol '{patrol_name}' not found in patrol data.")

if __name__ == "__main__":
    main()

