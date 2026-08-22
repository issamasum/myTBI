# Copyright (c) 2026 Issa Masumbuko
# SPDX-LIcence-Identifier: MIT

"""Database-backed event models"""

import enum
from datetime import datetime

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String, func
from sqlmodel import Enum, Field, SQLModel


class StatusType(str, enum.Enum):
    """Defines an event's status."""

    ACTIVE = "active"
    ENDED = "ended"
    CANCELED = "canceled"


class CreationType(str, enum.Enum):
    """ Defines how an event was created."""

    MANUAL = "manual"
    SYNCHED = "synced"
    SYSTEM = "system"



class Event(SQLModel, table=True):
    """Represents an event being held at the triangle Baha'i Institute."""

    id: int = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    event_name: str = Field(
        nullable=False
    )
    start_date: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
        default=None
    )
    end_date: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
        default=None
    )
    status: StatusType = Field(
        sa_column=Column(
            Enum(
                StatusType,
                values_callable=lambda e: [m.value for m in e]),
                nullable=True,
            )
    )
    publish: bool = Field(
        default=True
    )
    creation_type: CreationType =  Field(
        sa_column=Column(
            Enum(
                CreationType,
                values_callable=lambda e: [m.value for m in e]),
                nullable=True,
            )
    )
    external_calender_id: str = Field(
        sa_column=Column(String, nullable=True),
        default=None,
    
    )
    created_by: int = Field(
        sa_column=Column(Integer, ForeignKey("user.id"), nullable=False)
    )
    updated_by: int = Field(
            sa_column=Column(Integer, ForeignKey("user.id"), nullable=False)
        )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        default=None,
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
        default=None,
    )


class Checkins(SQLModel, table=True):
    """Represents a checked in visitor at the Triangle Baha'i Institute."""

    id: int = Field(
            sa_column=Column(Integer, primary_key=True, autoincrement=True)
        )
    visitor_name: str = Field(
            nullable=False
    )
    age: int = Field(nullable=True)
    meal: bool = Field(default=False)
    dietary_preferences: list[str] = Field(
        sa_column=Column(ARRAY(String), nullable=True),
        default_factory=list,
    )
    allergies: str = Field(nullable=True)
    purpose: str = Field(nullable=True)
    event_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("event.id"), nullable=True
            )
    )
    user_id: int = Field(
            sa_column=Column(
                Integer, ForeignKey("user.id"), nullable=False
                )
        )
    checked_in_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        default=None,
    )
   