# Copyright (c) 2026 Issa Masumbuko
# SPDX-License-Identifier: MIT

"""Pydantic models for checkin at TBI API requests and responses."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel


# ----Enums-----------

class EventStatus(str, Enum):
    """Defines an event's status."""

    ACTIVE = "active"
    ENDED = "ended"
    CANCELED = "canceled"


class EventCreationType(str, Enum):
    """ Defines how an event was created."""

    MANUAL = "manual"
    SYNCED = "synced"
    SYSTEM = "system"

class DietaryPreference(str, Enum):
    """Defines various options for dietary preferences."""

    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    HALAL = "halal"
    KOSHER = "kosher"
    OTHER = "other"



# -----Events----------


class CreateEventRequest(BaseModel):
    """Payload for updating an event."""

    event_name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    publish: bool = False


class UpdateEventRequest(BaseModel):
    """Payload for creating an event."""

    event_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    publish: Optional[bool] = None
    status: Optional[EventStatus] = None


class EventResponse(BaseModel):
    """Response for a created event."""

    id: int
    event_name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: EventStatus
    publish: bool 
    creation_type: EventCreationType
    external_calender_id: Optional[str] = None
    created_at: datetime
    updated_by: int
    updated_at: datetime


# -----Checkins---------


class CreateGeneralCheckinRequest(BaseModel):
    """Payload for a general check in not associated with an event."""

    purpose: str


class CreateCheckinRequest(BaseModel):
    """Payload for checking in at the TBI."""

    visitor_name: str
    age: Optional[int] = None
    meal: bool = False
    dietary_preferences: list[DietaryPreference] = []
    allergies: Optional[str] = None


class UpdateCheckinRequest(BaseModel):
    """Payload for checking in at the TBI."""

    visitor_name: Optional[str] = None
    age: Optional[int] = None
    meal: Optional[bool] = None
    dietary_preferences: Optional[list[DietaryPreference]] = None
    allergies: Optional[str] = None


class CheckinResponse(BaseModel):
    """Payload for checking in at the TBI."""

    id: int
    visitor_name: str
    age: Optional[int] = None
    meal: Optional[bool] = None
    dietary_preferences: list[DietaryPreference] = []
    allergies: Optional[str] = None
    event_id: Optional[int] = None
    user_id: Optional[int] = None
    purpose: Optional[str] = None
    checked_in_at: datetime
