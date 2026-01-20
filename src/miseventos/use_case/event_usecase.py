from miseventos.repositories.event_repository import EventRepository
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import (
    EventImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventRequest,
    EventSlotRelationResponse
)
from miseventos.entitis.event import EventEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventRespose, EventsCompletedResponse, EventUpdateRequest
)
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response


class EventUseCase:
    def __init__(self, event_implement: EventImplement):
        self.event_implement = event_implement

    def save_event(self, request: EventRequest) -> Response:
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
            status=status_value
        )
        #Validate  format
        if not new_event.validate_dates():
            return Response(success=False, error_message="Invalid date range.")
        if not new_event.is_capacity_valid():
            return Response(success=False, error_message="Invalid capacity value.")

        # # Save event  to repository
        event_saved = self.event_implement.add_event(new_event)
     

        return Response(success=True, error_message=None, event=event_saved)

    def get_event_paginated(self, page: int, limit: int) -> EventsCompletedResponse:
        events = self.event_implement.get_events_paginated(page=page, limit=limit)

        if not events:
            return EventsCompletedResponse(success=False, error_message="not events found.")
        return EventsCompletedResponse(success=True,
                                       events=events["data"],
                                       total=events["total"],
                                       page=events["page"],
                                       total_pages=events["total_pages"],
                                       page_size=events["page_size"],
                                       error_message=None)

    def get_event_by_title(self, title: str) -> EventRespose:
        event = self.event_implement.get_event_by_title(title)
        if not event:
            return EventsCompletedResponse(success=False, error_message="Event by title not found.")
        return EventsCompletedResponse(success=True, events=event["data"],
                                       error_message=None,
                                       total=None,
                                       page=None,
                                       total_pages=None,
                                       page_size=None)

    def delete_event(self, event_id: UUID) -> Response:
        deleted_event_id = self.event_implement.del_event(event_id)
        if not deleted_event_id:
            return Response(success=False, error_message="Event not found.")
        return Response(id=deleted_event_id, success=True, error_message=None)
    
    def update_event(self, request: EventUpdateRequest) -> EventRespose:

        
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
            status=status_value
        )
        #Validate  format
        if not new_event.validate_dates():
            return EventRespose(success=False, error_message="Invalid date range.")
        if not new_event.is_capacity_valid():
            return EventRespose(success=False, error_message="Invalid capacity value.")
        event_update = self.event_implement.update_event(new_event)
  
        if not event_update:
            return EventRespose(success=False, error_message= "update failed", events=None)
        return EventRespose(success=True, error_message= None, events=event_update)
 
    
    def get_events_all(self, page:int, limit:int)->EventRespose:
        event = self.event_implement.get_events(page=page, limit=limit)
        
        if not event:
            return EventRespose(success=False, error_message= "No data available", events=None)
        
        return EventRespose(success=True, error_message= None, events=event)
  

    def get_event_slot(self)-> EventSlotRelationResponse:
        event_slot = self.event_implement.get_event_slot_relation()
        
        if not event_slot:
            return EventSlotRelationResponse(success=False, error_message= "No data available", events=None)
        
        return EventSlotRelationResponse(success=True, error_message= None, events=event_slot)