from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, validator
from .base import BaseDataModel

class NewsSource(BaseDataModel):
    """Model for news sources."""
    source_id: int = Field(..., description="Unique identifier for the news source")
    name: str = Field(..., min_length=1, description="Name of the news source")
    website: str = Field(..., description="Website URL of the news source")
    country: str = Field(..., min_length=2, max_length=2, description="Country code of the news source")
    language: str = Field(..., min_length=2, max_length=5, description="Language code of the news source")
    is_active: bool = Field(..., description="Whether the source is currently active")
    categories: List[str] = Field(default_factory=list, description="Categories of news covered")
    reliability_score: Optional[float] = Field(None, ge=0, le=1, description="Reliability score of the source")

class NewsArticle(BaseDataModel):
    """Model for news articles."""
    article_id: int = Field(..., description="Unique identifier for the article")
    source_id: int = Field(..., description="ID of the news source")
    title: str = Field(..., min_length=1, description="Title of the article")
    content: str = Field(..., description="Content of the article")
    url: str = Field(..., description="URL of the article")
    published_at: datetime = Field(..., description="When the article was published")
    updated_at: Optional[datetime] = Field(None, description="When the article was last updated")
    author: Optional[str] = Field(None, description="Author of the article")
    sport_id: Optional[int] = Field(None, description="ID of the sport this article is about")
    competition_id: Optional[int] = Field(None, description="ID of the competition this article is about")
    team_id: Optional[int] = Field(None, description="ID of the team this article is about")
    player_id: Optional[int] = Field(None, description="ID of the player this article is about")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the article")
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1, description="Sentiment analysis score")
    is_breaking: bool = Field(default=False, description="Whether this is breaking news")

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class NewsImage(BaseDataModel):
    """Model for images in news articles."""
    image_id: int = Field(..., description="Unique identifier for the image")
    article_id: int = Field(..., description="ID of the article this image belongs to")
    url: str = Field(..., description="URL of the image")
    caption: Optional[str] = Field(None, description="Caption for the image")
    alt_text: Optional[str] = Field(None, description="Alternative text for the image")
    width: Optional[int] = Field(None, description="Width of the image in pixels")
    height: Optional[int] = Field(None, description="Height of the image in pixels")
    source: Optional[str] = Field(None, description="Source of the image")
    is_featured: bool = Field(default=False, description="Whether this is the featured image")

class NewsVideo(BaseDataModel):
    """Model for videos in news articles."""
    video_id: int = Field(..., description="Unique identifier for the video")
    article_id: int = Field(..., description="ID of the article this video belongs to")
    url: str = Field(..., description="URL of the video")
    title: Optional[str] = Field(None, description="Title of the video")
    description: Optional[str] = Field(None, description="Description of the video")
    duration: Optional[int] = Field(None, description="Duration of the video in seconds")
    thumbnail_url: Optional[str] = Field(None, description="URL of the video thumbnail")
    source: Optional[str] = Field(None, description="Source of the video")
    is_embed: bool = Field(default=False, description="Whether this is an embedded video")

class NewsComment(BaseDataModel):
    """Model for comments on news articles."""
    comment_id: int = Field(..., description="Unique identifier for the comment")
    article_id: int = Field(..., description="ID of the article this comment is on")
    user_id: int = Field(..., description="ID of the user who made the comment")
    content: str = Field(..., description="Content of the comment")
    created_at: datetime = Field(..., description="When the comment was created")
    updated_at: Optional[datetime] = Field(None, description="When the comment was last updated")
    parent_comment_id: Optional[int] = Field(None, description="ID of the parent comment if this is a reply")
    likes: int = Field(default=0, description="Number of likes on the comment")
    is_edited: bool = Field(default=False, description="Whether the comment has been edited")
    is_deleted: bool = Field(default=False, description="Whether the comment has been deleted")

class NewsSubscription(BaseDataModel):
    """Model for news subscriptions."""
    subscription_id: int = Field(..., description="Unique identifier for the subscription")
    user_id: int = Field(..., description="ID of the user who subscribed")
    source_id: Optional[int] = Field(None, description="ID of the news source if subscribed to a specific source")
    sport_id: Optional[int] = Field(None, description="ID of the sport if subscribed to a specific sport")
    team_id: Optional[int] = Field(None, description="ID of the team if subscribed to a specific team")
    player_id: Optional[int] = Field(None, description="ID of the player if subscribed to a specific player")
    created_at: datetime = Field(..., description="When the subscription was created")
    is_active: bool = Field(..., description="Whether the subscription is currently active")
    notification_preferences: Dict[str, bool] = Field(
        default_factory=lambda: {
            "email": True,
            "push": True,
            "breaking_news": True
        },
        description="User's notification preferences"
    ) 