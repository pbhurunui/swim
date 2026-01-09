# Swimming Tournament Management System

A comprehensive application for managing swimming tournaments, including athlete management, age group assignments, record tracking, and statistics.

## Features

- **Athlete Management**: Add, edit, delete, and view athlete information
- **Age Group Management**: Create and manage age groups with customizable age ranges
- **Automatic Age Assignment**: Automatically assign athletes to age groups based on a reference date
- **Record Tracking**: Enter and manage swimming records with stroke types and distances
- **Statistics**: View athlete performance statistics including personal bests and averages
- **Import Functionality**: Bulk import athletes from CSV files
- **Data Persistence**: All data is saved automatically to JSON format

## Installation

### Requirements

- Python 3.7 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pbhurunui/swim.git
cd swim
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the application with:
```bash
python tournament_app.py
```

### Main Commands

Once the application is running, you can use the following commands:

- `help` - Show available commands
- `athlete` - Manage athletes
- `agegroup` - Manage age groups
- `record` - Manage records
- `import` - Import athletes from CSV
- `assign` - Assign athletes to age groups
- `stats` - View athlete statistics
- `exit` - Exit the application

### Athlete Management

1. **Add an Athlete**
   - Select `athlete` → Option 1
   - Enter athlete details (ID, name, date of birth, gender)

2. **List Athletes**
   - Select `athlete` → Option 2
   - View all registered athletes with their age group assignments

3. **Edit an Athlete**
   - Select `athlete` → Option 3
   - Enter athlete ID and update desired fields

4. **Delete an Athlete**
   - Select `athlete` → Option 4
   - Enter athlete ID and confirm deletion

### Age Group Management

1. **Add an Age Group**
   - Select `agegroup` → Option 1
   - Enter name, age range (min/max), and optional gender restriction

2. **List Age Groups**
   - Select `agegroup` → Option 2
   - View all configured age groups

3. **Edit/Delete Age Groups**
   - Use options 3 and 4 in the age group menu

### Assigning Age Groups

To automatically assign athletes to age groups:

1. Select `assign` from the main menu
2. Enter a reference date (format: YYYY-MM-DD)
3. The system will calculate each athlete's age on that date and assign them to appropriate age groups

### Record Management

1. **Add a Record**
   - Select `record` → Option 1
   - Enter record details including athlete ID, event, stroke, distance, time, and date

2. **List Records**
   - Select `record` → Option 2
   - Optionally filter by athlete ID

3. **Edit/Delete Records**
   - Use options 3 and 4 in the record menu

### Importing Athletes

1. Prepare a CSV file with the following format:
   ```csv
   id,first_name,last_name,date_of_birth,gender
   A001,John,Smith,2005-03-15,M
   A002,Jane,Doe,2006-08-22,F
   ```

2. Select `import` from the main menu
3. Enter the path to your CSV file
4. The system will import all valid athletes and report any errors

A sample CSV file (`sample_athletes.csv`) is included with 10 example athletes.

### Viewing Statistics

1. Select `stats` from the main menu
2. Enter an athlete ID
3. View total events, personal bests for each event type, and average time

## Data Storage

All data is automatically saved to `tournament_data.json` in the application directory. This file contains:
- All registered athletes
- Age group configurations
- Swimming records

The file is updated automatically after each change.

## Running Tests

Run the test suite with:
```bash
python -m unittest test_tournament.py
```

Or run tests with verbose output:
```bash
python -m unittest test_tournament.py -v
```

## Example Workflow

1. **Initial Setup**
   ```
   > agegroup
   Choose: 1
   Add age groups (e.g., "10-12 Years", min: 10, max: 12)
   ```

2. **Import Athletes**
   ```
   > import
   Enter CSV file path: sample_athletes.csv
   ```

3. **Assign Age Groups**
   ```
   > assign
   Reference date: 2024-01-01
   ```

4. **Add Records**
   ```
   > record
   Choose: 1
   Enter record details for competitions
   ```

5. **View Statistics**
   ```
   > stats
   Enter athlete ID: A001
   ```

## Project Structure

```
swim/
├── tournament_app.py      # Main CLI application
├── models.py              # Data models (Athlete, AgeGroup, Record)
├── data_manager.py        # Data persistence and CRUD operations
├── test_tournament.py     # Unit tests
├── sample_athletes.csv    # Sample data for testing
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Data Models

### Athlete
- ID (unique identifier)
- First name
- Last name
- Date of birth
- Gender (M/F)
- Age group (assigned automatically)

### Age Group
- Name
- Minimum age
- Maximum age
- Gender (optional - if not specified, applies to all genders)

### Record
- ID (unique identifier)
- Athlete ID
- Event name
- Stroke type (Freestyle, Backstroke, Breaststroke, Butterfly, Individual Medley)
- Distance (in meters)
- Time (in seconds)
- Date

## Contributing

This is a basic implementation that can be extended with:
- Web interface
- Database backend (PostgreSQL, MySQL)
- Export functionality (PDF reports, Excel)
- Advanced statistics and analytics
- Multi-tournament support
- Team management

## License

This project is open source and available for use and modification.
