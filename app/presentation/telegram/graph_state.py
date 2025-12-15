from aiogram.fsm.state import StatesGroup, State

class GraphStates(StatesGroup):
    waiting_hours = State()
    waiting_segments = State()