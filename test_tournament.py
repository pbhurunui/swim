"""
Unit tests for the Swimming Tournament Application.
"""
import unittest
import os
import tempfile
from datetime import date
from models import Athlete, AgeGroup, Record, Gender, StrokeType
from data_manager import DataManager


class TestModels(unittest.TestCase):
    """Test the data models."""
    
    def test_athlete_creation(self):
        """Test creating an athlete."""
        athlete = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        self.assertEqual(athlete.id, "A001")
        self.assertEqual(athlete.first_name, "John")
        self.assertEqual(athlete.gender, Gender.MALE)
        self.assertEqual(athlete.date_of_birth, date(2005, 6, 15))
    
    def test_athlete_age_calculation(self):
        """Test age calculation."""
        athlete = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        # Age on 2024-01-01
        age = athlete.calculate_age(date(2024, 1, 1))
        self.assertEqual(age, 18)
        
        # Age on 2024-07-01 (after birthday)
        age = athlete.calculate_age(date(2024, 7, 1))
        self.assertEqual(age, 19)
    
    def test_age_group_contains_age(self):
        """Test age group age checking."""
        age_group = AgeGroup(
            name="Youth",
            min_age=10,
            max_age=14,
            gender=None
        )
        self.assertTrue(age_group.contains_age(10))
        self.assertTrue(age_group.contains_age(12))
        self.assertTrue(age_group.contains_age(14))
        self.assertFalse(age_group.contains_age(9))
        self.assertFalse(age_group.contains_age(15))
    
    def test_record_time_formatting(self):
        """Test record time formatting."""
        record = Record(
            id="R001",
            athlete_id="A001",
            event_name="100m Freestyle",
            stroke=StrokeType.FREESTYLE,
            distance=100,
            time_seconds=65.45,
            date="2024-01-15"
        )
        self.assertEqual(record.format_time(), "01:05.45")
        
        # Test time under 1 minute
        record.time_seconds = 32.18
        self.assertEqual(record.format_time(), "00:32.18")


class TestDataManager(unittest.TestCase):
    """Test the data manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary file for test data
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.data_manager = DataManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_and_get_athlete(self):
        """Test adding and retrieving an athlete."""
        athlete = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        
        self.assertTrue(self.data_manager.add_athlete(athlete))
        retrieved = self.data_manager.get_athlete("A001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, "John")
    
    def test_add_duplicate_athlete(self):
        """Test adding duplicate athlete fails."""
        athlete1 = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        athlete2 = Athlete(
            id="A001",
            first_name="Jane",
            last_name="Smith",
            date_of_birth="2006-03-20",
            gender="F"
        )
        
        self.assertTrue(self.data_manager.add_athlete(athlete1))
        self.assertFalse(self.data_manager.add_athlete(athlete2))
    
    def test_update_athlete(self):
        """Test updating an athlete."""
        athlete = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        self.data_manager.add_athlete(athlete)
        
        athlete.first_name = "Jonathan"
        self.assertTrue(self.data_manager.update_athlete(athlete))
        
        retrieved = self.data_manager.get_athlete("A001")
        self.assertEqual(retrieved.first_name, "Jonathan")
    
    def test_delete_athlete(self):
        """Test deleting an athlete."""
        athlete = Athlete(
            id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth="2005-06-15",
            gender="M"
        )
        self.data_manager.add_athlete(athlete)
        
        self.assertTrue(self.data_manager.delete_athlete("A001"))
        self.assertIsNone(self.data_manager.get_athlete("A001"))
    
    def test_age_group_assignment(self):
        """Test age group assignment."""
        # Add age groups
        ag1 = AgeGroup("10-12 Years", 10, 12, None)
        ag2 = AgeGroup("13-15 Years", 13, 15, None)
        self.data_manager.add_age_group(ag1)
        self.data_manager.add_age_group(ag2)
        
        # Add athletes
        athlete1 = Athlete("A001", "John", "Doe", "2012-06-15", "M")
        athlete2 = Athlete("A002", "Jane", "Smith", "2009-03-20", "F")
        self.data_manager.add_athlete(athlete1)
        self.data_manager.add_athlete(athlete2)
        
        # Assign age groups based on 2024-01-01
        self.data_manager.assign_age_groups(date(2024, 1, 1))
        
        # Check assignments
        athlete1 = self.data_manager.get_athlete("A001")
        athlete2 = self.data_manager.get_athlete("A002")
        
        self.assertEqual(athlete1.age_group, "10-12 Years")  # 11 years old
        self.assertEqual(athlete2.age_group, "13-15 Years")  # 14 years old
    
    def test_athlete_statistics(self):
        """Test athlete statistics calculation."""
        # Add athlete
        athlete = Athlete("A001", "John", "Doe", "2005-06-15", "M")
        self.data_manager.add_athlete(athlete)
        
        # Add records
        record1 = Record("R001", "A001", "Event 1", StrokeType.FREESTYLE, 100, 65.5, "2024-01-15")
        record2 = Record("R002", "A001", "Event 2", StrokeType.FREESTYLE, 100, 63.2, "2024-01-20")
        record3 = Record("R003", "A001", "Event 3", StrokeType.BACKSTROKE, 50, 35.8, "2024-01-25")
        
        self.data_manager.add_record(record1)
        self.data_manager.add_record(record2)
        self.data_manager.add_record(record3)
        
        # Get statistics
        stats = self.data_manager.get_athlete_statistics("A001")
        
        self.assertEqual(stats.total_events, 3)
        self.assertEqual(stats.personal_bests["100m Freestyle"], 63.2)
        self.assertEqual(stats.personal_bests["50m Backstroke"], 35.8)
        self.assertIsNotNone(stats.average_time)


class TestCSVImport(unittest.TestCase):
    """Test CSV import functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_data = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_data.close()
        self.data_manager = DataManager(self.temp_data.name)
        
        # Create test CSV
        self.temp_csv = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_csv.write("id,first_name,last_name,date_of_birth,gender\n")
        self.temp_csv.write("A001,John,Doe,2005-06-15,M\n")
        self.temp_csv.write("A002,Jane,Smith,2006-03-20,F\n")
        self.temp_csv.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_data.name):
            os.unlink(self.temp_data.name)
        if os.path.exists(self.temp_csv.name):
            os.unlink(self.temp_csv.name)
    
    def test_import_athletes_from_csv(self):
        """Test importing athletes from CSV."""
        imported, errors = self.data_manager.import_athletes_from_csv(self.temp_csv.name)
        
        self.assertEqual(imported, 2)
        self.assertEqual(len(errors), 0)
        
        athlete1 = self.data_manager.get_athlete("A001")
        athlete2 = self.data_manager.get_athlete("A002")
        
        self.assertIsNotNone(athlete1)
        self.assertEqual(athlete1.first_name, "John")
        self.assertIsNotNone(athlete2)
        self.assertEqual(athlete2.first_name, "Jane")


if __name__ == '__main__':
    unittest.main()
