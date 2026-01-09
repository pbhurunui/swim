"""
Data models for the Swimming Tournament Application.
"""
from datetime import datetime, date
from typing import Optional, Dict, List
from dataclasses import dataclass, field, asdict
from enum import Enum


class Gender(Enum):
    """Athlete gender."""
    MALE = "M"
    FEMALE = "F"


class StrokeType(Enum):
    """Swimming stroke types."""
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"
    INDIVIDUAL_MEDLEY = "Individual Medley"


@dataclass
class Athlete:
    """Represents a swimmer in the tournament."""
    id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    age_group: Optional[str] = None
    
    def __post_init__(self):
        """Convert string gender to Gender enum if needed."""
        if isinstance(self.gender, str):
            self.gender = Gender(self.gender)
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
    
    def calculate_age(self, reference_date: date) -> int:
        """Calculate age on a specific reference date."""
        age = reference_date.year - self.date_of_birth.year
        if (reference_date.month, reference_date.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age
    
    def to_dict(self) -> Dict:
        """Convert athlete to dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "gender": self.gender.value,
            "age_group": self.age_group
        }


@dataclass
class AgeGroup:
    """Represents an age group category."""
    name: str
    min_age: int
    max_age: int
    gender: Optional[Gender] = None
    
    def __post_init__(self):
        """Convert string gender to Gender enum if needed."""
        if isinstance(self.gender, str):
            self.gender = Gender(self.gender) if self.gender else None
    
    def contains_age(self, age: int) -> bool:
        """Check if an age falls within this group."""
        return self.min_age <= age <= self.max_age
    
    def to_dict(self) -> Dict:
        """Convert age group to dictionary."""
        return {
            "name": self.name,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "gender": self.gender.value if self.gender else None
        }


@dataclass
class Record:
    """Represents a swimming record/result."""
    id: str
    athlete_id: str
    event_name: str
    stroke: StrokeType
    distance: int  # in meters
    time_seconds: float
    date: date
    
    def __post_init__(self):
        """Convert string types to proper types if needed."""
        if isinstance(self.stroke, str):
            self.stroke = StrokeType(self.stroke)
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
    
    def format_time(self) -> str:
        """Format time in MM:SS.ms format."""
        minutes = int(self.time_seconds // 60)
        seconds = self.time_seconds % 60
        return f"{minutes:02d}:{seconds:05.2f}"
    
    def to_dict(self) -> Dict:
        """Convert record to dictionary."""
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "event_name": self.event_name,
            "stroke": self.stroke.value,
            "distance": self.distance,
            "time_seconds": self.time_seconds,
            "date": self.date.isoformat()
        }


@dataclass
class AthleteStatistics:
    """Statistics for an athlete."""
    athlete_id: str
    total_events: int = 0
    personal_bests: Dict[str, float] = field(default_factory=dict)  # event_key -> time
    average_time: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert statistics to dictionary."""
        return {
            "athlete_id": self.athlete_id,
            "total_events": self.total_events,
            "personal_bests": self.personal_bests,
            "average_time": self.average_time
        }
