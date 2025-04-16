from typing import Optional
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class UFCFighter(BaseDataModel):
    """Model for UFC fighter data with validation rules."""
    
    name: str = Field(..., min_length=1, description="Fighter's full name")
    rank: str = Field(..., description="Current ranking in weight class")
    record: str = Field(..., description="Fighter's professional record (W-L-D)")
    weight_class: str = Field(..., description="Fighter's weight class")
    country: Optional[str] = Field(None, description="Fighter's country of origin")
    age: Optional[int] = Field(None, ge=0, le=100, description="Fighter's age")
    height: Optional[str] = Field(None, description="Fighter's height")
    reach: Optional[str] = Field(None, description="Fighter's reach")
    last_fight: Optional[str] = Field(None, description="Date of last fight")
    
    @validator('record')
    def validate_record(cls, v):
        """Validate that the record is in the correct format (W-L-D)."""
        parts = v.split('-')
        if len(parts) != 3:
            raise ValueError('Record must be in format W-L-D')
        try:
            wins, losses, draws = map(int, parts)
            if wins < 0 or losses < 0 or draws < 0:
                raise ValueError('Record numbers cannot be negative')
        except ValueError:
            raise ValueError('Record must contain valid numbers')
        return v
    
    @validator('rank')
    def validate_rank(cls, v):
        """Validate that rank is either a number or 'C' for champion."""
        if v.lower() == 'c':
            return 'C'
        try:
            rank_num = int(v)
            if rank_num < 1:
                raise ValueError('Rank must be positive')
            return str(rank_num)
        except ValueError:
            raise ValueError('Rank must be a number or "C" for champion')
    
    @validator('weight_class')
    def validate_weight_class(cls, v):
        """Validate that weight class is one of the standard UFC divisions."""
        valid_classes = {
            'Heavyweight', 'Light Heavyweight', 'Middleweight',
            'Welterweight', 'Lightweight', 'Featherweight',
            'Bantamweight', 'Flyweight', "Women's Featherweight",
            "Women's Bantamweight", "Women's Flyweight", "Women's Strawweight"
        }
        if v not in valid_classes:
            raise ValueError(f'Invalid weight class. Must be one of: {", ".join(valid_classes)}')
        return v 