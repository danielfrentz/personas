from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_habit_service
from models.habit import Habit
from service.persona_domain.habit_service import HabitService

habit_rest_router = APIRouter(prefix="/habit")
@habit_rest_router.post("/", response_model=Habit)
async def create(persona_id: int, habit: Habit, habit_service: HabitService = Depends(get_habit_service)) -> Habit:
    return habit_service.save(persona_id=persona_id, habit=habit)

@habit_rest_router.get("/", response_model=List[Habit])
async def get_all(persona_id: int, habit_service: HabitService = Depends(get_habit_service)):
    return habit_service.find_by_persona_id(persona_id)


@habit_rest_router.delete("/{habit_id}/")
async def delete(habit_id: int, habit_service: HabitService = Depends(get_habit_service)):
    return habit_service.delete_by_id(habit_id=habit_id)