"""
Data manager for persisting and managing tournament data.
"""
import json
import os
from datetime import date, datetime
from typing import List, Optional, Dict
from models import Athlete, AgeGroup, Record, AthleteStatistics, Gender, StrokeType


class DataManager:
    """Manages data persistence for the tournament application."""
    
    def __init__(self, data_file: str = "tournament_data.json"):
        """Initialize the data manager."""
        self.data_file = data_file
        self.athletes: Dict[str, Athlete] = {}
        self.age_groups: Dict[str, AgeGroup] = {}
        self.records: Dict[str, Record] = {}
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load athletes
                for athlete_data in data.get('athletes', []):
                    athlete = Athlete(**athlete_data)
                    self.athletes[athlete.id] = athlete
                
                # Load age groups
                for ag_data in data.get('age_groups', []):
                    age_group = AgeGroup(**ag_data)
                    self.age_groups[age_group.name] = age_group
                
                # Load records
                for record_data in data.get('records', []):
                    record = Record(**record_data)
                    self.records[record.id] = record
                    
            except Exception as e:
                print(f"Warning: Could not load data from {self.data_file}: {e}")
    
    def save_data(self):
        """Save data to JSON file."""
        data = {
            'athletes': [athlete.to_dict() for athlete in self.athletes.values()],
            'age_groups': [ag.to_dict() for ag in self.age_groups.values()],
            'records': [record.to_dict() for record in self.records.values()]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Athlete CRUD operations
    def add_athlete(self, athlete: Athlete) -> bool:
        """Add a new athlete."""
        if athlete.id in self.athletes:
            return False
        self.athletes[athlete.id] = athlete
        self.save_data()
        return True
    
    def get_athlete(self, athlete_id: str) -> Optional[Athlete]:
        """Get an athlete by ID."""
        return self.athletes.get(athlete_id)
    
    def update_athlete(self, athlete: Athlete) -> bool:
        """Update an existing athlete."""
        if athlete.id not in self.athletes:
            return False
        self.athletes[athlete.id] = athlete
        self.save_data()
        return True
    
    def delete_athlete(self, athlete_id: str) -> bool:
        """Delete an athlete."""
        if athlete_id not in self.athletes:
            return False
        del self.athletes[athlete_id]
        # Also delete associated records
        records_to_delete = [rid for rid, record in self.records.items() 
                            if record.athlete_id == athlete_id]
        for rid in records_to_delete:
            del self.records[rid]
        self.save_data()
        return True
    
    def list_athletes(self) -> List[Athlete]:
        """List all athletes."""
        return list(self.athletes.values())
    
    # Age Group CRUD operations
    def add_age_group(self, age_group: AgeGroup) -> bool:
        """Add a new age group."""
        if age_group.name in self.age_groups:
            return False
        self.age_groups[age_group.name] = age_group
        self.save_data()
        return True
    
    def get_age_group(self, name: str) -> Optional[AgeGroup]:
        """Get an age group by name."""
        return self.age_groups.get(name)
    
    def update_age_group(self, age_group: AgeGroup) -> bool:
        """Update an existing age group."""
        if age_group.name not in self.age_groups:
            return False
        self.age_groups[age_group.name] = age_group
        self.save_data()
        return True
    
    def delete_age_group(self, name: str) -> bool:
        """Delete an age group."""
        if name not in self.age_groups:
            return False
        del self.age_groups[name]
        # Remove age group assignments from athletes
        for athlete in self.athletes.values():
            if athlete.age_group == name:
                athlete.age_group = None
        self.save_data()
        return True
    
    def list_age_groups(self) -> List[AgeGroup]:
        """List all age groups."""
        return list(self.age_groups.values())
    
    # Record CRUD operations
    def add_record(self, record: Record) -> bool:
        """Add a new record."""
        if record.id in self.records:
            return False
        self.records[record.id] = record
        self.save_data()
        return True
    
    def get_record(self, record_id: str) -> Optional[Record]:
        """Get a record by ID."""
        return self.records.get(record_id)
    
    def update_record(self, record: Record) -> bool:
        """Update an existing record."""
        if record.id not in self.records:
            return False
        self.records[record.id] = record
        self.save_data()
        return True
    
    def delete_record(self, record_id: str) -> bool:
        """Delete a record."""
        if record_id not in self.records:
            return False
        del self.records[record_id]
        self.save_data()
        return True
    
    def list_records(self, athlete_id: Optional[str] = None) -> List[Record]:
        """List all records, optionally filtered by athlete."""
        records = list(self.records.values())
        if athlete_id:
            records = [r for r in records if r.athlete_id == athlete_id]
        return records
    
    # Age group assignment
    def assign_age_groups(self, reference_date: date):
        """Assign athletes to age groups based on a reference date."""
        for athlete in self.athletes.values():
            age = athlete.calculate_age(reference_date)
            assigned = False
            
            # Find matching age group
            for age_group in self.age_groups.values():
                # Check if gender matches (if age group has gender requirement)
                if age_group.gender and age_group.gender != athlete.gender:
                    continue
                
                # Check if age falls in range
                if age_group.contains_age(age):
                    athlete.age_group = age_group.name
                    assigned = True
                    break
            
            if not assigned:
                athlete.age_group = None
        
        self.save_data()
    
    # Statistics
    def get_athlete_statistics(self, athlete_id: str) -> Optional[AthleteStatistics]:
        """Calculate statistics for an athlete."""
        if athlete_id not in self.athletes:
            return None
        
        athlete_records = self.list_records(athlete_id)
        if not athlete_records:
            return AthleteStatistics(athlete_id=athlete_id)
        
        stats = AthleteStatistics(
            athlete_id=athlete_id,
            total_events=len(athlete_records)
        )
        
        # Calculate personal bests for each event type
        event_times: Dict[str, List[float]] = {}
        for record in athlete_records:
            event_key = f"{record.distance}m {record.stroke.value}"
            if event_key not in event_times:
                event_times[event_key] = []
            event_times[event_key].append(record.time_seconds)
        
        # Get best (minimum) time for each event
        for event_key, times in event_times.items():
            stats.personal_bests[event_key] = min(times)
        
        # Calculate average time across all events
        all_times = [r.time_seconds for r in athlete_records]
        stats.average_time = sum(all_times) / len(all_times) if all_times else None
        
        return stats
    
    # Import functionality
    def import_athletes_from_csv(self, file_path: str) -> tuple[int, List[str]]:
        """
        Import athletes from a CSV file.
        Returns: (number_imported, list_of_errors)
        """
        import csv
        
        imported = 0
        errors = []
        
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        athlete = Athlete(
                            id=row['id'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            date_of_birth=row['date_of_birth'],
                            gender=row['gender']
                        )
                        if self.add_athlete(athlete):
                            imported += 1
                        else:
                            errors.append(f"Row {row_num}: Athlete ID {row['id']} already exists")
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
        except Exception as e:
            errors.append(f"File error: {str(e)}")
        
        return imported, errors
