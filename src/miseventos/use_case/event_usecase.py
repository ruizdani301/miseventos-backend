"""Event use case module.

This module contains the EventUseCase class which handles all business logic
related to event management operations including CRUD operations, pagination,
and time slot relationships.
"""

# Standard library imports
from uuid import UUID

# Local application imports
from miseventos.entitis.event import EventEntity
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import (
    EventImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventNotSlotsResponse,
    EventRequest,
    EventRespose,
    EventsCompletedResponse,
    EventSlotRelationResponse,
    EventUpdateRequest,
)
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response
from miseventos.repositories.event_repository import EventRepository


class EventUseCase:
    """Use case class for event management operations.
    
    This class encapsulates all business logic related to events, including
    validation, CRUD operations, pagination, and filtering.
    
    Attributes:
        event_implement: Repository implementation for event data access.
    """

    def __init__(self, event_implement: EventImplement):
        """Initialize the EventUseCase.
        
        Args:
            event_implement: The event repository implementation instance.
        """
        self.event_implement = event_implement

    def save_event(self, request: EventRequest) -> Response:
        """Create and save a new event.
        
        Validates that no event with the same title exists, validates date ranges
        and capacity, then persists the event to the database.
        
        Args:
            request: Event creation request containing title, description, dates,
                capacity, and status.
        
        Returns:
            Response object with success status and either the created event or
            an error message.
        
        Raises:
            No exceptions raised directly, errors are returned in Response object.
        """
        existing_event = self.event_implement.event_by_simple_title(request.title)
        if existing_event:
            return Response(
                success=False, error_message="Event with this title already exists."
            )
        status_value = (
            request.status.value
            if hasattr(request.status, "value")
            else str(request.status)
        )

        new_event = EventEntity(
            title=request.title,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            capacity=request.capacity,
            status=status_value,
        )
        
        # Validate date range
        if not new_event.validate_dates():
            return Response(success=False, error_message="Invalid date range.")
        
        # Validate capacity
        if not new_event.is_capacity_valid():
            return Response(success=False, error_message="Invalid capacity value.")

        # Save event to repository
        event_saved = self.event_implement.add_event(new_event)

        return Response(success=True, error_message=None, event=event_saved)

    def get_event_paginated(
        self, page: int, limit: int, user_id: UUID = None, title: str = None
    ) -> EventsCompletedResponse:
        """Retrieve paginated events with optional filtering.
        
        Fetches events with their associated sessions, speakers, and time slots.
        Supports filtering by title (case-insensitive) and user-specific registration
        information.
        
        Args:
            page: Page number for pagination (1-indexed).
            limit: Number of events per page.
            user_id: Optional user ID to include user-specific registration data.
            title: Optional title filter for case-insensitive partial matching.
        
        Returns:
            EventsCompletedResponse containing paginated events with metadata
            (total count, page info) or error message if no events found.
        """
        events = self.event_implement.get_events_paginated(
            page=page, limit=limit, user_id=user_id, title=title
        )

        if not events:
            return EventsCompletedResponse(
                success=False, error_message="not events found.", events=None
            )
        
        return EventsCompletedResponse(
            success=True,
            total=events["total"],
            page=events["page"],
            total_pages=events["total_pages"],
            page_size=events["page_size"],
            events=events["data"],
            error_message=None,
        )

    def get_event_by_title(self, title: str) -> EventRespose:
        """Search for events by title.
        
        Performs a case-insensitive partial match search on event titles.
        
        Args:
            title: Search string to match against event titles.
        
        Returns:
            EventsCompletedResponse with matching events or error message if
            no events found.
        """
        event = self.event_implement.get_event_by_title(title)
        if not event:
            return EventsCompletedResponse(
                success=False, error_message="Event by title not found."
            )
        return EventsCompletedResponse(
            success=True,
            events=event["data"],
            error_message=None,
            total=None,
            page=None,
            total_pages=None,
            page_size=None,
        )

    def delete_event(self, event_id: UUID) -> Response:
        """Delete an event by ID.
        
        Removes the event and all associated data (sessions, registrations, etc.)
        due to cascade delete configuration.
        
        Args:
            event_id: UUID of the event to delete.
        
        Returns:
            Response object with success status and deleted event ID or error message.
        """
        deleted_event_id = self.event_implement.del_event(event_id)
        if not deleted_event_id:
            return Response(success=False, error_message="Event not found.")
        return Response(id=deleted_event_id, success=True, error_message=None)

    def update_event(self, request: EventUpdateRequest) -> EventRespose:
        """Update an existing event.
        
        Validates date ranges and capacity before updating the event in the database.
        
        Args:
            request: Event update request containing event ID and updated fields.
        
        Returns:
            EventRespose with success status and updated event or error message.
        """
        status_value = (
            request.status.value
            if hasattr(request.status, "value")
            else str(request.status)
        )

        new_event = EventEntity(
            id=request.id,
            title=request.title,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            capacity=request.capacity,
            status=status_value,
        )
        
        # Validate date range
        if not new_event.validate_dates():
            return EventRespose(success=False, error_message="Invalid date range.")
        
        # Validate capacity
        if not new_event.is_capacity_valid():
            return EventRespose(success=False, error_message="Invalid capacity value.")
        
        event_update = self.event_implement.update_event(new_event)

        if not event_update:
            return EventRespose(
                success=False, error_message="update failed", events=None
            )
        return EventRespose(success=True, error_message=None, events=event_update)

    def get_events_all(self, page: int, limit: int) -> EventRespose:
        """Retrieve all events with pagination (simplified version).
        
        Returns basic event information without associated sessions or speakers.
        
        Args:
            page: Page number for pagination (1-indexed).
            limit: Number of events per page.
        
        Returns:
            EventRespose with paginated events or error message.
        """
        event = self.event_implement.get_events(page=page, limit=limit)

        if not event:
            return EventRespose(
                success=False, error_message="No data available", events=None
            )

        return EventRespose(success=True, error_message=None, events=event)

    def get_event_slot(self) -> EventSlotRelationResponse:
        """Retrieve events with their associated time slots.
        
        Returns:
            EventSlotRelationResponse containing events and their time slot
            relationships or error message if no data available.
        """
        event_slot = self.event_implement.get_event_slot_relation()
        if not event_slot:
            return EventSlotRelationResponse(
                success=False, error_message="No data available", events=None
            )

        return EventSlotRelationResponse(
            success=True, error_message=None, events=event_slot
        )

    def get_event_not_in_slot(self) -> EventNotSlotsResponse:
        """Retrieve events that don't have assigned time slots.
        
        Useful for identifying events that need time slot configuration.
        
        Returns:
            EventNotSlotsResponse containing events without time slots or
            error message if no data available.
        """
        event_slot = self.event_implement.get_event_not_in_timeslot()
        if not event_slot:
            return EventNotSlotsResponse(
                success=False, error_message="No data available", events=None
            )

        return EventNotSlotsResponse(
            success=True, error_message=None, events=event_slot
        )
