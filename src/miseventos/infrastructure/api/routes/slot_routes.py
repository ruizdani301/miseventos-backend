from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.slot_implement import (
    SlotImplement,
)
from miseventos.use_case.event_usecase import EventUseCase
from miseventos.use_case.slot_usecase import SlotUseCase
from uuid import UUID
from miseventos.infrastructure.api.controllers.slot_controller import (
    add_slot_controller,
    find_slot_by_event_id_controller,
    delete_slot_controller,
    all_slots_controller
)
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotRequest,
)


def register_slotcase(db: Session = Depends(get_db)):
    repo = SlotImplement(
        db
    )  # instancia de UserImplement con la sesión de la base de datos
    return SlotUseCase(repo)  # instancia de UserUseCase con el con user implement


slot_router = APIRouter()


@slot_router.post("/slot/")
async def register_slot(
    body: SlotRequest, usecase: SlotUseCase = Depends(register_slotcase)
):  
    """
    Crea y almacena uno o varios time slots asociados a un evento.

    - Cada slot representa un rango horario (`start_time` – `end_time`).
    - Todos los slots creados pertenecen al mismo evento.
    - Los slots se guardan en una sola operación dentro de la base de datos.
    - Retorna un objeto agrupado que contiene el evento y la lista de slots creados.

    **Parámetros:**
    - **slots**: Lista de objetos `TimeSlot` con la información de los rangos horarios a crear.

    **Respuesta:**
    - Objeto `SlotGroupResponse` con:
      - `id`: Identificador del primer slot creado.
      - `event_id`: ID del evento asociado.
      - `is_assigned`: Indica si los slots están asignados.
      - `created_at`: Fecha de creación.
      - `slots`: Lista de rangos horarios creados.

    **Ejemplo de respuesta:**
    ```json
    {
      "id": "0011fa8d-02aa-436a-b6ff-08122ca08e61",
      "event_id": "483f65c1-1b90-4660-a1ce-5af69252fcb4",
      "is_assigned": false,
      "created_at": "2026-01-10T13:29:10.106907",
      "slots": [
        {
          "start_time": "18:00:00",
          "end_time": "19:00:00"
        },
        {
          "start_time": "19:00:00",
          "end_time": "20:00:00"
        }
      ]
    }
    ```

    **Errores:**
    - Retorna `None` si ocurre un conflicto o no es posible guardar los slots.
    """
    response = add_slot_controller(usecase)
    return await response(body)


@slot_router.delete("/slot/{slot_id}")
async def delete_slot(slot_id: UUID, usecase: SlotUseCase = Depends(register_slotcase)):
    """
        Elimina un slot de tiempo identificado por su ID.

        Busca el slot en la base de datos usando el `slot_id`.  
        Si no existe ningún registro, retorna una respuesta indicando el error.
        Si existe, elimina el slot y confirma la operación en la base de datos.

        Args:
            slot_id (UUID): Identificador único del slot a eliminar.

        Returns:
            Response: 
                - SlotDeleteResponse con `success=True` y el `id` del slot eliminado si la operación fue exitosa.
                - SlotDeleteResponse con `success=False` y un mensaje de error si el slot no existe.
    """
    response = delete_slot_controller(usecase)
    return await response(slot_id)


@slot_router.get("/slot/{event_id}")
async def get_slot_by_event_id(
    event_id: UUID, usecase: SlotUseCase = Depends(register_slotcase)
):
    response = find_slot_by_event_id_controller(usecase)
    return await response(event_id)

@slot_router.get("/slot/")
async def get_all_slots(
    page: int = 1, limit: int = 10, usecase: SlotUseCase = Depends(register_slotcase)
):  
    """
    Obtiene una lista paginada de eventos junto con sus time slots asociados.

    - Cada evento incluye sus datos básicos (id, título, descripción, fecha y capacidad).
    - El campo `time_slots` contiene los rangos horarios relacionados al evento.
    - Los resultados se devuelven ordenados por fecha de creación descendente.

    **Parámetros:**
    - **page**: Número de página (comienza en 1).
    - **limit**: Cantidad máxima de eventos por página.

    **Respuesta:**
    - Lista de eventos con sus respectivos time slots.

    **Ejemplo de respuesta:**
    ```json
    [
      {
        "id": "483f65c1-1b90-4660-a1ce-5af69252fcb4",
        "title": "Evento de prueba",
        "description": "Descripción del evento",
        "start_date": "2026-01-10T10:00:00",
        "capacity": 100,
        "time_slots": [
          {
            "start_time": "18:00:00",
            "end_time": "19:00:00"
          }
        ]
      }
    ]
    ```
    """
    response = all_slots_controller(usecase)
    return await response(page, limit)
