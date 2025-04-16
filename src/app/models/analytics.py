from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from .base import BaseDataModel

class AnalyticsEvent(BaseDataModel):
    """Model for tracking analytics events."""
    event_id: int = Field(..., description="Unique identifier for the event")
    event_type: str = Field(..., description="Type of the event")
    event_data: Dict = Field(..., description="Data associated with the event")
    timestamp: datetime = Field(..., description="When the event occurred")
    user_id: Optional[int] = Field(None, description="ID of the user who triggered the event")
    session_id: Optional[str] = Field(None, description="Session ID when event occurred")
    ip_address: Optional[str] = Field(None, description="IP address when event occurred")
    user_agent: Optional[str] = Field(None, description="User agent string")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    page_url: Optional[str] = Field(None, description="Page URL where event occurred")
    device_info: Optional[Dict] = Field(None, description="Information about the device")

class PageView(BaseDataModel):
    """Model for tracking page views."""
    view_id: int = Field(..., description="Unique identifier for the page view")
    page_url: str = Field(..., description="URL of the page viewed")
    timestamp: datetime = Field(..., description="When the page was viewed")
    user_id: Optional[int] = Field(None, description="ID of the user who viewed the page")
    session_id: str = Field(..., description="Session ID")
    duration: Optional[int] = Field(None, description="Time spent on page in seconds")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    device_info: Dict = Field(..., description="Information about the device")
    location_info: Optional[Dict] = Field(None, description="Geographic location information")

class UserEngagement(BaseDataModel):
    """Model for tracking user engagement metrics."""
    engagement_id: int = Field(..., description="Unique identifier for the engagement record")
    user_id: int = Field(..., description="ID of the user")
    date: datetime = Field(..., description="Date of the engagement")
    page_views: int = Field(default=0, description="Number of page views")
    time_spent: int = Field(default=0, description="Total time spent in seconds")
    events_triggered: int = Field(default=0, description="Number of events triggered")
    articles_read: int = Field(default=0, description="Number of articles read")
    comments_made: int = Field(default=0, description="Number of comments made")
    shares: int = Field(default=0, description="Number of shares")
    likes: int = Field(default=0, description="Number of likes")
    searches: int = Field(default=0, description="Number of searches performed")

class ContentAnalytics(BaseDataModel):
    """Model for tracking content performance."""
    content_id: int = Field(..., description="ID of the content")
    content_type: str = Field(..., description="Type of content (article, video, etc.)")
    date: datetime = Field(..., description="Date of the analytics")
    views: int = Field(default=0, description="Number of views")
    unique_views: int = Field(default=0, description="Number of unique views")
    average_time_spent: float = Field(default=0.0, description="Average time spent in seconds")
    shares: int = Field(default=0, description="Number of shares")
    likes: int = Field(default=0, description="Number of likes")
    comments: int = Field(default=0, description="Number of comments")
    bounce_rate: float = Field(default=0.0, description="Bounce rate percentage")
    conversion_rate: float = Field(default=0.0, description="Conversion rate percentage")

class SearchAnalytics(BaseDataModel):
    """Model for tracking search analytics."""
    search_id: int = Field(..., description="Unique identifier for the search")
    query: str = Field(..., description="Search query")
    timestamp: datetime = Field(..., description="When the search was performed")
    user_id: Optional[int] = Field(None, description="ID of the user who performed the search")
    results_count: int = Field(..., description="Number of results returned")
    filters_used: List[str] = Field(default_factory=list, description="Filters applied to the search")
    time_taken: float = Field(..., description="Time taken to return results in seconds")
    clicked_results: List[int] = Field(default_factory=list, description="IDs of clicked results")
    no_results: bool = Field(default=False, description="Whether the search returned no results")

class PerformanceMetrics(BaseDataModel):
    """Model for tracking system performance metrics."""
    metric_id: int = Field(..., description="Unique identifier for the metric")
    timestamp: datetime = Field(..., description="When the metric was recorded")
    metric_type: str = Field(..., description="Type of metric")
    value: float = Field(..., description="Value of the metric")
    unit: str = Field(..., description="Unit of measurement")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")

class ErrorLog(BaseDataModel):
    """Model for tracking system errors."""
    error_id: int = Field(..., description="Unique identifier for the error")
    timestamp: datetime = Field(..., description="When the error occurred")
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    stack_trace: Optional[str] = Field(None, description="Stack trace")
    user_id: Optional[int] = Field(None, description="ID of the user who encountered the error")
    request_data: Optional[Dict] = Field(None, description="Request data when error occurred")
    severity: str = Field(..., description="Severity level of the error")
    status: str = Field(..., description="Status of the error (new, in_progress, resolved)")
    resolved_at: Optional[datetime] = Field(None, description="When the error was resolved") 