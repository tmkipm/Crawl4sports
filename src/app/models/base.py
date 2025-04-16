from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class BaseDataModel(BaseModel):
    """Base model for all data models in the application."""
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the record was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When the record was last updated")
    is_deleted: bool = Field(default=False, description="Whether the record is soft-deleted")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata for the record")
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="When the data was scraped")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class Sport(BaseDataModel):
    """Model for sports."""
    sport_id: int = Field(..., description="Unique identifier for the sport")
    name: str = Field(..., min_length=1, description="Name of the sport")
    code: str = Field(..., min_length=2, max_length=10, description="Short code for the sport")
    description: Optional[str] = Field(None, description="Description of the sport")
    is_active: bool = Field(..., description="Whether the sport is currently active")
    parent_sport_id: Optional[int] = Field(None, description="ID of parent sport if this is a sub-sport")
    competition_ids: List[int] = Field(default_factory=list, description="List of competition IDs for this sport")

class Player(BaseDataModel):
    """Model for individual athletes."""
    player_id: int = Field(..., description="Unique identifier for the player")
    full_name: str = Field(..., min_length=1, description="Player's full name")
    date_of_birth: datetime = Field(..., description="Player's date of birth")
    nationality: str = Field(..., min_length=2, description="Player's nationality")
    height: Optional[float] = Field(None, description="Player's height in meters")
    weight: Optional[float] = Field(None, description="Player's weight in kilograms")
    sport_id: int = Field(..., description="Primary sport the player participates in")
    current_team_id: Optional[int] = Field(None, description="Current team ID if applicable")

class Team(BaseDataModel):
    """Model for teams or squads."""
    team_id: int = Field(..., description="Unique identifier for the team")
    name: str = Field(..., min_length=1, description="Team name")
    sport_id: int = Field(..., description="Sport the team participates in")
    country: str = Field(..., min_length=2, description="Team's country of origin")
    founded_year: Optional[int] = Field(None, description="Year the team was founded")
    stadium: Optional[str] = Field(None, description="Home stadium/venue name")

class Competition(BaseDataModel):
    """Model for leagues, tournaments, or competitions."""
    competition_id: int = Field(..., description="Unique identifier for the competition")
    name: str = Field(..., min_length=1, description="Competition name")
    type: str = Field(..., description="Type of competition (League, Tournament, etc.)")
    sport_id: int = Field(..., description="Sport this competition belongs to")
    start_date: datetime = Field(..., description="Start date of the competition")
    end_date: datetime = Field(..., description="End date of the competition")
    is_active: bool = Field(..., description="Whether the competition is currently active")

class Event(BaseDataModel):
    """Model for matches, games, or events."""
    event_id: int = Field(..., description="Unique identifier for the event")
    competition_id: Optional[int] = Field(None, description="Competition this event belongs to")
    sport_id: int = Field(..., description="Sport this event belongs to")
    event_date: datetime = Field(..., description="Date and time of the event")
    location: str = Field(..., description="Venue or location of the event")
    status: str = Field(..., description="Event status (scheduled, live, completed, etc.)")
    stage: Optional[str] = Field(None, description="Stage or round in the competition")

class EventParticipant(BaseDataModel):
    """Model for participants in an event."""
    event_id: int = Field(..., description="Event ID")
    team_id: Optional[int] = Field(None, description="Team ID if team participant")
    player_id: Optional[int] = Field(None, description="Player ID if individual participant")
    is_home: Optional[bool] = Field(None, description="Whether this is the home participant")
    score: Optional[int] = Field(None, description="Score or points achieved")
    outcome: Optional[str] = Field(None, description="Outcome (Win, Loss, Draw, etc.)")
    rank: Optional[int] = Field(None, description="Finishing position if applicable")

    @validator('team_id', 'player_id')
    def validate_participant(cls, v, values):
        """Ensure at least one of team_id or player_id is provided."""
        if not values.get('team_id') and not values.get('player_id'):
            raise ValueError("Either team_id or player_id must be provided")
        return v

class PlayerAppearance(BaseDataModel):
    """Model for player appearances in events."""
    event_id: int = Field(..., description="Event ID")
    player_id: int = Field(..., description="Player ID")
    team_id: int = Field(..., description="Team ID")
    started: bool = Field(..., description="Whether player started the event")
    entry_time: Optional[int] = Field(None, description="Minute when player entered")
    exit_time: Optional[int] = Field(None, description="Minute when player exited")
    position: Optional[str] = Field(None, description="Position played")

class PlayerStats(BaseDataModel):
    """Model for player statistics in events."""
    event_id: int = Field(..., description="Event ID")
    player_id: int = Field(..., description="Player ID")
    team_id: int = Field(..., description="Team ID")
    minutes_played: int = Field(..., description="Minutes played in the event")
    points: Optional[float] = Field(None, description="Points scored")
    goals: Optional[int] = Field(None, description="Goals scored")
    assists: Optional[int] = Field(None, description="Assists made")
    yellow_cards: Optional[int] = Field(None, description="Yellow cards received")
    red_cards: Optional[int] = Field(None, description="Red cards received")

class MatchEvent(BaseDataModel):
    """Model for minute-by-minute events in matches."""
    event_id: int = Field(..., description="Event ID")
    event_type: str = Field(..., description="Type of event (Goal, Card, Substitution, etc.)")
    minute: int = Field(..., description="Minute when event occurred")
    player_id: Optional[int] = Field(None, description="Player involved")
    related_player_id: Optional[int] = Field(None, description="Related player if applicable")
    team_id: Optional[int] = Field(None, description="Team involved")
    description: Optional[str] = Field(None, description="Description of the event")

class PlayerTransfer(BaseDataModel):
    """Model for player transfers between teams."""
    transfer_id: int = Field(..., description="Unique identifier for the transfer")
    player_id: int = Field(..., description="Player ID")
    from_team_id: Optional[int] = Field(None, description="Previous team ID")
    to_team_id: int = Field(..., description="New team ID")
    transfer_date: datetime = Field(..., description="Date of transfer")
    fee: Optional[float] = Field(None, description="Transfer fee if applicable")
    transfer_type: str = Field(..., description="Type of transfer (Transfer, Loan, etc.)")

class PlayerInjury(BaseDataModel):
    """Model for player injuries."""
    injury_id: int = Field(..., description="Unique identifier for the injury")
    player_id: int = Field(..., description="Player ID")
    injury_start_date: datetime = Field(..., description="Start date of injury")
    expected_return_date: Optional[datetime] = Field(None, description="Expected return date")
    injury_type: str = Field(..., description="Type of injury")
    description: Optional[str] = Field(None, description="Description of the injury")
    status: str = Field(..., description="Injury status (Ongoing, Recovered, etc.)")
    source_url: Optional[str] = Field(None, description="Source URL for the injury information")

    @validator('source_url')
    def validate_url(cls, v):
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('source_url must be a valid HTTP/HTTPS URL')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 