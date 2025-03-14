# EmailMiner.ai ETL Pipeline

This project processes email data from the Enron dataset using a custom ETL (Extract, Transform, Load) pipeline.

## Project Overview

The ETL project parses email data from the Enron Maildir dataset, extracting relevant information and preparing it for analysis. The parser handles email metadata, recipients, and content.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ETL.git
   cd ETL
   ```

2. Set up a virtual environment:
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```
   
   This script will:
   - Create a Python virtual environment
   - Activate the environment
   - Install required dependencies (if requirements.txt exists)

3. If you need to manually activate the virtual environment later:
   ```bash
   source venv/bin/activate
   ```

## Project Structure

```
ETL/
├── data/               # Directory for email data
│   └── maildir/        # All users and respective emails
│   └── data.tar.gz     # Compressed Enron dataset
├── util/               # Utility modules
│   └── fetch_data.py   # Creating dataset from Enron tarball
│   └── parser.py       # Email parsing functionality
├── main.py             # Main application entry point
├── setup_venv.sh       # Virtual environment setup script
└── README.md           # This documentation
```

## Usage

1. Ensure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Create the data folder and then run the fetching script to get data:
   ```bash
   cd util
   mkdir data
   python fetch_data.py
   ```

3. Create the user_data folder and then run the parser to generate the 5 json files:
   parser.py takes in the directory for the database and the number of emails to parse as cmd line args.
   ```bash
   mkdir user_data
   python parser.py data/maildir <num_emails_to_parse>
   ```

4. The script will process the emails and output parsing statistics.

5. To upload the parsed data to neo4j, start the neo4j database in the desktop app and run neo4j_uploader.py
   ```bash
   cd neo4j
   python neo4j_uploader.py <max_emails> <max_users>
   ```

6. To view all nodes and relationships in the neo4j browser run the following cypher commands:
   ```bash
   MATCH (n) RETURN n;
   ```
   To remove all nodes and relationships in the neo4j browser run:
   ```bash
   MATCH (n) DETACH DELETE n;
   ```

## Customization

WARNING: `main.py` is currently deprecated
You can modify the `main.py` file to:
- Change the input data directories
- Adjust the maximum number of emails to process
- Customize the output format

## Deactivating the Environment

When you're done working with the project, deactivate the virtual environment:
```bash
deactivate
```

