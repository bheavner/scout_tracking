import pandas as pd
import argparse

# Function to clean the CSV file
def clean_csv(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # List of values to remove in the 'Advancement' column
    advancement_remove_values = [
        'Bobcat', 'Tiger', 'Wolf', 'Bear', 'Webelos', 
        'Arrow of Light', 'Venturing', 'Discovery', 
        'Pathfinder', 'Summit', 'Lion'
    ]

    # List of values for which 'Advancement Type' column should be checked to start with
    advancement_type_remove_prefixes = [
        'Venturing', 'Discovery', 'Pathfinder', 
        'Summit', 'Merit', 'Award', 'Webelos',
        'Arrow of Light', 'Apprentice', 'Adventure',
        'Tiger', 'Bear', 'Bobcat', 'Academics & Sports',
        'Wolf', 'Lion'
    ]

    # Remove rows where 'Advancement' column contains any of the listed values
    df = df[~df['Advancement'].isin(advancement_remove_values)]

    # Remove rows where 'Advancement Type' column starts with any of the listed prefixes
    df = df[~df['Advancement Type'].str.startswith(tuple(advancement_type_remove_prefixes))]

    # List of columns to drop
    columns_to_drop = [
        'BSA Member ID', 'Version', 'Awarded', 'MarkedCompletedBy',
        'MarkedCompletedDate', 'CounselorApprovedBy', 'CounselorApprovedDate',
        'LeaderApprovedBy', 'LeaderApprovedDate', 'AwardedBy', 'AwardedDate',
        'Middle Name'  # Drop 'Middle Name' as it's not needed
    ]

    # Drop the unnecessary columns
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Merge the 'First Name' and 'Last Name' columns, ensuring no NaN values are present
    df['Name'] = df['First Name'].fillna('') + (' ' + df['Last Name'].fillna('')) 

    # Merge the 'Advancement Type' and 'Advancement' columns, ensuring no NaN values are present
    df['Advancement Info'] = df['Advancement Type'].fillna('') + (' ' + df['Advancement'].fillna(''))

    # Keep only the desired columns in the output
    df = df[['Name', 'Advancement Info', 'Date Completed']]

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Cleaning complete! The cleaned file is saved as '{output_file}'.")

# Main function to handle CLI arguments
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Clean a CSV file by removing specific rows based on 'Advancement' and 'Advancement Type' columns.")
    parser.add_argument('input_file', help="Path to the input CSV file")
    parser.add_argument('output_file', help="Path to save the cleaned CSV file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to clean the CSV file
    clean_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()

