"""
Command-line interface for the Swimming Tournament Application.
"""
import sys
from datetime import date, datetime
from typing import Optional
from models import Athlete, AgeGroup, Record, Gender, StrokeType
from data_manager import DataManager


class TournamentCLI:
    """Command-line interface for tournament management."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.data_manager = DataManager()
        self.commands = {
            'help': self.show_help,
            'athlete': self.athlete_menu,
            'agegroup': self.age_group_menu,
            'record': self.record_menu,
            'import': self.import_menu,
            'assign': self.assign_age_groups,
            'stats': self.show_statistics,
            'exit': self.exit_app
        }
    
    def run(self):
        """Run the CLI main loop."""
        print("=" * 60)
        print("Swimming Tournament Management System")
        print("=" * 60)
        print("Type 'help' for available commands\n")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                if not command:
                    continue
                
                cmd_parts = command.split(maxsplit=1)
                cmd = cmd_parts[0]
                
                if cmd in self.commands:
                    self.commands[cmd]()
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help information."""
        print("\nAvailable commands:")
        print("  help      - Show this help message")
        print("  athlete   - Manage athletes (add, list, edit, delete)")
        print("  agegroup  - Manage age groups (add, list, edit, delete)")
        print("  record    - Manage records (add, list, edit, delete)")
        print("  import    - Import athletes from CSV file")
        print("  assign    - Assign athletes to age groups")
        print("  stats     - View athlete statistics")
        print("  exit      - Exit the application")
    
    def athlete_menu(self):
        """Athlete management menu."""
        print("\n--- Athlete Management ---")
        print("1. Add athlete")
        print("2. List athletes")
        print("3. Edit athlete")
        print("4. Delete athlete")
        print("5. View athlete details")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            self.add_athlete()
        elif choice == '2':
            self.list_athletes()
        elif choice == '3':
            self.edit_athlete()
        elif choice == '4':
            self.delete_athlete()
        elif choice == '5':
            self.view_athlete()
    
    def add_athlete(self):
        """Add a new athlete."""
        print("\n--- Add New Athlete ---")
        try:
            athlete_id = input("Athlete ID: ").strip()
            if not athlete_id:
                print("Error: ID cannot be empty")
                return
            
            if self.data_manager.get_athlete(athlete_id):
                print(f"Error: Athlete with ID {athlete_id} already exists")
                return
            
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            dob_str = input("Date of birth (YYYY-MM-DD): ").strip()
            gender_str = input("Gender (M/F): ").strip().upper()
            
            # Validate inputs
            if not all([first_name, last_name, dob_str, gender_str]):
                print("Error: All fields are required")
                return
            
            if gender_str not in ['M', 'F']:
                print("Error: Gender must be M or F")
                return
            
            # Create athlete
            athlete = Athlete(
                id=athlete_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob_str,
                gender=gender_str
            )
            
            if self.data_manager.add_athlete(athlete):
                print(f"✓ Athlete {first_name} {last_name} added successfully!")
            else:
                print("Error: Could not add athlete")
        except Exception as e:
            print(f"Error: {e}")
    
    def list_athletes(self):
        """List all athletes."""
        athletes = self.data_manager.list_athletes()
        if not athletes:
            print("\nNo athletes found.")
            return
        
        print(f"\n--- Athletes ({len(athletes)}) ---")
        print(f"{'ID':<10} {'Name':<30} {'DOB':<12} {'Gender':<8} {'Age Group':<15}")
        print("-" * 85)
        for athlete in sorted(athletes, key=lambda a: (a.last_name, a.first_name)):
            name = f"{athlete.first_name} {athlete.last_name}"
            print(f"{athlete.id:<10} {name:<30} {athlete.date_of_birth} {athlete.gender.value:<8} {athlete.age_group or 'Unassigned':<15}")
    
    def edit_athlete(self):
        """Edit an existing athlete."""
        athlete_id = input("\nEnter athlete ID to edit: ").strip()
        athlete = self.data_manager.get_athlete(athlete_id)
        
        if not athlete:
            print(f"Error: Athlete with ID {athlete_id} not found")
            return
        
        print(f"\nEditing: {athlete.first_name} {athlete.last_name}")
        print("(Press Enter to keep current value)")
        
        first_name = input(f"First name [{athlete.first_name}]: ").strip() or athlete.first_name
        last_name = input(f"Last name [{athlete.last_name}]: ").strip() or athlete.last_name
        dob_str = input(f"Date of birth [{athlete.date_of_birth}]: ").strip()
        gender_str = input(f"Gender [{athlete.gender.value}]: ").strip().upper()
        
        # Update athlete
        athlete.first_name = first_name
        athlete.last_name = last_name
        if dob_str:
            athlete.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
        if gender_str:
            athlete.gender = Gender(gender_str)
        
        if self.data_manager.update_athlete(athlete):
            print("✓ Athlete updated successfully!")
        else:
            print("Error: Could not update athlete")
    
    def delete_athlete(self):
        """Delete an athlete."""
        athlete_id = input("\nEnter athlete ID to delete: ").strip()
        athlete = self.data_manager.get_athlete(athlete_id)
        
        if not athlete:
            print(f"Error: Athlete with ID {athlete_id} not found")
            return
        
        confirm = input(f"Delete {athlete.first_name} {athlete.last_name}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if self.data_manager.delete_athlete(athlete_id):
                print("✓ Athlete deleted successfully!")
            else:
                print("Error: Could not delete athlete")
    
    def view_athlete(self):
        """View detailed athlete information."""
        athlete_id = input("\nEnter athlete ID: ").strip()
        athlete = self.data_manager.get_athlete(athlete_id)
        
        if not athlete:
            print(f"Error: Athlete with ID {athlete_id} not found")
            return
        
        print(f"\n--- Athlete Details ---")
        print(f"ID: {athlete.id}")
        print(f"Name: {athlete.first_name} {athlete.last_name}")
        print(f"Date of Birth: {athlete.date_of_birth}")
        print(f"Gender: {athlete.gender.value}")
        print(f"Age Group: {athlete.age_group or 'Unassigned'}")
        
        # Show records
        records = self.data_manager.list_records(athlete_id)
        if records:
            print(f"\nRecords ({len(records)}):")
            for record in sorted(records, key=lambda r: r.date, reverse=True):
                print(f"  {record.date} - {record.distance}m {record.stroke.value}: {record.format_time()}")
    
    def age_group_menu(self):
        """Age group management menu."""
        print("\n--- Age Group Management ---")
        print("1. Add age group")
        print("2. List age groups")
        print("3. Edit age group")
        print("4. Delete age group")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            self.add_age_group()
        elif choice == '2':
            self.list_age_groups()
        elif choice == '3':
            self.edit_age_group()
        elif choice == '4':
            self.delete_age_group()
    
    def add_age_group(self):
        """Add a new age group."""
        print("\n--- Add New Age Group ---")
        try:
            name = input("Age group name: ").strip()
            if not name:
                print("Error: Name cannot be empty")
                return
            
            if self.data_manager.get_age_group(name):
                print(f"Error: Age group '{name}' already exists")
                return
            
            min_age = int(input("Minimum age: ").strip())
            max_age = int(input("Maximum age: ").strip())
            gender_str = input("Gender (M/F/blank for both): ").strip().upper()
            
            if gender_str and gender_str not in ['M', 'F']:
                print("Error: Gender must be M, F, or blank")
                return
            
            age_group = AgeGroup(
                name=name,
                min_age=min_age,
                max_age=max_age,
                gender=gender_str if gender_str else None
            )
            
            if self.data_manager.add_age_group(age_group):
                print(f"✓ Age group '{name}' added successfully!")
            else:
                print("Error: Could not add age group")
        except ValueError:
            print("Error: Invalid age value")
        except Exception as e:
            print(f"Error: {e}")
    
    def list_age_groups(self):
        """List all age groups."""
        age_groups = self.data_manager.list_age_groups()
        if not age_groups:
            print("\nNo age groups found.")
            return
        
        print(f"\n--- Age Groups ({len(age_groups)}) ---")
        print(f"{'Name':<20} {'Age Range':<15} {'Gender':<10}")
        print("-" * 50)
        for ag in sorted(age_groups, key=lambda x: x.min_age):
            age_range = f"{ag.min_age}-{ag.max_age}"
            gender = ag.gender.value if ag.gender else "Both"
            print(f"{ag.name:<20} {age_range:<15} {gender:<10}")
    
    def edit_age_group(self):
        """Edit an existing age group."""
        name = input("\nEnter age group name to edit: ").strip()
        age_group = self.data_manager.get_age_group(name)
        
        if not age_group:
            print(f"Error: Age group '{name}' not found")
            return
        
        print(f"\nEditing: {age_group.name}")
        print("(Press Enter to keep current value)")
        
        try:
            min_age_str = input(f"Minimum age [{age_group.min_age}]: ").strip()
            max_age_str = input(f"Maximum age [{age_group.max_age}]: ").strip()
            gender_str = input(f"Gender [{age_group.gender.value if age_group.gender else 'Both'}]: ").strip().upper()
            
            if min_age_str:
                age_group.min_age = int(min_age_str)
            if max_age_str:
                age_group.max_age = int(max_age_str)
            if gender_str:
                age_group.gender = Gender(gender_str) if gender_str not in ['BOTH', 'B', ''] else None
            
            if self.data_manager.update_age_group(age_group):
                print("✓ Age group updated successfully!")
            else:
                print("Error: Could not update age group")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_age_group(self):
        """Delete an age group."""
        name = input("\nEnter age group name to delete: ").strip()
        age_group = self.data_manager.get_age_group(name)
        
        if not age_group:
            print(f"Error: Age group '{name}' not found")
            return
        
        confirm = input(f"Delete age group '{name}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if self.data_manager.delete_age_group(name):
                print("✓ Age group deleted successfully!")
            else:
                print("Error: Could not delete age group")
    
    def record_menu(self):
        """Record management menu."""
        print("\n--- Record Management ---")
        print("1. Add record")
        print("2. List records")
        print("3. Edit record")
        print("4. Delete record")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            self.add_record()
        elif choice == '2':
            self.list_records()
        elif choice == '3':
            self.edit_record()
        elif choice == '4':
            self.delete_record()
    
    def add_record(self):
        """Add a new record."""
        print("\n--- Add New Record ---")
        try:
            record_id = input("Record ID: ").strip()
            if not record_id:
                print("Error: ID cannot be empty")
                return
            
            if self.data_manager.get_record(record_id):
                print(f"Error: Record with ID {record_id} already exists")
                return
            
            athlete_id = input("Athlete ID: ").strip()
            if not self.data_manager.get_athlete(athlete_id):
                print(f"Error: Athlete with ID {athlete_id} not found")
                return
            
            event_name = input("Event name: ").strip()
            
            print("\nStroke types:")
            for i, stroke in enumerate(StrokeType, 1):
                print(f"  {i}. {stroke.value}")
            stroke_choice = int(input("Choose stroke (1-5): ").strip())
            stroke = list(StrokeType)[stroke_choice - 1]
            
            distance = int(input("Distance (meters): ").strip())
            time_seconds = float(input("Time (seconds): ").strip())
            date_str = input("Date (YYYY-MM-DD): ").strip()
            
            record = Record(
                id=record_id,
                athlete_id=athlete_id,
                event_name=event_name,
                stroke=stroke,
                distance=distance,
                time_seconds=time_seconds,
                date=date_str
            )
            
            if self.data_manager.add_record(record):
                print(f"✓ Record added successfully! Time: {record.format_time()}")
            else:
                print("Error: Could not add record")
        except (ValueError, IndexError) as e:
            print(f"Error: Invalid input - {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def list_records(self):
        """List all records."""
        athlete_id = input("\nFilter by athlete ID (or press Enter for all): ").strip()
        athlete_id = athlete_id if athlete_id else None
        
        records = self.data_manager.list_records(athlete_id)
        if not records:
            print("\nNo records found.")
            return
        
        print(f"\n--- Records ({len(records)}) ---")
        print(f"{'ID':<10} {'Athlete ID':<12} {'Event':<20} {'Distance':<10} {'Time':<12} {'Date':<12}")
        print("-" * 90)
        for record in sorted(records, key=lambda r: r.date, reverse=True):
            event = f"{record.stroke.value[:15]}"
            print(f"{record.id:<10} {record.athlete_id:<12} {event:<20} {record.distance}m{'':<6} {record.format_time():<12} {record.date}")
    
    def edit_record(self):
        """Edit an existing record."""
        record_id = input("\nEnter record ID to edit: ").strip()
        record = self.data_manager.get_record(record_id)
        
        if not record:
            print(f"Error: Record with ID {record_id} not found")
            return
        
        print(f"\nEditing record: {record.id}")
        print("(Press Enter to keep current value)")
        
        try:
            event_name = input(f"Event name [{record.event_name}]: ").strip() or record.event_name
            distance_str = input(f"Distance [{record.distance}]: ").strip()
            time_str = input(f"Time in seconds [{record.time_seconds}]: ").strip()
            
            record.event_name = event_name
            if distance_str:
                record.distance = int(distance_str)
            if time_str:
                record.time_seconds = float(time_str)
            
            if self.data_manager.update_record(record):
                print("✓ Record updated successfully!")
            else:
                print("Error: Could not update record")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_record(self):
        """Delete a record."""
        record_id = input("\nEnter record ID to delete: ").strip()
        record = self.data_manager.get_record(record_id)
        
        if not record:
            print(f"Error: Record with ID {record_id} not found")
            return
        
        confirm = input(f"Delete record {record_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if self.data_manager.delete_record(record_id):
                print("✓ Record deleted successfully!")
            else:
                print("Error: Could not delete record")
    
    def import_menu(self):
        """Import athletes from CSV."""
        print("\n--- Import Athletes ---")
        print("CSV format: id,first_name,last_name,date_of_birth,gender")
        print("Example: A001,John,Smith,2005-03-15,M")
        
        file_path = input("\nEnter CSV file path: ").strip()
        if not file_path:
            return
        
        imported, errors = self.data_manager.import_athletes_from_csv(file_path)
        
        print(f"\n✓ Imported {imported} athletes")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
    
    def assign_age_groups(self):
        """Assign athletes to age groups."""
        print("\n--- Assign Age Groups ---")
        
        date_str = input("Reference date (YYYY-MM-DD): ").strip()
        try:
            reference_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            self.data_manager.assign_age_groups(reference_date)
            print("✓ Age groups assigned successfully!")
            
            # Show summary
            athletes = self.data_manager.list_athletes()
            assigned = sum(1 for a in athletes if a.age_group)
            print(f"\nAssigned {assigned} out of {len(athletes)} athletes to age groups")
        except ValueError:
            print("Error: Invalid date format")
        except Exception as e:
            print(f"Error: {e}")
    
    def show_statistics(self):
        """Show athlete statistics."""
        athlete_id = input("\nEnter athlete ID: ").strip()
        
        athlete = self.data_manager.get_athlete(athlete_id)
        if not athlete:
            print(f"Error: Athlete with ID {athlete_id} not found")
            return
        
        stats = self.data_manager.get_athlete_statistics(athlete_id)
        if not stats:
            print("No statistics available")
            return
        
        print(f"\n--- Statistics for {athlete.first_name} {athlete.last_name} ---")
        print(f"Total Events: {stats.total_events}")
        
        if stats.personal_bests:
            print("\nPersonal Bests:")
            for event, time in sorted(stats.personal_bests.items()):
                minutes = int(time // 60)
                seconds = time % 60
                formatted_time = f"{minutes:02d}:{seconds:05.2f}"
                print(f"  {event}: {formatted_time}")
        
        if stats.average_time:
            minutes = int(stats.average_time // 60)
            seconds = stats.average_time % 60
            print(f"\nAverage Time: {minutes:02d}:{seconds:05.2f}")
    
    def exit_app(self):
        """Exit the application."""
        print("Goodbye!")
        sys.exit(0)


def main():
    """Main entry point."""
    cli = TournamentCLI()
    cli.run()


if __name__ == '__main__':
    main()
