from fastapi import APIRouter, Depends

from endpoint import get_habit_service
from models.habit import Habit
from service.persona_domain.habit_service import HabitService

habit_generate_router = APIRouter(prefix="/habit")

@habit_generate_router.post("/", response_model=Habit)
async def generate_habit(persona_id: int, universe_id: int, habit_service: HabitService = Depends(get_habit_service)) -> Habit:
    return habit_service.generate(persona_id=persona_id, universe_id=universe_id)