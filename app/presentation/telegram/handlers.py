from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from application.weather_service import WeatherService
from .graph_builder import build_weather_graph
from .graph_state import GraphStates

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌤 Текущая погода", callback_data="current"),
        ],
        [
            InlineKeyboardButton(text="🔮 Прогноз", callback_data="predict"),
        ],
        [
            InlineKeyboardButton(text="📊 График", callback_data="graph"),
        ]
    ]
)
router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать, выберите действие\n",
        reply_markup=main_menu
    )

@router.callback_query(F.data == "current")
async def current_handler(callback: CallbackQuery, weather_service: WeatherService):
    weather = await weather_service.get_current()

    if weather is None:
        await callback.message.answer("Нет данных о погоде", reply_markup=main_menu)
        return

    msg = (
        "🌤 Погода в данный момент:\n"
        f"🌡 Температура: {weather.temperature}°C\n"
        f"💧 Влажность: {weather.humidity}%\n"
        f"🔽 Давление: {weather.pressure} hPa"
    )
    if callback.message.text != msg:
        await callback.message.edit_text(msg, reply_markup=main_menu)

    await callback.answer()

@router.callback_query(F.data == "predict")
async def predict_handler(callback: CallbackQuery, weather_service: WeatherService):
    result = await weather_service.predict()
    if callback.message.text != result:
        await callback.message.edit_text(result, reply_markup=main_menu)

    await callback.answer()


@router.callback_query(F.data == "graph")
async def graph_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("За сколько часов построить график? (например: 6)")
    await callback.answer()
    await state.set_state(GraphStates.waiting_hours)

@router.message(GraphStates.waiting_hours)
async def graph_hours(message: Message, state: FSMContext):
    try:
        hours = int(message.text)
        if not (1 <= hours <= 24):
            raise ValueError
    except ValueError:
        await message.answer("Введите число от 1 до 24")
        return

    await state.update_data(hours=hours)
    await message.answer("На сколько сегментов разбить? (например: 12)")
    await state.set_state(GraphStates.waiting_segments)

@router.message(GraphStates.waiting_segments)
async def graph_segments(
    message: Message,
    state: FSMContext,
    weather_service: WeatherService
):
    try:
        segments = int(message.text)
        if not (2 <= segments <= 512):
            raise ValueError
    except ValueError:
        await message.answer("Введите число от 2 до 512")
        return

    data = await state.get_data()
    hours = data["hours"]

    segments_data = await weather_service.get_graph_data(
        hours=hours,
        segments=segments
    )

    image = build_weather_graph(segments_data)
    await message.answer_photo(image)
    await message.answer("выберите действие", reply_markup=main_menu)

    await state.clear()

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена", reply_markup=main_menu)
