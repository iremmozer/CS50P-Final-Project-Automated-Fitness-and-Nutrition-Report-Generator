import pytest
from project import (calculate_bmr,analyze_body_composition,calculate_water_intake,calculate_nutrition_plan,calculate_weight_projection,calculate_composition_changes,calculate_healthy_weight)

def test_calculate_bmr():
    assert calculate_bmr("F", 55, 165, 20, 2) == (20.2, 1320, 1815)
    assert calculate_bmr("M", 90, 180, 35, 2) == (27.8, 1855, 2551)
    assert calculate_bmr("F", 70, 163, 43, 4) == (26.3, 1343, 2316)

def test_analyze_body_composition():
    assert analyze_body_composition(67, 30, 95, "F", 165, 55) == (24.33, 13.38, 41.62, 22.47)
    assert analyze_body_composition(60, 30, 87, "F", 160, 50) == (17.44, 8.72, 41.28, 22.29)
    assert analyze_body_composition(86, 39,  0, "M", 178, 78) == (16.44, 12.82, 65.18, 35.20)

def test_calculate_water_intake():
    assert calculate_water_intake(60, "F") == (2.0)
    assert calculate_water_intake(50, "F") == (1.7)
    assert calculate_water_intake(60, "M") == (2.1)

def test_calculate_nutrition_plan():
    assert calculate_nutrition_plan("F", 4, 1800, 1) == (1500, 320, 80, 720, 180, 450, 50)
    assert calculate_nutrition_plan("F", 4, 1800, 2) == (1400, 320, 80, 680, 170, 450, 50)
    assert calculate_nutrition_plan("F", 3, 1600, 1) == (1600, 320, 80, 800, 200, 450, 50)
    assert calculate_nutrition_plan("M", 1, 2000, 1) == (2300, 480, 120, 1280, 320, 540, 60)
    assert calculate_nutrition_plan("M", 2, 2600, 2) == (2450, 600, 150, 1240, 310, 630, 70)

def test_calculate_weight_projection():
    assert calculate_weight_projection(1600,1800, 50) == (50.7, 51.4, {"Current Weight": 50, "Week 4 (Expected)": 50.7, "Week 8 (Expected)": 51.4}, 0.7)
    assert calculate_weight_projection(2000, 1700, 60) == (58.9, 57.8, {"Current Weight": 60, "Week 4 (Expected)": 58.9, "Week 8 (Expected)": 57.8}, 1.1)
    assert calculate_weight_projection(2400, 2600, 70) == (70.7, 71.4, {"Current Weight": 70, "Week 4 (Expected)": 70.7, "Week 8 (Expected)": 71.4}, 0.7)
    assert calculate_weight_projection(2500, 2500, 80) == (80, 80, {"Current Weight": 80, "Week 4 (Expected)": 80, "Week 8 (Expected)": 80}, 0.0)

def test_calculate_composition_changes():
    assert calculate_composition_changes(1.0, 25.0, 15.0, 25.0, 1, 60) == (25.55, 15.45, 25.33, 26.1, 15.9, 25.65)
    assert calculate_composition_changes(0.0, 22.0, 14.0, 25.0, 2, 56) == (22.5, 13.5, 24.11, 23.0, 13.0, 23.21)
    assert calculate_composition_changes(0.0, 24.0, 12.0, 20.0, 3, 60) == (24.0, 12.0, 20.0, 24.0, 12.0, 20.0)
    assert calculate_composition_changes(1.0, 28.0, 20.0, 25.0, 4, 80) == (27.85, 19.15, 24.24, 27.7, 18.3, 23.46)

def test_calculate_healthy_weight():
    assert calculate_healthy_weight(165) == (50.4, 67.8)
    assert calculate_healthy_weight(180) == (59.9, 80.7)
    assert calculate_healthy_weight(150) == (41.6, 56.0)

