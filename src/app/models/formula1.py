from typing import Optional
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class Formula1Driver(BaseDataModel):
    """Model for Formula 1 driver data with validation rules."""
    
    name: str = Field(..., min_length=1, description="Driver's full name")
    team: str = Field(..., min_length=1, description="Driver's team name")
    position: int = Field(..., ge=1, le=20, description="Current championship position")
    points: float = Field(..., ge=0, description="Total championship points")
    wins: int = Field(..., ge=0, description="Number of race wins")
    podiums: int = Field(..., ge=0, description="Number of podium finishes")
    fastest_laps: int = Field(..., ge=0, description="Number of fastest laps")
    nationality: str = Field(..., min_length=2, description="Driver's nationality")
    car_number: int = Field(..., ge=1, le=99, description="Driver's car number")
    next_race: Optional[str] = Field(None, description="Next scheduled race")
    
    @validator('podiums')
    def validate_podiums(cls, v, values):
        """Validate that podiums count is not less than wins count."""
        if 'wins' in values and v < values['wins']:
            raise ValueError('Podiums count cannot be less than wins count')
        return v
    
    @validator('points')
    def validate_points(cls, v):
        """Validate that points is a multiple of 0.5 (standard F1 points system)."""
        if v * 2 != int(v * 2):
            raise ValueError('Points must be a multiple of 0.5')
        return v
    
    @validator('car_number')
    def validate_car_number(cls, v):
        """Validate that car number is not retired or reserved."""
        reserved_numbers = {17, 19}  # Retired numbers
        if v in reserved_numbers:
            raise ValueError(f'Car number {v} is retired or reserved')
        return v 