# scout_tracking
Some python tools to support Patrol Leaders in tracking advancement signoffs for Scouts in their Patrol.

Collectively, these scripts process a Scoutbook data export to produce an advancement chart for each Patrol in a Troop.

# Scoutbook export cleaner
`clean_advancement.py` - load the CSV file produced by Scoutbook's backup functionality, and clean records not related to Scout Advancement work.

You can run it from the command line like: 
`python clean_advancement.py input_file output_file'

# Scout Advancement Report Generator
`generate_report.py` - load the advancement info, list of patrols, and list of requirements, process them to produce an advancement report for each patrol, along with a report for any scouts not connected to patrols, or any requirements from the report that aren't included in the list of requirements.

You can run it from the command line like:
'python generate_report.py advancement.tsv patrols.tsv requirements.tsv ./reports'

# requirements.tsv
a list of advancement requirements through first class rank (as of 2025)

# patrols_example.tsv
an example roster of a pretend Troop

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The original code was generated with the assistance of ChatGPT (OpenAI). Thanks to OpenAI for providing the language model that assisted in creating this code.

