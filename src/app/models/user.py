from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr, validator
from .base import BaseDataModel

class User(BaseDataModel):
    """Model for user accounts."""
    user_id: int = Field(..., description="Unique identifier for the user")
    username: str = Field(..., min_length=3, max_length=50, description="Username for login")
    email: EmailStr = Field(..., description="Email address of the user")
    hashed_password: str = Field(..., description="Hashed password")
    full_name: str = Field(..., min_length=1, description="User's full name")
    date_of_birth: Optional[datetime] = Field(None, description="User's date of birth")
    country: Optional[str] = Field(None, min_length=2, max_length=2, description="Country code")
    language: str = Field(default="en", min_length=2, max_length=5, description="Preferred language")
    is_active: bool = Field(default=True, description="Whether the account is active")
    is_verified: bool = Field(default=False, description="Whether the email is verified")
    is_admin: bool = Field(default=False, description="Whether the user has admin privileges")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    preferences: Dict = Field(
        default_factory=lambda: {
            "theme": "light",
            "notifications": True,
            "email_updates": True
        },
        description="User preferences"
    )

    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v

class UserProfile(BaseDataModel):
    """Model for user profile information."""
    profile_id: int = Field(..., description="Unique identifier for the profile")
    user_id: int = Field(..., description="ID of the user this profile belongs to")
    bio: Optional[str] = Field(None, max_length=500, description="User's biography")
    avatar_url: Optional[str] = Field(None, description="URL of the user's avatar")
    favorite_sports: List[int] = Field(default_factory=list, description="List of favorite sport IDs")
    favorite_teams: List[int] = Field(default_factory=list, description="List of favorite team IDs")
    favorite_players: List[int] = Field(default_factory=list, description="List of favorite player IDs")
    social_links: Dict[str, str] = Field(
        default_factory=dict,
        description="Social media links (platform -> URL)"
    )
    location: Optional[str] = Field(None, description="User's location")
    timezone: Optional[str] = Field(None, description="User's timezone")

class UserSession(BaseDataModel):
    """Model for user sessions."""
    session_id: int = Field(..., description="Unique identifier for the session")
    user_id: int = Field(..., description="ID of the user this session belongs to")
    token: str = Field(..., description="Session token")
    device_info: Dict = Field(..., description="Information about the device")
    ip_address: str = Field(..., description="IP address of the device")
    created_at: datetime = Field(..., description="When the session was created")
    expires_at: datetime = Field(..., description="When the session expires")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    is_active: bool = Field(..., description="Whether the session is active")

class UserActivity(BaseDataModel):
    """Model for tracking user activities."""
    activity_id: int = Field(..., description="Unique identifier for the activity")
    user_id: int = Field(..., description="ID of the user who performed the activity")
    activity_type: str = Field(..., description="Type of activity")
    activity_data: Dict = Field(..., description="Data related to the activity")
    timestamp: datetime = Field(..., description="When the activity occurred")
    ip_address: Optional[str] = Field(None, description="IP address when activity was performed")
    user_agent: Optional[str] = Field(None, description="User agent string")

class UserNotification(BaseDataModel):
    """Model for user notifications."""
    notification_id: int = Field(..., description="Unique identifier for the notification")
    user_id: int = Field(..., description="ID of the user to notify")
    title: str = Field(..., description="Title of the notification")
    message: str = Field(..., description="Content of the notification")
    notification_type: str = Field(..., description="Type of notification")
    is_read: bool = Field(default=False, description="Whether the notification has been read")
    created_at: datetime = Field(..., description="When the notification was created")
    read_at: Optional[datetime] = Field(None, description="When the notification was read")
    action_url: Optional[str] = Field(None, description="URL for action related to notification")
    priority: int = Field(default=0, description="Priority level of the notification")

class UserRole(BaseDataModel):
    """Model for user roles and permissions."""
    role_id: int = Field(..., description="Unique identifier for the role")
    name: str = Field(..., description="Name of the role")
    description: Optional[str] = Field(None, description="Description of the role")
    permissions: List[str] = Field(..., description="List of permissions granted by this role")
    is_system: bool = Field(default=False, description="Whether this is a system role")
    created_at: datetime = Field(..., description="When the role was created")
    updated_at: Optional[datetime] = Field(None, description="When the role was last updated")

class UserRoleAssignment(BaseDataModel):
    """Model for assigning roles to users."""
    assignment_id: int = Field(..., description="Unique identifier for the assignment")
    user_id: int = Field(..., description="ID of the user")
    role_id: int = Field(..., description="ID of the role")
    assigned_by: int = Field(..., description="ID of the user who assigned the role")
    assigned_at: datetime = Field(..., description="When the role was assigned")
    expires_at: Optional[datetime] = Field(None, description="When the role assignment expires")
    is_active: bool = Field(..., description="Whether the assignment is active") 