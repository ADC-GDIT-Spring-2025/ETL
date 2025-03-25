# ETL Project

This project processes email data from the Enron dataset using a custom ETL (Extract, Transform, Load) pipeline and provides a Flask API for querying the processed data.

## Project Overview

The ETL project parses email data from the Enron Maildir dataset, extracting relevant information and preparing it for analysis. The parser handles email metadata, recipients, and content. A Flask API is provided to query and analyze the processed data.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)
- Virtual environment (recommended)

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

### Data Setup

Run the ETL pipeline setup script to download and process the Enron dataset:
```bash
chmod +x setup_etl.sh
./setup_etl.sh
```

This script will:
1. Download the Enron email dataset (~423MB)
2. Extract the dataset (~1.7GB when extracted)
3. Parse all emails and generate JSON files in the user_data directory

## Running the Flask API

1. Ensure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### API Endpoints

The API provides the following endpoints:

- `GET /` - Basic health check endpoint

- `GET /messages` - Get all email messages from the dataset
  - Returns the contents of messages.json which contains all parsed email data

- `GET /users` - Get all users from the dataset
  - Returns the contents of users.json which maps user email addresses to unique IDs

- `GET /threads` - Get all email threads
  - Returns the contents of threads.json which maps thread subjects to unique IDs

- `GET /user-threads` - Get mapping of users to their email threads
  - Returns the contents of user_threads.json which shows which threads each user participated in

- `GET /thread-users` - Get mapping of threads to their participating users
  - Returns the contents of thread_users.json which shows which users participated in each thread

Example API calls:
```bash
# Get all messages
curl http://localhost:5000/messages

# Get all users
curl http://localhost:5000/users

# Get all threads
curl http://localhost:5000/threads

# Get user-thread mappings
curl http://localhost:5000/user-threads

# Get thread-user mappings
curl http://localhost:5000/thread-users
```

## Project Structure

```
ETL/
├── app.py              # Flask API application
├── data/               # Directory for email data
│   └── maildir/        # Extracted Enron dataset
├── util/               # Utility modules
│   ├── parser.py       # Email parsing functionality
│   └── fetch_data.py   # Dataset download script
├── user_data/          # Processed JSON files
├── setup_venv.sh       # Virtual environment setup script
├── setup_etl.sh        # ETL pipeline setup script
└── README.md           # This documentation
```

## Development

To modify the API or add new features:
1. Make your changes to the relevant files
2. Test your changes locally
3. Update the documentation if you've added new endpoints or features

## Troubleshooting

1. If the API fails to start:
   - Check that all JSON files exist in the user_data directory
   - Ensure you're in the virtual environment
   - Verify that Flask is installed (`pip install flask`)

2. If data isn't loading:
   - Run `setup_etl.sh` again to regenerate the JSON files
   - Check the user_data directory for valid JSON files

## Deactivating the Environment

When you're done working with the project, deactivate the virtual environment:
```bash
deactivate
```

## License

[Add your license information here]

## Contact

[Add your contact information here]
