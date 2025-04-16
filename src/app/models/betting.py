from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class Bookmaker(BaseDataModel):
    """Model for bookmakers."""
    bookmaker_id: int = Field(..., description="Unique identifier for the bookmaker")
    name: str = Field(..., min_length=1, description="Name of the bookmaker")
    country: str = Field(..., min_length=2, max_length=2, description="Country code of the bookmaker")
    website: str = Field(..., description="Website URL of the bookmaker")
    is_active: bool = Field(..., description="Whether the bookmaker is currently active")
    supported_markets: List[str] = Field(default_factory=list, description="List of supported betting markets")

class BettingMarket(BaseDataModel):
    """Model for betting markets."""
    market_id: int = Field(..., description="Unique identifier for the betting market")
    name: str = Field(..., min_length=1, description="Name of the betting market")
    description: Optional[str] = Field(None, description="Description of the betting market")
    sport_id: int = Field(..., description="ID of the sport this market belongs to")
    is_active: bool = Field(..., description="Whether the market is currently active")
    parameters: Optional[Dict] = Field(None, description="Additional parameters for the market")

class BettingOdds(BaseDataModel):
    """Model for betting odds."""
    event_id: int = Field(..., description="ID of the event these odds are for")
    bookmaker_id: int = Field(..., description="ID of the bookmaker offering these odds")
    market_id: int = Field(..., description="ID of the betting market")
    odds: float = Field(..., gt=0, description="The odds value")
    timestamp: datetime = Field(..., description="When these odds were recorded")
    is_live: bool = Field(..., description="Whether these are live odds")
    probability: Optional[float] = Field(None, ge=0, le=1, description="Implied probability of the odds")
    handicap: Optional[float] = Field(None, description="Handicap value if applicable")
    over_under: Optional[float] = Field(None, description="Over/Under value if applicable")

class BettingOutcome(BaseDataModel):
    """Model for betting outcomes."""
    outcome_id: int = Field(..., description="Unique identifier for the outcome")
    market_id: int = Field(..., description="ID of the betting market")
    event_id: int = Field(..., description="ID of the event")
    outcome_type: str = Field(..., description="Type of outcome (e.g., 'home_win', 'draw', 'away_win')")
    outcome_value: Optional[str] = Field(None, description="Value of the outcome if applicable")
    odds: float = Field(..., gt=0, description="Current odds for this outcome")
    probability: Optional[float] = Field(None, ge=0, le=1, description="Implied probability")

class BettingHistory(BaseDataModel):
    """Model for historical betting odds."""
    event_id: int = Field(..., description="ID of the event")
    bookmaker_id: int = Field(..., description="ID of the bookmaker")
    market_id: int = Field(..., description="ID of the betting market")
    timestamp: datetime = Field(..., description="When these odds were recorded")
    odds_data: Dict = Field(..., description="Historical odds data")
    is_live: bool = Field(..., description="Whether these were live odds")
    source: str = Field(..., description="Source of the odds data")

class BettingArbitrage(BaseDataModel):
    """Model for arbitrage opportunities."""
    event_id: int = Field(..., description="ID of the event")
    market_id: int = Field(..., description="ID of the betting market")
    timestamp: datetime = Field(..., description="When this arbitrage was identified")
    profit_percentage: float = Field(..., gt=0, description="Potential profit percentage")
    stake_distribution: Dict[str, float] = Field(..., description="Optimal stake distribution")
    bookmaker_odds: Dict[str, float] = Field(..., description="Odds from different bookmakers")
    is_active: bool = Field(..., description="Whether this arbitrage opportunity is still active") 