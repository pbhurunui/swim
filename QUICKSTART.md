# Swimming Tournament Management System - Quick Start Guide

## What You Can Do

This application helps you manage swimming tournaments with these capabilities:

### 1. Athlete Management
- Add individual athletes with ID, name, birth date, and gender
- Edit athlete information
- Delete athletes
- View detailed athlete profiles with their records
- Import multiple athletes from CSV files

### 2. Age Group Management
- Create age groups (e.g., "10-12 Years", "13-15 Years")
- Set age ranges for each group
- Optionally restrict groups by gender
- Edit or delete age groups

### 3. Automatic Age Assignment
- Specify a reference date (e.g., tournament date)
- System automatically calculates each athlete's age on that date
- Athletes are assigned to appropriate age groups

### 4. Record Tracking
- Enter swimming records with:
  - Event name
  - Stroke type (Freestyle, Backstroke, Breaststroke, Butterfly, Individual Medley)
  - Distance (in meters)
  - Time (automatically formatted as MM:SS.ms)
  - Date
- Edit or delete records
- View records for specific athletes

### 5. Statistics
- View total events per athlete
- See personal best times for each event type
- Calculate average times across all events

## Quick Example Workflow

1. **Start the application:**
   ```bash
   python tournament_app.py
   ```

2. **Import sample athletes:**
   ```
   > import
   Enter CSV file path: sample_athletes.csv
   ✓ Imported 10 athletes
   ```

3. **Create age groups:**
   ```
   > agegroup
   Choose: 1
   Name: 10-12 Years
   Min age: 10
   Max age: 12
   Gender: [leave blank for both]
   ```

4. **Assign athletes to age groups:**
   ```
   > assign
   Reference date: 2024-01-01
   ✓ Age groups assigned successfully!
   ```

5. **Add a swimming record:**
   ```
   > record
   Choose: 1
   Record ID: R001
   Athlete ID: A001
   Event name: 100m Freestyle Final
   Stroke: 1 (Freestyle)
   Distance: 100
   Time: 65.45
   Date: 2024-01-15
   ✓ Record added successfully! Time: 01:05.45
   ```

6. **View athlete statistics:**
   ```
   > stats
   Enter athlete ID: A001
   
   --- Statistics for Emma Wilson ---
   Total Events: 2
   
   Personal Bests:
     100m Freestyle: 01:05.45
     50m Freestyle: 00:32.18
   
   Average Time: 00:48.81
   ```

## Sample Athletes Included

The repository includes `sample_athletes.csv` with 10 pre-configured athletes:
- Emma Wilson (F, born 2008-05-15)
- Noah Johnson (M, born 2007-11-22)
- Olivia Brown (F, born 2009-03-10)
- Liam Davis (M, born 2006-08-30)
- Ava Martinez (F, born 2010-01-18)
- Ethan Garcia (M, born 2008-12-05)
- Sophia Rodriguez (F, born 2007-06-25)
- Mason Miller (M, born 2009-09-14)
- Isabella Anderson (F, born 2006-04-03)
- Lucas Taylor (M, born 2010-07-28)

## Data Persistence

All data is automatically saved to `tournament_data.json` in the application directory. The data persists between sessions, so you can close and reopen the application without losing your work.

## Tips

- Use unique IDs for athletes and records (e.g., A001, A002, R001, R002)
- Set up age groups before assigning athletes
- The reference date for age assignment is typically the start date of the tournament
- You can filter records by athlete when listing them
- CSV imports validate data and report errors for invalid rows

## Getting Help

Type `help` at any time to see available commands.

For detailed documentation, see the main README.md file.
