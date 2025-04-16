from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class FantasyLeague(BaseDataModel):
    """Model for fantasy sports leagues."""
    fantasy_league_id: int = Field(..., description="Unique identifier for the fantasy league")
    name: str = Field(..., min_length=1, description="Name of the fantasy league")
    competition_id: Optional[int] = Field(None, description="Real competition this fantasy league is based on")
    scoring_system: str = Field(..., description="Description of the scoring system used")
    start_date: datetime = Field(..., description="Start date of the fantasy league")
    end_date: datetime = Field(..., description="End date of the fantasy league")
    is_active: bool = Field(..., description="Whether the fantasy league is currently active")
    max_teams: Optional[int] = Field(None, description="Maximum number of teams allowed")
    entry_fee: Optional[float] = Field(None, description="Entry fee if applicable")

class FantasyTeam(BaseDataModel):
    """Model for user's fantasy teams."""
    fantasy_team_id: int = Field(..., description="Unique identifier for the fantasy team")
    fantasy_league_id: int = Field(..., description="Fantasy league this team belongs to")
    name: str = Field(..., min_length=1, description="Name of the fantasy team")
    owner_name: str = Field(..., min_length=1, description="Name of the team owner")
    total_points: float = Field(default=0.0, description="Total fantasy points accumulated")
    rank: Optional[int] = Field(None, description="Current rank in the league")
    budget: Optional[float] = Field(None, description="Remaining budget for transfers")
    transfers_made: int = Field(default=0, description="Number of transfers made")
    transfers_remaining: Optional[int] = Field(None, description="Number of transfers remaining")

class FantasyTeamPlayer(BaseDataModel):
    """Model for players in fantasy teams."""
    fantasy_team_id: int = Field(..., description="Fantasy team ID")
    player_id: int = Field(..., description="Player ID")
    added_date: datetime = Field(..., description="Date when player was added to team")
    dropped_date: Optional[datetime] = Field(None, description="Date when player was dropped")
    purchase_price: Optional[float] = Field(None, description="Price paid for the player")
    current_value: Optional[float] = Field(None, description="Current market value")
    is_captain: bool = Field(default=False, description="Whether player is team captain")
    is_vice_captain: bool = Field(default=False, description="Whether player is vice captain")
    position: str = Field(..., description="Position in fantasy team")

    @validator('dropped_date')
    def validate_dates(cls, v, values):
        """Ensure dropped_date is after added_date if provided."""
        if v and values.get('added_date') and v < values['added_date']:
            raise ValueError("Dropped date must be after added date")
        return v

class FantasyScore(BaseDataModel):
    """Model for fantasy points scored in each round."""
    fantasy_team_id: int = Field(..., description="Fantasy team ID")
    round: int = Field(..., description="Round number in the competition")
    points: float = Field(..., description="Points scored in this round")
    rank: Optional[int] = Field(None, description="Rank in this round")
    bench_points: Optional[float] = Field(None, description="Points scored by bench players")
    transfer_points: Optional[float] = Field(None, description="Points deducted for transfers")
    captain_points: Optional[float] = Field(None, description="Points scored by captain")
    vice_captain_points: Optional[float] = Field(None, description="Points scored by vice captain")

class FantasyPlayerStats(BaseDataModel):
    """Model for player statistics in fantasy context."""
    player_id: int = Field(..., description="Player ID")
    round: int = Field(..., description="Round number")
    points: float = Field(..., description="Fantasy points scored")
    minutes_played: int = Field(..., description="Minutes played")
    goals_scored: Optional[int] = Field(None, description="Goals scored")
    assists: Optional[int] = Field(None, description="Assists made")
    clean_sheets: Optional[int] = Field(None, description="Clean sheets kept")
    saves: Optional[int] = Field(None, description="Saves made")
    bonus_points: Optional[int] = Field(None, description="Bonus points awarded")
    yellow_cards: Optional[int] = Field(None, description="Yellow cards received")
    red_cards: Optional[int] = Field(None, description="Red cards received")
    own_goals: Optional[int] = Field(None, description="Own goals scored")
    penalties_missed: Optional[int] = Field(None, description="Penalties missed")
    penalties_saved: Optional[int] = Field(None, description="Penalties saved") 