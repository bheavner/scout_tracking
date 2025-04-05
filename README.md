# scout_tracking
This project helps to generate reports and perform quality checks for scout advancement data, patrol membership, and requirements. It includes several scripts that can be run from the command line.

Collectively, these scripts process a Scoutbook data export to produce an advancement chart for each Patrol in a Troop.

This README describes:
- [Installation](#Installation)
- [CLI Commands and Usage](#CLI-Commands-and-Usage)
- [License](#License)
- [Attribution](#Attribution)

## Installation
This is a python module. You can clone the repo to your local environment, `cd` to the directory with `setup.py` in it, and use `pip install .`

## CLI Commands and Usage

### **clean_advancement.py**
**Purpose**: Process the Scoutbook export/backup file to prepare it for subsequent report generation work. This script removes extra fields and records not related to Scout Advancement Work (for example, Cub Scout Awards).

**Usage**:
```
python clean_advancement.py <input_file> <output_file>
```

**Arguments**:
- `input_file`: Path to the advancement data backup file downloaded from Scoutbook (CSV format).
- `output_file`: Path and name for the output file (CSV format).

**Example**:
```
python clean_advancement.py troop_100__advancement.csv advancement.csv
```

**Example Input**:
`troop100__advancement.csv`
```
"BSA Member ID","First Name","Middle Name","Last Name","Advancement Type","Advancement","Version","Date Completed","Approved","Awarded","MarkedCompletedBy","MarkedCompletedDate","CounselorApprovedBy","CounselorApprovedDate","LeaderApprovedBy","LeaderApprovedDate","AwardedBy","AwardedDate"
12600561,"Frank","A","Jones","Scout Rank Requirement","2b",2022,"7/19/2024",1,,ASM_Bill,8/6/2024,,,SM_Mary,8/27/2024,,
```

**Example Output**:
A CSV file containing slected information from the Scoutbook backup, formatted for input to subsequent report and QC scripts included in this repository.

`advancement.csv`
```
Scout Name,Requirement,Completion Date
Frank Jones,Scout Rank Requirement 2b,7/19/2024
```

---
### `main.py`

**Purpose**: Generate one or more patrol reports summarizing the advancement progress of each scout in each patrols.

**Usage**:
```
python main.py <patrols_file> <requirements_file> <advancement_file> <output_dir> [<patrol_name>]
```

**Arguments**:
- `patrols_file`: Path to the patrol membership file (TSV format).
- `requirements_file`: Path to the requirements list file (TSV format).
- `advancement_file`: Path to the advancement data file (CSV format).
- `output_dir`: Directory where the reports will be saved.
- `patrol_name`: Optional patrol name to generate report for a specific patrol (default is all patrols).

**Example**:
```
python generate_report.py scout_tracking/patrols.tsv scout_tracking/requirements.tsv scout_tracking/advancement.csv ./reports Lions
```

**Example Inputs**:
advancement.csv`
```
Scout Name,Requirement,Completion Date
Frank Jones,Scout Rank Requirement 2b,7/19/2024
John Doe,Scout Rank Requirement 3a,7/19/2024
Jane Smith,First Class Rank Requirement 4,8/1/2024
John Doe,Tenderfoot Rank Requirement 1a,8/8/2024
Alice Brown,Scout Rank Requirement 1a,8/1/2024
Bob Green,Second Class Rank Requirement 2g,8/1/2024
Bob Green,Tenderfoot Rank Requirement 1a,8/1/2024
```

`patrols.tsv`
```
Scout Name    Patrol
Frank Jones   Ninjas
Jane Smith    Lions
Bob Green     Lions
John Doe      Tigers
Alice Brown   Tigers
```

`requirements.tsv`
```
Requirement Name        Alternative Text
Scout Rank Requirement 2b              2nd 2b
Tenderfoot Rank Requirement 1a                Tenderfoot 1a
```

**Example Outputs**:
A TSV report for the specified patrol, showing each scout and their completion status for each requirement.

`lion_report.csv``
```
Requirement        Jane Smith   Bob Green
Basic First Aid     ✔           ✔
Camping Skills                  ✔
```

`tiger_report.csv``
```
Requirement        John Doe    Alice Brown
Basic First Aid     ✔           ✔
Camping Skills      ✔
```

`additional_report.txt`
```
Scouts not in Patrols:
bob green

Requirements not in requirements list:
Emergency Preparedness
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Attribution

The original code was generated with the assistance of ChatGPT (OpenAI). Thanks to OpenAI for providing the language model that assisted in creating this code.
