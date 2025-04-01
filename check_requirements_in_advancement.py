import csv
import argparse

# Load requirements data
def load_requirements(filename):
    requirements = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            requirement, alternative_text = row
            requirement = requirement.strip().lower()  # Normalize to lowercase
            alternative_text = alternative_text.strip().lower()  # Normalize to lowercase
            requirements[requirement] = alternative_text
    return requirements

# Load advancement data
def load_advancement_data(filename):
    advancement_data = set()  # Using a set to eliminate duplicates
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:
                continue
            _, requirement, _ = row
            requirement = requirement.strip().lower()  # Normalize to lowercase
            advancement_data.add(requirement)  # Add the requirement (duplicates will be ignored)
    return advancement_data

# Check for requirements in advancement data that are not in the requirements list
def check_requirements_not_in_requirements(advancement_data, requirements):
    missing_requirements = set()

    # Check each requirement in the advancement data
    for requirement in advancement_data:
        # If requirement is not found in either the requirement name or its alternative
        if requirement not in requirements and requirement not in requirements.values():
            missing_requirements.add(requirement)
    
    return missing_requirements

# Main function to parse arguments and check for errors
def main():
    parser = argparse.ArgumentParser(description="Check for requirements in advancement.csv that are not in requirements.tsv.")
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    
    args = parser.parse_args()

    # Load the data
    advancement_data = load_advancement_data(args.advancement_file)
    requirements = load_requirements(args.requirements_file)

    # Check for requirements not in the requirements list
    requirements_not_in_list = check_requirements_not_in_requirements(advancement_data, requirements)

    if requirements_not_in_list:
        print("Requirements in advancement.csv not found in requirements.tsv:")
        for requirement in requirements_not_in_list:
            print(requirement)
    else:
        print("All requirements in advancement.csv are listed in requirements.tsv.")

if __name__ == "__main__":
    main()

