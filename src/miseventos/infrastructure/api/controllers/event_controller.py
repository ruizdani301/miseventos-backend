from fastapi import HTTPException
from miseventos.entitis.event import EventEntity
from miseventos.use_case.event_usecase import EventUseCase
from typing import List
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventRespose,
    EventsCompletedResponse,
    EventRequest,
    EventUpdateRequest,EventSlotRelationResponse, EventNotSlotsResponse
)


def add_event_controller(usecase: EventUseCase):
    async def controller(body: EventRequest) -> EventRespose:
    
        response = usecase.save_event(body)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def find_by_title_controller(usecase: EventUseCase):
    async def controller(title: str) -> List[EventsCompletedResponse]:
        response = usecase.get_event_by_title(title)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response.events

    return controller


def all_events_controller(usecase: EventUseCase):
    async def controller(page: int, limit: int)-> List[EventsCompletedResponse]:
        response = usecase.get_event_paginated(page=page, limit=limit)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def delete_event_controller(usecase: EventUseCase):
    async def controller(event_id: UUID) -> UUID:
        response = usecase.delete_event(event_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller

def update_event_controller(usecase: EventUseCase):
    async def controller(body: EventUpdateRequest):
        response = usecase.update_event(body)

        if not response.success:
            raise HTTPException(
                status_code=400,
                detail=response.error_message
            )

        return response

    return controller

def get_all_events_controller(usecase: EventUseCase):
    async def controller(page: int, limit: int)-> EventRespose:
        response = usecase.get_events_all(page=page, limit=limit)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller

def get_events_slot_controller(usecase: EventUseCase):
    async def controller()-> EventSlotRelationResponse:
        response = usecase.get_event_slot()
        print(response)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)

        return response

    return controller

def get_events_not_slot_controller(usecase: EventUseCase):
    async def controller()-> EventNotSlotsResponse:
        response = usecase.get_event_not_in_slot()
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
     
        return response

    return controller