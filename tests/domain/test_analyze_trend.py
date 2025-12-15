from app.domain.weather_analyzer import analyze_trend

import math

def test_no_elemets_trend():
    result = analyze_trend([])
    assert result == 0.0

def test_one_element_trend():
    values: list[float] = [1000]
    result = analyze_trend(values)
    assert result == 0.0

def test_positive_trend():
    values: list[float] = [1000, 1002, 1004]
    result = analyze_trend(values)
    assert result > 0

def test_negative_trend():
    values: list[float] = [1004, 1002, 1000]
    result = analyze_trend(values)
    assert result < 0

def test_flat_trend():
    values: list[float] = [1000, 1000, 1000, 1000, 1000]
    result = analyze_trend(values)
    assert math.ceil(result) == 0.0

def test_almost_flat_trend():
    values: list[float] = [1000, 1001, 1000, 1001, 1000]
    result = analyze_trend(values)
    assert math.ceil(result) < 0.33
