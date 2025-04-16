from typing import Optional
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class PremierLeagueTeam(BaseDataModel):
    """Model for Premier League team data with validation rules."""
    
    name: str = Field(..., min_length=1, description="Team's full name")
    position: int = Field(..., ge=1, le=20, description="Current league position")
    played: int = Field(..., ge=0, description="Number of matches played")
    won: int = Field(..., ge=0, description="Number of matches won")
    drawn: int = Field(..., ge=0, description="Number of matches drawn")
    lost: int = Field(..., ge=0, description="Number of matches lost")
    goals_for: int = Field(..., ge=0, description="Goals scored")
    goals_against: int = Field(..., ge=0, description="Goals conceded")
    goal_difference: int = Field(..., description="Goal difference")
    points: int = Field(..., ge=0, description="Total points")
    form: str = Field(..., min_length=5, max_length=5, description="Last 5 matches form (W/D/L)")
    next_match: Optional[str] = Field(None, description="Next scheduled match")
    
    @validator('form')
    def validate_form(cls, v):
        """Validate that form string contains only W, D, or L characters."""
        valid_chars = {'W', 'D', 'L'}
        if not all(char in valid_chars for char in v):
            raise ValueError('Form must contain only W (win), D (draw), or L (loss)')
        return v
    
    @validator('goal_difference')
    def validate_goal_difference(cls, v, values):
        """Validate that goal difference matches goals_for - goals_against."""
        if 'goals_for' in values and 'goals_against' in values:
            expected_gd = values['goals_for'] - values['goals_against']
            if v != expected_gd:
                raise ValueError(f'Goal difference must be {expected_gd} (goals_for - goals_against)')
        return v
    
    @validator('points')
    def validate_points(cls, v, values):
        """Validate that points match the standard scoring system (3 for win, 1 for draw)."""
        if 'won' in values and 'drawn' in values:
            expected_points = (values['won'] * 3) + values['drawn']
            if v != expected_points:
                raise ValueError(f'Points must be {expected_points} (3 * won + drawn)')
        return v 