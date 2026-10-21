
#  CS50P Final Project: Automated Fitness & Nutrition Report Generator
# Otomatik Fitness ve Beslenme Raporu Oluşturucu
import re
import math
import matplotlib.pyplot as plt
from fpdf import FPDF

def calculate_bmr(gender, weight, height_cm, age, activity_level):
    if gender == "F":
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5

    bmi = weight / (height_cm / 100) ** 2

    multipliers = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725}
    tdee = multipliers[activity_level] * bmr

    return round(bmi,1),round(bmr),round(tdee)

def analyze_body_composition(waist, neck, hip, gender, height_cm, weight):
    if gender == "F":
        log_value = math.log10(waist + hip - neck)
        log_h = math.log10(int(height_cm))
        body_fat_percentage = 495 / (1.29579 - 0.35004 * log_value + 0.22100 * log_h) - 450
        fat_mass = weight * (body_fat_percentage / 100)
        lean_mass = weight - fat_mass
        skeletal_muscle_mass = lean_mass * 0.54
    else:
        log_value = math.log10(waist - neck)
        log_h = math.log10(int(height_cm))
        body_fat_percentage = 495 / (1.0324 - 0.19077 * log_value + 0.15456 * log_h) - 450
        fat_mass = weight * (body_fat_percentage / 100)
        lean_mass = weight - fat_mass
        skeletal_muscle_mass = lean_mass * 0.54

    return round(body_fat_percentage,2), round(fat_mass,2), round(lean_mass,2), round(skeletal_muscle_mass,2)

def calculate_water_intake(weight, gender):#
    if gender == "F":
        recommended_water_l = weight * 0.033
    else:
        recommended_water_l = weight * 0.035

    return  round(recommended_water_l,1)

def get_recommended_goal(gender, body_fat_percentage, bmi):#
    if gender == "F":
        if body_fat_percentage < 16 or bmi < 18.5:
            return (
                "Recommended Biological Goal --> Weight Gain\n\n"
                "Biological Rationale: A slight caloric surplus is essential to preserve hormonal balance, "
                "prevent bone density loss, and promote lean tissue accretion."
            )
        elif 16 <= body_fat_percentage < 21 or 18.5 <= bmi <= 24.9:
            return (
                "Recommended Biological Goal --> Muscle Gain / Body Recomposition\n\n"
                "Biological Rationale: The individual is already within an optimal/fit body fat range; "
                "muscle mass can be developed while oxidizing fat without significantly altering scale weight "
                "(maintaining near maintenance calories or a very mild deficit)."
            )
        elif 21 <= body_fat_percentage <= 25 or 18.5 <= bmi <= 23.5:
            return (
                "Recommended Biological Goal --> Maintenance / Energy Balance\n\n"
                "Biological Rationale: This is the most metabolically and hormonally sustainable range. "
                "Energy balance (calories in = calories out) is prioritized."
            )
        elif body_fat_percentage >= 25 or bmi >= 25:
            return (
                "Recommended Biological Goal --> Fat Loss / Weight Reduction\n\n"
                "Biological Rationale: A controlled caloric deficit is targeted to enhance insulin sensitivity, "
                "reduce visceral adiposity, and promote fat loss."
            )
    else:
        if body_fat_percentage < 10 or bmi < 18.5:
            return (
                "Recommended Biological Goal --> Weight Gain\n\n"
                "Biological Rationale: A caloric surplus is required for optimal anabolic hormonal profiles, "
                "testosterone production, and skeletal muscle hypertrophy."
            )
        elif 10 <= body_fat_percentage < 15 or 18.5 <= bmi <= 24.9:
            return (
                "Recommended Biological Goal --> Muscle Gain / Body Recomposition\n\n"
                "Biological Rationale: Insulin sensitivity is heightened and nutrient partitioning favors muscle tissue; "
                "lean muscle accretion is achievable at maintenance calories."
            )
        elif 15 <= body_fat_percentage <= 18 or 18.5 <= bmi <= 24:
            return (
                "Recommended Biological Goal --> Maintenance / Energy Balance\n\n"
                "Biological Rationale: Represents the most stable physiological state for strength, aesthetics, "
                "and overall metabolic health markers."
            )
        elif body_fat_percentage >= 18 or bmi >= 25:
            return (
                "Recommended Biological Goal --> Fat Loss / Weight Reduction\n\n"
                "Biological Rationale: When body fat exceeds optimal thresholds, anabolic signaling diminishes; "
                "a controlled deficit is advised to bring body fat back into the 12-15% target range."
            )

def calculate_nutrition_plan(gender, goal_id, tdee, month=1):#
    if gender == "F":
        if goal_id == 1:
            target_calories = tdee * 1.12
            if month == 2:
                target_calories += 100
            protein_calories = target_calories * 0.20
            protein = protein_calories / 4
            carb_calories = target_calories * 0.55
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.25
            fat = fat_calories / 9
        elif goal_id == 2:
            target_calories = tdee * 0.95
            protein_calories = target_calories * 0.24
            protein = protein_calories / 4
            carb_calories = target_calories * 0.46
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.30
            fat = fat_calories / 9
        elif goal_id == 3:
            target_calories = tdee
            protein_calories = target_calories * 0.20
            protein = protein_calories / 4
            carb_calories = target_calories * 0.50
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.30
            fat = fat_calories / 9
        else:
            target_calories = tdee * 0.82
            if month == 2:
                target_calories -= 100
            protein_calories = target_calories * 0.22
            protein = protein_calories / 4
            carb_calories = target_calories * 0.48
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.30
            fat = fat_calories / 9

        if fat < 40:
            fat = 40
            fat_calories = 360
            carb_calories = target_calories - (protein_calories + fat_calories)
            carbs = carb_calories / 4
    else:
        if goal_id == 1:
            target_calories = tdee * 1.15
            if month == 2:
                target_calories += 150
            protein_calories = target_calories * 0.20
            protein = protein_calories / 4
            carb_calories = target_calories * 0.55
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.25
            fat = fat_calories / 9
        elif goal_id == 2:
            target_calories = tdee * 0.95
            protein_calories = target_calories * 0.25
            protein = protein_calories / 4
            carb_calories = target_calories * 0.50
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.25
            fat = fat_calories / 9
        elif goal_id == 3:
            target_calories = tdee
            protein_calories = target_calories * 0.20
            protein = protein_calories / 4
            carb_calories = target_calories * 0.55
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.25
            fat = fat_calories / 9
        else:
            target_calories = tdee * 0.80
            if month == 2:
                target_calories -= 150
            protein_calories = target_calories * 0.28
            protein = protein_calories / 4
            carb_calories = target_calories * 0.47
            carbs = carb_calories / 4
            fat_calories = target_calories * 0.25
            fat = fat_calories / 9

    target_calories = int(round(target_calories / 50) * 50)
    carbs = int(round(carbs, -1))
    protein = int(round(protein, -1))
    fat = int(round(fat, -1))

    protein_calories = protein * 4
    carb_calories = carbs * 4
    fat_calories = fat * 9

    return target_calories, protein_calories, protein, carb_calories, carbs, fat_calories, fat

def distribute_meal_macros(target_calories, protein, carbs, fat, meals_count):#
    if meals_count == 2:
        meal_macros = {
            "Meal-1 (Breakfast)": {
                "Total Meal Energy": f"{round(target_calories * 0.45)} kcal",
                "Carbohydrates": f"{round(carbs * 0.45)} grams --> {round(carbs * 0.45) * 4} kcal",
                "Protein": f"{round(protein * 0.45)} grams --> {round(protein * 0.45) * 4} kcal",
                "Fat": f"{round(fat * 0.45)} grams --> {round(fat * 0.45) * 9} kcal",
            },
            "Meal-2 (Dinner)": {
                "Total Meal Energy": f"{round(target_calories * 0.45)} kcal",
                "Carbohydrates": f"{round(carbs * 0.45)} grams --> {round(carbs * 0.45) * 4} kcal",
                "Protein": f"{round(protein * 0.45)} grams --> {round(protein * 0.45) * 4} kcal",
                "Fat": f"{round(fat * 0.45)} grams --> {round(fat * 0.45) * 9} kcal",
            },
            "Snack": {
                "Total Meal Energy": f"{round(target_calories * 0.1)} kcal",
                "Carbohydrates": f"{round(carbs * 0.1)} grams --> {round(carbs * 0.1) * 4} kcal",
                "Protein": f"{round(protein * 0.1)} grams --> {round(protein * 0.1) * 4} kcal",
                "Fat": f"{round(fat * 0.1)} grams --> {round(fat * 0.1) * 9} kcal",
            },
        }
    else:
        meal_macros = {
            "Meal-1 (Breakfast)": {
                "Total Meal Energy": f"{round(target_calories * 0.30)} kcal",
                "Carbohydrates": f"{round(carbs * 0.30)} grams --> {round(carbs * 0.30) * 4} kcal",
                "Protein": f"{round(protein * 0.30)} grams --> {round(protein * 0.30) * 4} kcal",
                "Fat": f"{round(fat * 0.30)} grams --> {round(fat * 0.30) * 9} kcal",
            },
            "Meal-2 (Lunch)": {
                "Total Meal Energy": f"{round(target_calories * 0.35)} kcal",
                "Carbohydrates": f"{round(carbs * 0.35)} grams --> {round(carbs * 0.35) * 4} kcal",
                "Protein": f"{round(protein * 0.35)} grams --> {round(protein * 0.35) * 4} kcal",
                "Fat": f"{round(fat * 0.35)} grams --> {round(fat * 0.35) * 9} kcal",
            },
            "Meal-3 (Dinner)": {
                "Total Meal Energy": f"{round(target_calories * 0.25)} kcal",
                "Carbohydrates": f"{round(carbs * 0.25)} grams --> {round(carbs * 0.25) * 4} kcal",
                "Protein": f"{round(protein * 0.25)} grams --> {round(protein * 0.25) * 4} kcal",
                "Fat": f"{round(fat * 0.25)} grams --> {round(fat * 0.25) * 9} kcal",
            },
            "Snack": {
                "Total Meal Energy": f"{round(target_calories * 0.1)} kcal",
                "Carbohydrates": f"{round(carbs * 0.1)} grams --> {round(carbs * 0.1) * 4} kcal",
                "Protein": f"{round(protein * 0.1)} grams --> {round(protein * 0.1) * 4} kcal",
                "Fat": f"{round(fat * 0.1)} grams --> {round(fat * 0.1) * 9} kcal",
            },
        }
    return meal_macros

def generate_workout_plan(workout_environment, activity_level):#
    if workout_environment == 1:
        # Home / Mat Workouts
        if activity_level == 1:
            workout_schedule = {
                "Monday": "Low-Intensity Walk & Mobility (25 min: 20 min indoor/outdoor brisk walk, 5 min shoulder and neck circles)",
                "Tuesday": "Rest & Postural Realignment (15 min: Cat-cow, back and chest stretches on mat)",
                "Wednesday": "Low-Intensity Walk & Joint Mobility (30 min: 25 min steady pacing, 5 min ankle and knee mobilization)",
                "Thursday": "Full Rest (Light indoor movement)",
                "Friday": "Full-Body Gentle Stretch & Breathing (20 min: 15 min static stretching, 5 min diaphragmatic breathing)",
                "Saturday": "Active Walking (30 min: Comfortable continuous walk)",
                "Sunday": "Full Rest (Rest Day)",
            }
        elif activity_level == 2:
            workout_schedule = {
                "Monday": "Full-Body Foundational Strength (35 min: 5 min dynamic warm-up, 25 min chair squats, knee push-ups, glute bridges, 5 min cool-down)",
                "Tuesday": "Rest & Daily Step Goal (Light unstructured movement)",
                "Wednesday": "LISS Cardio & Core (30 min: 20 min steady-state home cardio steps, 10 min planks and deadbugs)",
                "Thursday": "Full Rest (Muscle recovery)",
                "Friday": "Lower Body & Posture-Focused Mat (35 min: 5 min warm-up, 25 min lunges, thoracic openers, glute activation, 5 min static stretches)",
                "Saturday": "Outdoor / Brisk Walk (35 min: Moderate tempo walking + 5 min leg stretches)",
                "Sunday": "Full Rest (Rest Day)",
            }
        elif activity_level == 3:
            workout_schedule = {
                "Monday": "Full-Body Resistance & Mat Strength (45 min: 5 min dynamic warm-up, 35 min squats, push-ups, glute bridges, core combination, 5 min cool-down)",
                "Tuesday": "LISS Cardio & Mobility (40 min: 30 min brisk walk/step workout, 10 min hip and spinal mobility exercises)",
                "Wednesday": "Lower Body & Core (45 min: 5 min warm-up, 35 min lunge variations, donkey kicks, obliques circuit, 5 min stretch)",
                "Thursday": "Active Recovery & Postural Mobility (25 min: 15 min gentle stretching, 10 min joint mobility)",
                "Friday": "Upper Body & Posture Reinforcement (40 min: 5 min mobilization, 30 min back, shoulder, arm, deep core circuits, 5 min stretch)",
                "Saturday": "Functional Cardio / HIIT (30 min: 5 min warm-up, 20 min high-effort intervals, 5 min heart rate cool-down)",
                "Sunday": "Full Rest (Rest Day)",
            }
        else:
            workout_schedule = {
                "Monday": "Advanced Lower Body Resistance (50 min: 5 min dynamic activation, 40 min single-leg squats, jump lunges, glute and leg circuits, 5 min cool-down)",
                "Tuesday": "Upper Body Push/Pull Resistance (45 min: 5 min warm-up, 35 min push-up variations, dumbbell/band back and shoulders, 5 min stretch)",
                "Wednesday": "High-Intensity Interval Cardio / HIIT (35 min: 5 min warm-up, 25 min elevated heart-rate functional circuits, 5 min cool-down)",
                "Thursday": "Core & Deep Mobility (40 min: 25 min intensive core stabilization, 15 min yoga/mobility flow)",
                "Friday": "Full-Body Metabolic Conditioning (50 min: 5 min warm-up, 40 min supersetted full-body mat strength, 5 min stretch)",
                "Saturday": "Brisk LISS Cardio & Stretching (45 min: 35 min brisk walk/treadmill, 10 min full-body static stretches)",
                "Sunday": "Full Rest (Central nervous system recovery)",
            }
    else:
        # Gym Workouts
        if activity_level == 1:
            workout_schedule = {
                "Monday": "Full-Body Machine Adaptation (35 min: 5 min treadmill warm-up, 25 min Leg Press, Lat Pulldown, Chest Press machines, 5 min stretch)",
                "Tuesday": "Rest (Light daily walk)",
                "Wednesday": "Low-Intensity Gym Cardio (30 min: Incline treadmill or recumbent bike at steady heart rate)",
                "Thursday": "Full Rest",
                "Friday": "Full-Body Foundational Resistance (35 min: 5 min warm-up, 25 min Seated Cable Row, Shoulder Press machine, abdominal curls, 5 min stretch)",
                "Saturday": "Active Walking / Cycling (30 min: Relaxed pace on elliptical or stationary bike)",
                "Sunday": "Full Rest (Rest Day)",
            }
        elif activity_level == 2:
            workout_schedule = {
                "Monday": "Lower Body & Leg Focus (45 min: 5 min warm-up, 35 min Goblet Squats, Leg Curls, Leg Extensions, Calf Raises, 5 min stretch)",
                "Tuesday": "Rest (Free daily step target)",
                "Wednesday": "Upper Body Push/Pull Combination (45 min: 5 min shoulder warm-up, 35 min Dumbbell Bench Press, Lat Pulldowns, Cable Rows, Lateral Raises, 5 min stretch)",
                "Thursday": "Full Rest (Muscle recovery)",
                "Friday": "Full-Body Strength & Core (45 min: 5 min warm-up, 30 min deadlift variations, dumbbell shoulder press, 10 min plank/cable crunches)",
                "Saturday": "Cardio & Mobility (35 min: 25 min incline treadmill walk, 10 min leg and chest stretches)",
                "Sunday": "Full Rest (Rest Day)",
            }
        elif activity_level == 3:
            workout_schedule = {
                "Monday": "Lower Body Hypertrophy (60 min: 8 min dynamic mobility, 45 min Barbell/Dumbbell Squats, Leg Press, Romanian Deadlifts, Lunges, 7 min static stretches)",
                "Tuesday": "Push Day (Chest, Shoulders, Triceps) (55 min: 8 min shoulder mobilization, 40 min Incline/Flat Bench Press, Overhead Press, Lateral Raises, Triceps Pushdowns, 7 min stretch)",
                "Wednesday": "LISS Cardio & Core (45 min: 30 min incline treadmill/rower LISS cardio, 15 min Cable Crunches, Hanging Leg Raises, Planks)",
                "Thursday": "Pull Day (Back, Rear Delts, Biceps) (55 min: 8 min back activation, 40 min Lat Pulldowns, Seated Cable Rows, Face Pulls, Biceps Curls, 7 min lat stretches)",
                "Friday": "Lower Body Focus 2 (Glutes & Hamstrings) (55 min: 8 min glute activation, 40 min Barbell Hip Thrusts, Lying Leg Curls, Bulgarian Split Squats, Calf Raises, 7 min stretch)",
                "Saturday": "Active Recovery & Functional Cardio (40 min: 25 min moderate cardio, 15 min foam rolling and deep stretching)",
                "Sunday": "Full Rest (Central nervous system renewal)",
            }
        else:
            workout_schedule = {
                "Monday": "Push Day (Heavy Chest, Shoulders, Triceps) (65 min: 10 min warm-up, 50 min free-weight push stations to failure, 5 min cool-down)",
                "Tuesday": "Pull Day (Heavy Back, Rear Delts, Biceps) (65 min: 10 min mobility, 50 min deadlift/row variations, lat isolations, 5 min stretch)",
                "Wednesday": "Lower Body (Quad-Dominant) (65 min: 10 min hip/knee activation, 50 min Back Squats, Hack Squats, Walking Lunges, Leg Extensions, 5 min stretch)",
                "Thursday": "Upper Body Hypertrophy & Core (55 min: 8 min warm-up, 35 min superset dumbbell/cable pump, 12 min weighted core circuits)",
                "Friday": "Lower Body (Glute & Hamstring Dominant) (60 min: 8 min activation, 45 min RDLs, Hip Thrusts, Seated Leg Curls, Calves, 7 min stretch)",
                "Saturday": "Conditioning & HIIT Cardio (40 min: 8 min warm-up, 25 min rower/air bike interval sprints, 7 min foam rolling)",
                "Sunday": "Full Rest (Rest Day)",
            }

    return workout_schedule
def calculate_weight_projection(tdee, target_calories_1, weight):#
    diff = target_calories_1 - tdee

    if diff < 0:
        diff = -1 * diff
        monthly_diff = diff * 28
        monthly_change = round(monthly_diff / 7700, 1)
        month_1_end = round(weight - monthly_change, 1)
        month_2_end = round(month_1_end - monthly_change, 1)
    elif diff == 0:
        monthly_change = 0.0
        month_1_end = weight
        month_2_end = weight
    else:
        monthly_diff = diff * 28
        monthly_change = round(monthly_diff / 7700, 1)
        month_1_end = round(weight + monthly_change, 1)
        month_2_end = round(month_1_end + monthly_change, 1)

    weight_projection_table = {
        "Current Weight": weight,
        "Week 4 (Expected)": month_1_end,
        "Week 8 (Expected)": month_2_end,
    }

    return month_1_end, month_2_end, weight_projection_table, monthly_change
def calculate_composition_changes(monthly_change, skeletal_muscle_mass, fat_mass, body_fat_percentage, goal_id, weight):#
    if goal_id == 1:
        muscle_change_1 = round(skeletal_muscle_mass + (monthly_change * 0.55), 2)
        fat_mass_change_1 = round(fat_mass + (monthly_change * 0.45), 2)
        fat_pct_change_1 = round((fat_mass_change_1 / (weight + monthly_change)) * 100, 2)

        muscle_change_2 = round(skeletal_muscle_mass + (monthly_change * 2 * 0.55), 2)
        fat_mass_change_2 = round(fat_mass + (monthly_change * 2 * 0.45), 2)
        fat_pct_change_2 = round((fat_mass_change_2 / (weight + (monthly_change * 2))) * 100, 2)

    elif goal_id == 2:
        muscle_change_1 = round(skeletal_muscle_mass + 0.50, 2)
        fat_mass_change_1 = round(fat_mass - 0.50, 2)
        fat_pct_change_1 = round((fat_mass_change_1 / weight) * 100, 2)

        muscle_change_2 = round(skeletal_muscle_mass + 1.00, 2)
        fat_mass_change_2 = round(fat_mass - 1.00, 2)
        fat_pct_change_2 = round((fat_mass_change_2 / weight) * 100, 2)

    elif goal_id == 3:
        muscle_change_1 = round(skeletal_muscle_mass, 2)
        fat_mass_change_1 = round(fat_mass, 2)
        fat_pct_change_1 = round(body_fat_percentage, 2)

        muscle_change_2 = round(skeletal_muscle_mass, 2)
        fat_mass_change_2 = round(fat_mass, 2)
        fat_pct_change_2 = round(body_fat_percentage, 2)

    else:
        muscle_change_1 = round(skeletal_muscle_mass - (monthly_change * 0.15), 2)
        fat_mass_change_1 = round(fat_mass - (monthly_change * 0.85), 2)
        fat_pct_change_1 = round((fat_mass_change_1 / (weight - monthly_change)) * 100, 2)

        muscle_change_2 = round(skeletal_muscle_mass - (monthly_change * 2 * 0.15), 2)
        fat_mass_change_2 = round(fat_mass - (monthly_change * 2 * 0.85), 2)
        fat_pct_change_2 = round((fat_mass_change_2 / (weight - (monthly_change * 2))) * 100, 2)

    return muscle_change_1, fat_mass_change_1, fat_pct_change_1, muscle_change_2, fat_mass_change_2, fat_pct_change_2
def generate_progress_charts(
    weight,
    month_1_end,
    month_2_end,
    skeletal_muscle_mass,
    muscle_change_1,
    muscle_change_2,
    fat_mass,
    fat_mass_change_1,
    fat_mass_change_2,
    body_fat_percentage,
    fat_pct_change_1,
    fat_pct_change_2,
): #
    timeline = ["Current", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]

    weight_step_1 = (month_1_end - weight) / 4
    weight_step_2 = (month_2_end - month_1_end) / 4
    weight_data = [
        weight,
        weight_step_1 + weight,
        (weight_step_1 * 2) + weight,
        (weight_step_1 * 3) + weight,
        month_1_end,
        month_1_end + weight_step_2,
        month_1_end + (weight_step_2 * 2),
        month_1_end + (weight_step_2 * 3),
        month_2_end,
    ]

    muscle_step_1 = (muscle_change_1 - skeletal_muscle_mass) / 4
    muscle_step_2 = (muscle_change_2 - muscle_change_1) / 4
    muscle_data = [
        skeletal_muscle_mass,
        skeletal_muscle_mass + muscle_step_1,
        (muscle_step_1 * 2) + skeletal_muscle_mass,
        (muscle_step_1 * 3) + skeletal_muscle_mass,
        muscle_change_1,
        muscle_step_2 + muscle_change_1,
        (muscle_step_2 * 2) + muscle_change_1,
        (muscle_step_2 * 3) + muscle_change_1,
        muscle_change_2,
    ]

    fat_mass_step_1 = (fat_mass_change_1 - fat_mass) / 4
    fat_mass_step_2 = (fat_mass_change_2 - fat_mass_change_1) / 4
    fat_mass_data = [
        fat_mass,
        fat_mass + fat_mass_step_1,
        fat_mass + (fat_mass_step_1 * 2),
        fat_mass + (fat_mass_step_1 * 3),
        fat_mass_change_1,
        fat_mass_change_1 + fat_mass_step_2,
        fat_mass_change_1 + (fat_mass_step_2 * 2),
        fat_mass_change_1 + (fat_mass_step_2 * 3),
        fat_mass_change_2,
    ]

    fat_pct_step_1 = (fat_pct_change_1 - body_fat_percentage) / 4
    fat_pct_step_2 = (fat_pct_change_2 - fat_pct_change_1) / 4
    fat_pct_data = [
        body_fat_percentage,
        body_fat_percentage + fat_pct_step_1,
        body_fat_percentage + (fat_pct_step_1 * 2),
        body_fat_percentage + (fat_pct_step_1 * 3),
        fat_pct_change_1,
        fat_pct_change_1 + fat_pct_step_2,
        fat_pct_change_1 + (fat_pct_step_2 * 2),
        fat_pct_change_1 + (fat_pct_step_2 * 3),
        fat_pct_change_2,
    ]

    plt.figure(figsize=(12, 16))

    # Subplot 1: Weight Progression
    plt.subplot(2, 2, 1)
    plt.title("Expected Weight Progression")
    plt.plot(timeline, weight_data, marker="o", color="blue", linewidth=2, label="Weight (kg)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.xlabel("Weeks", labelpad=8, fontsize=8.5)
    plt.xticks(rotation=30, ha="right", fontsize=7.5)
    plt.ylabel("Weight (kg)")
    for x, y in zip(timeline, weight_data):
        plt.annotate(
            f"{y:.2f} kg",
            (x, y),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    # Subplot 2: Skeletal Muscle Mass Progression
    plt.subplot(2, 2, 2)
    plt.title("Expected Skeletal Muscle Mass Progression")
    plt.plot(timeline, muscle_data, marker="o", color="red", linewidth=2, label="Muscle Mass (kg)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.xlabel("Weeks", labelpad=8, fontsize=8.5)
    plt.xticks(rotation=30, ha="right", fontsize=7.5)
    plt.ylabel("Skeletal Muscle Mass (kg)")
    for x, y in zip(timeline, muscle_data):
        plt.annotate(
            f"{y:.2f} kg",
            (x, y),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    # Subplot 3: Fat Mass Progression
    plt.subplot(2, 2, 3)
    plt.title("Expected Fat Mass Progression")
    plt.plot(timeline, fat_mass_data, marker="o", color="orange", linewidth=2, label="Fat Mass (kg)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.xlabel("Weeks", labelpad=8, fontsize=8.5)
    plt.xticks(rotation=30, ha="right", fontsize=7.5)
    plt.ylabel("Fat Mass (kg)")
    for x, y in zip(timeline, fat_mass_data):
        plt.annotate(
            f"{y:.2f} kg",
            (x, y),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    # Subplot 4: Body Fat Percentage Progression
    plt.subplot(2, 2, 4)
    plt.title("Expected Body Fat Percentage Progression")
    plt.plot(timeline, fat_pct_data, marker="o", color="orange", linewidth=2, label="Body Fat (%)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.xlabel("Weeks", labelpad=8, fontsize=8.5)
    plt.xticks(rotation=30, ha="right", fontsize=7.5)
    plt.ylabel("Body Fat (%)")
    for x, y in zip(timeline, fat_pct_data):
        plt.annotate(
            f"{y:.2f} %",
            (x, y),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    plt.tight_layout(pad=2.0, h_pad=4.2, w_pad=2.0)
    for ax in plt.gcf().axes:
        ax.patch.set_alpha(0.0)

    chart_filename = "progress_charts.png"
    plt.savefig(chart_filename, dpi=200, facecolor="white", edgecolor="none")
    plt.close()
    return chart_filename

def calculate_healthy_weight(height_cm):#
    min_weight = 18.5 * (height_cm / 100) ** 2
    max_weight = 24.9 * (height_cm / 100) ** 2
    return round(min_weight, 1), round(max_weight, 1)

def plot_reference_ranges(
    weight, min_weight, max_weight, body_fat_percentage, gender, filename="reference_ranges.png"
):#
    if gender == "F":
        y_limits = [0, 13, 20, 24, 31, 45]
    else:
        y_limits = [0, 5, 13, 17, 24, 40]

    overweight_limit = max_weight * (29.9 / 24.9)

    fig, (ax_weight, ax_fat) = plt.subplots(2, 1, figsize=(7.5, 3.4), dpi=300)
    fig.patch.set_facecolor("none")
    plt.subplots_adjust(hspace=0.48)

    weight_left = max(35.0, min_weight - 10)
    weight_right = max(max_weight + 15, weight + 8)

    ax_weight.axvspan(35, min_weight, color="#E0E7FF", alpha=0.7)
    ax_weight.axvspan(min_weight, max_weight, color="#DCFCE7", alpha=0.7)
    ax_weight.axvspan(max_weight, overweight_limit, color="#FEF3C7", alpha=0.7)
    ax_weight.axvspan(overweight_limit, weight_right, color="#FEE2E2", alpha=0.7)

    ax_weight.text((35 + min_weight) / 2, 0.45, "Underweight", ha="center", fontsize=7.5, color="#475569")
    ax_weight.text((min_weight + max_weight) / 2, 0.45, "Healthy", ha="center", fontsize=7.5, fontweight="bold", color="#15803D")
    ax_weight.text((max_weight + overweight_limit) / 2, 0.45, "Overweight", ha="center", fontsize=7.5, color="#B45309")
    ax_weight.text((overweight_limit + weight_right) / 2, 0.45, "Obesity", ha="center", fontsize=7.5, color="#B91C1C")

    ax_weight.barh(0, weight, height=0.22, color="#4A196E", zorder=3)
    ax_weight.text(weight + 0.8, 0, f"Current: {weight:.2f} kg", va="center", fontsize=8, fontweight="bold", color="#4A196E")

    ax_weight.set_xlim(weight_left, weight_right)
    ax_weight.set_ylim(-0.4, 0.9)
    ax_weight.set_yticks([])
    ax_weight.set_title("Weight and Healthy Reference Range", fontsize=9, fontweight="bold", color="#32144B", loc="left", x=0, pad=6)

    ax_weight.tick_params(axis="x", labelsize=8)
    for spine in ax_weight.spines.values():
        spine.set_color("#E0E0E0")

    ax_fat.axvspan(y_limits[0], y_limits[1], color="#E0E7FF", alpha=0.7)
    ax_fat.axvspan(y_limits[1], y_limits[2], color="#DCFCE7", alpha=0.7)
    ax_fat.axvspan(y_limits[2], y_limits[3], color="#A7F3D0", alpha=0.7)
    ax_fat.axvspan(y_limits[3], y_limits[4], color="#FEF3C7", alpha=0.7)
    ax_fat.axvspan(y_limits[4], 45, color="#FEE2E2", alpha=0.7)

    ax_fat.text((y_limits[0] + y_limits[1]) / 2, 0.45, "Essential", ha="center", fontsize=7, color="#4338CA")
    ax_fat.text((y_limits[1] + y_limits[2]) / 2, 0.45, "Athletic", ha="center", fontsize=7, color="#15803D")
    ax_fat.text((y_limits[2] + y_limits[3]) / 2, 0.45, "Fitness", ha="center", fontsize=7, color="#047857")
    ax_fat.text((y_limits[3] + y_limits[4]) / 2, 0.45, "Acceptable", ha="center", fontsize=7, color="#B45309")
    ax_fat.text((y_limits[4] + 45) / 2, 0.45, "Obesity", ha="center", color="#B91C1C", fontsize=7)

    ax_fat.barh(0, body_fat_percentage, height=0.22, color="#4A196E", zorder=3)
    ax_fat.text(body_fat_percentage + 0.6, 0, f"Current: %{body_fat_percentage:.1f}", va="center", fontsize=8, fontweight="bold", color="#4A196E")

    ax_fat.set_xlim(0, max(45, body_fat_percentage + 5))
    ax_fat.set_ylim(-0.4, 0.9)
    ax_fat.set_yticks([])
    ax_fat.set_title("Body Fat Percentage and Reference Range", fontsize=9, fontweight="bold", color="#32144B", loc="left", x=0, pad=6)

    ax_fat.tick_params(axis="x", labelsize=8)
    for spine in ax_fat.spines.values():
        spine.set_color("#E0E0E0")

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", dpi=300, facecolor="white", edgecolor="none")
    plt.close()

class ReportPDF(FPDF):#
    def header(self):
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 297, "F")

    def section_header(self, text):
        self.ln(4)
        self.set_fill_color(226, 215, 245)
        self.set_text_color(74, 25, 110)
        self.set_font("CustomFont", "B", 11)
        self.cell(0, 8, f" {text}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(3)
        self.set_text_color(40, 40, 40)

    def footer(self):
        self.set_y(-12)
        self.set_font("CustomFont", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="R")
def generate_page_1(pdf, data):#
    pdf.add_page()

    pdf.set_font("CustomFont", "B", 18)
    pdf.set_text_color(70, 30, 95)
    pdf.cell(0, 12, "INDIVIDUAL NUTRITION & DEVELOPMENT PLAN", ln=1, align="C")
    pdf.ln(3)

    pdf.section_header("Personal Information")
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)

    pdf.cell(24, 6, "First Name: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(40, 6, str(data["first_name"]), ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(24, 6, "Last Name: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(40, 6, str(data["last_name"]), ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "Age: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(48, 6, str(data["age"]), ln=1)

    bmi_value = f"{float(data['bmi']):.1f}"

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(24, 6, "Height: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(40, 6, f"{data['height_cm']} cm", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(24, 6, "Weight: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(40, 6, f"{float(data['weight']):.1f} kg", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "BMI: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(48, 6, bmi_value, ln=1)

    tdee_value = f"{float(data['tdee']):.0f}"

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(62, 6, "Daily Energy Expenditure (TDEE): ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(32, 6, f"{tdee_value} kcal", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(36, 6, "Daily Water Need: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 6, f"{data['water_l']:.1f} L", ln=1)

    pdf.section_header("Current Anthropometrics & Body Composition")

    if data["gender"] == "F":
        hip_txt = f"{data['hip']} cm"
    else:
        hip_txt = "--"

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "Waist: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(49, 6, f"{data['waist']} cm ", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(16, 6, "Neck: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(47, 6, f"{data['neck']} cm ", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "Hip: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(49, 6, hip_txt, ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(32, 6, "Skeletal Muscle: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(31, 6, f"{float(data['skeletal_muscle_mass']):.2f} kg ", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(24, 6, "Fat Mass: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(39, 6, f"{float(data['fat_mass']):.2f} kg ", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(34, 6, "Body Fat Percentage: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(29, 6, f"% {float(data['body_fat_percentage']):.1f}", ln=1)

    pdf.ln(4)
    pdf.set_font("CustomFont", "B", 10)
    clean_goal = "\n".join(
        [
            line.strip()
            for line in str(data["recommended_goal"]).splitlines()
            if line.strip()
        ]
    )
    pdf.multi_cell(0, 4.5, clean_goal, align="L")
    pdf.ln(3)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(46, 5.5, "Selected Goal: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5.5, f" {data['selected_goal']}", ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(46, 5.5, "Selected Activity Level: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5.5, f" {data['activity_title']}", ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(46, 5.5, "Selected Meals Count: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5.5, f" {data['meals_count']}", ln=1)
    pdf.ln(2)

    pdf.section_header("Target Outcomes After 8 Weeks")

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(38, 5, "Target Weight:", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(42, 5, f" {data['target_weight']} kg", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(42, 5, "Target Muscle Mass:", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"{data['target_muscle_mass']} kg", ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(38, 5, "Target Fat Mass:", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(42, 5, f" {data['target_fat_mass']} kg", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(42, 5, "Target Body Fat %:", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f" %{data['target_fat_pct']}", ln=1)
    pdf.ln(6)

    chart_y = pdf.get_y()
    pdf.image("reference_ranges.png", x=6, y=chart_y, w=195)
    pdf.set_y(chart_y + 82)
    pdf.ln(4)

    pdf.set_draw_color(220, 215, 230)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    pdf.set_x(10)
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("CustomFont", "B", 10)
    pdf.cell(0, 4, "METHODOLOGY & SCIENTIFIC REFERENCES", ln=1)

    pdf.set_font("CustomFont", "", 9)
    methodology_text = (
        "* Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) are calculated using the Mifflin-St Jeor formula.\n\n"
        "* Body Composition and body fat percentage estimations are modeled based on U.S. Navy Body Fat Algorithms.\n\n"
        "* Healthy weight classifications and reference intervals conform to World Health Organization (WHO) and American Council on Exercise (ACE) standards."
    )
    pdf.ln(3)
    pdf.multi_cell(190, 3.8, methodology_text)
def generate_page_2(pdf, data):#
    pdf.add_page()

    pdf.section_header("Daily Target Calories and Macronutrient Intake")
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)

    pdf.ln(2)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(90, 80, 100)
    note_text = (
        "Note: In cases where the selected goal is Weight Gain or Fat Loss, a separate "
        "plan with progressive adjustments has been structured for Month 1 and Month 2 "
        "to account for metabolic adaptation and achieve optimal outcomes. Other goals "
        "do not require phase-based recalibration."
    )
    pdf.multi_cell(0, 4.2, note_text, align="L")

    # Phase 1: First 4 Weeks
    pdf.section_header("First 4 Weeks")
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)

    pdf.cell(18, 6, "Calories: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"{data['calories_1']} kcal", ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(18, 6, "Protein: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(45, 6, f"{data['protein_1']} grams", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(30, 6, "Carbohydrates: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(33, 6, f"{data['carbs_1']} grams", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "Fat: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(50, 6, f"{data['fat_1']} grams", ln=1)
    pdf.ln(3)

    pdf.section_header("First 4 Weeks Meal Plan")
    distribution_1 = distribute_meal_macros(
        data["calories_1"],
        data["protein_1"],
        data["carbs_1"],
        data["fat_1"],
        data["meals_count"],
    )
    draw_meal_table(pdf, distribution_1)
    pdf.ln(2)

    # Phase 2: Second 4 Weeks
    pdf.section_header("Second 4 Weeks")
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)

    pdf.cell(18, 6, "Calories: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"{data['calories_2']} kcal", ln=1)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(18, 6, "Protein: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(45, 6, f"{data['protein_2']} grams", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(30, 6, "Carbohydrates: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(33, 6, f"{data['carbs_2']} grams", ln=0)

    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(50, 20, 75)
    pdf.cell(14, 6, "Fat: ", ln=0)
    pdf.set_font("CustomFont", "B", 9.5)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(50, 6, f"{data['fat_2']} grams", ln=1)
    pdf.ln(3)

    pdf.section_header("Second 4 Weeks Meal Plan")
    distribution_2 = distribute_meal_macros(
        data["calories_2"],
        data["protein_2"],
        data["carbs_2"],
        data["fat_2"],
        data["meals_count"],
    )
    draw_meal_table(pdf, distribution_2)

    pdf.ln(12 if data["meals_count"] == 2 else 6)
    min_protein = round(data["protein_1"] * 0.8)
    optimum_protein = round(data["protein_1"] * 1.6)

    pdf.set_fill_color(243, 237, 247)
    pdf.set_draw_color(167, 139, 219)
    pdf.set_text_color(50, 20, 75)
    pdf.set_font("CustomFont", "B", 10.5)
    pdf.cell(
        190,
        5.5,
        "Meal Timing and Critical Macro Flexibility Thresholds",
        ln=1,
        fill=True,
        border="LTR",
    )

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("CustomFont", "", 9.5)
    notes = (
        "\n"
        f"* Protein Intake Flexibility: The amounts presented in the plan represent the optimal baseline. "
        f"Even with daily fluctuations, protein should not drop below {min_protein} g (0.8 g/kg threshold) "
        f"to prevent lean tissue catabolism; keeping it close to {optimum_protein} g supports maximum recovery.\n\n"
        "* Meal Timing: Spacing main meals by roughly 3.5 to 4 hours stabilizes glycemic control and promotes "
        "muscle protein synthesis (MPS). Flexibility in meal timing is permissible as long as daily macro targets are hit.\n\n"
        "* Fluid Balance: To avoid diluting gastric acids and digestive enzymes, consume substantial liquids "
        "20 to 30 minutes before or after main meals rather than during."
    )
    pdf.multi_cell(190, 4.0, notes, fill=True, border="LBR")
def generate_pages_3_4_5(pdf, data, workout_schedule):#
    # PAGE 3
    pdf.add_page()

    nutrition_guide = {
        "Carbohydrates & Legumes": [
            ("Rolled Oats", "60g Carb / 370 kcal"),
            ("Pasta (Durum Wheat, Raw)", "72g Carb / 355 kcal"),
            ("Rice / Basmati (Raw)", "78g Carb / 355 kcal"),
            ("Bulgur (Raw)", "70g Carb / 342 kcal"),
            ("Buckwheat (Raw)", "71g Carb / 343 kcal"),
            ("Dry Beans (Raw)", "60g Carb / 335 kcal"),
            ("Chickpeas (Raw)", "61g Carb / 364 kcal"),
            ("Red / Green Lentils (Raw)", "60g Carb / 340 kcal"),
            ("Whole Wheat Bread", "45g Carb / 240 kcal"),
            ("Boiled Potatoes", "17g Carb / 77 kcal"),
            ("Popcorn (Air-Popped/Oil-Free)", "74g Carb / 365 kcal"),
            ("Banana (Medium)", "23g Carb / 89 kcal"),
            ("Apple (With Skin)", "14g Carb / 52 kcal"),
            ("Dried Dates / Apricots", "65g Carb / 270 kcal"),
            ("Peach (Medium)", "9.5g Carb / 39 kcal"),
            ("Orange (Medium)", "15g Carb / 60 kcal"),
        ],
        "Protein & Dairy": [
            ("Chicken Breast (Raw/Skinless)", "23g Prt / 120 kcal"),
            ("Turkey Breast (Raw)", "24g Prt / 115 kcal"),
            ("Lean Minced Beef / Cubes", "21g Prt / 150 kcal"),
            ("Salmon / Cod / Trout", "20g Prt / 175 kcal"),
            ("Tuna (Canned in Water)", "25g Prt / 110 kcal"),
            ("Whole Egg (Large)", "13g Prt / 143 kcal"),
            ("Egg White", "11g Prt / 52 kcal"),
            ("Strained Greek Yogurt", "10g Prt / 66 kcal"),
            ("Natural Plain Yogurt", "4g Prt / 60 kcal"),
            ("Low-Fat Curd / Cottage Cheese", "17g Prt / 85 kcal"),
            ("Feta / White Cheese", "16g Prt / 240 kcal"),
            ("Kashar / Cheddar Cheese", "25g Prt / 350 kcal"),
            ("Semi-Skimmed Milk (100 ml)", "3.3g Prt / 46 kcal"),
            ("Skimmed / Lactose-Free Milk (100 ml)", "3.4g Prt / 36 kcal"),
            ("Chickpeas (Raw)", "19g Prt / 364 kcal"),
            ("Dry Beans (Raw)", "21g Prt / 335 kcal"),
        ],
        "Healthy Fats & Seeds": [
            ("Extra Virgin Olive Oil", "100g Fat / 884 kcal"),
            ("Raw Almonds", "50g Fat / 579 kcal"),
            ("Walnuts", "65g Fat / 654 kcal"),
            ("Raw Hazelnuts", "61g Fat / 628 kcal"),
            ("Raw Cashews", "44g Fat / 553 kcal"),
            ("Raw Pistachios", "45g Fat / 560 kcal"),
            ("Roasted Unsalted Peanuts", "49g Fat / 567 kcal"),
            ("Natural Peanut Butter (100%)", "50g Fat / 588 kcal"),
            ("Tahini", "54g Fat / 595 kcal"),
            ("Sesame Seeds (Raw)", "50g Fat / 573 kcal"),
            ("Black Seed (Nigella)", "35g Fat / 375 kcal"),
            ("Pumpkin Seeds (Raw)", "49g Fat / 559 kcal"),
            ("Chia Seeds", "31g Fat / 486 kcal"),
            ("Ground Flaxseeds", "42g Fat / 534 kcal"),
            ("Black / Green Olives", "11g Fat / 115 kcal"),
            ("Avocado", "15g Fat / 160 kcal"),
        ],
    }

    pdf.set_fill_color(243, 237, 247)
    pdf.set_draw_color(167, 139, 219)
    pdf.set_text_color(50, 20, 75)
    pdf.set_font("CustomFont", "B", 9)
    pdf.cell(
        190,
        5.5,
        "Essential Macronutrient Exchange Guide & Reference Values",
        ln=1,
        fill=True,
        border="LTR",
        align="C",
    )

    pdf.set_fill_color(74, 25, 110)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("CustomFont", "B", 8)

    col_w = 190 / 3
    categories = [
        "Carbohydrates & Legumes",
        "Protein & Dairy",
        "Healthy Fats & Seeds",
    ]
    for cat in categories:
        pdf.cell(col_w, 5, cat, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("CustomFont", "", 8)
    pdf.set_text_color(35, 35, 35)
    pdf.set_draw_color(225, 220, 235)

    num_rows = 16
    for i in range(num_rows):
        fill_status = i % 2 == 0
        pdf.set_fill_color(250, 248, 253)

        for cat in categories:
            item, val = nutrition_guide[cat][i]
            entry_text = f"{item}: {val}"
            pdf.cell(col_w, 7.5, f"{entry_text}", border=1, fill=fill_status, align="L")
        pdf.ln()

    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(110, 110, 120)
    pdf.set_font("CustomFont", "", 7)
    footnote = (
        "\n"
        "* Measurement & Consumption Standard: Values are referenced for 100g net raw/uncooked dry weight for solids, "
        "and 100ml for dairy products. Legumes expand 2-2.5 times in weight when boiled; use dry weight benchmarks "
        "when portioning cooked foods. You may flexibly combine your daily macronutrients using these sources."
    )
    pdf.multi_cell(190, 3.4, footnote, border="LBR")
    pdf.ln(18)

    day_col_w = 28
    detail_col_w = 162
    row_h = 9

    pdf.section_header("Goal-Tailored Training & Workout Plan")
    pdf.ln(3)
    pdf.set_font("CustomFont", "B", 9)
    pdf.set_fill_color(74, 25, 110)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(day_col_w, 10, "Day", border=1, fill=True, align="C")
    pdf.cell(detail_col_w, 10, "Workout / Activity Details", border=1, ln=1, fill=True, align="C")

    for day, details in workout_schedule.items():
        y_start = pdf.get_y()
        pdf.set_font("CustomFont", "", 8.5)
        pdf.set_text_color(20, 20, 20)

        pdf.set_xy(10 + day_col_w, y_start)
        pdf.multi_cell(detail_col_w, row_h, f" {details.strip()}", border=1, align="L")

        y_end = pdf.get_y()
        total_block_h = y_end - y_start

        pdf.set_xy(10, y_start)
        pdf.set_font("CustomFont", "B", 8.5)
        pdf.set_fill_color(248, 245, 254)
        pdf.set_text_color(74, 25, 110)
        pdf.cell(28, total_block_h, f"{day}", border=1, fill=True, align="C")

        pdf.set_xy(10, y_end)

    # PAGE 4
    pdf.add_page()
    pdf.section_header("8-Week Target Progression Projection")
    chart_y = pdf.get_y()
    pdf.image("progress_charts.png", x=10, y=chart_y, w=190)
    pdf.set_y(chart_y + 110)
    pdf.ln(4)

    # PAGE 5
    pdf.add_page()
    pdf.section_header("8-Week Personal Progress & Measurement Tracking Sheet")
    pdf.ln(3)
    pdf.set_font("CustomFont", "", 8)
    pdf.set_text_color(90, 90, 100)
    instructions = (
        "This tracking sheet is designed to help maintain adherence throughout your 8-week journey. "
        "Record your measurements once a week on the same day, first thing in the morning while fasting "
        "and under consistent conditions."
    )
    pdf.multi_cell(190, 4.5, instructions, border=0)
    pdf.ln(4)

    columns = [
        ("Week", 16),
        ("Weight (kg)", 20),
        ("Waist (cm)", 20),
        ("Hips (cm)", 20),
        ("Arm/Chest", 22),
        ("Avg Step/Water", 24),
        ("Workout", 24),
        ("Weekly Notes / Review", 44),
    ]

    pdf.set_font("CustomFont", "B", 7.5)
    pdf.set_fill_color(74, 25, 110)
    pdf.set_text_color(255, 255, 255)
    for title, width in columns:
        pdf.cell(width, 8.5, title, border=1, fill=True, align="C")
    pdf.ln()

    tracking_row_h = 17.5
    pdf.set_text_color(60, 60, 70)

    for week in range(1, 9):
        if week % 2 == 0:
            pdf.set_fill_color(248, 245, 252)
            fill_active = True
        else:
            pdf.set_fill_color(255, 255, 255)
            fill_active = False

        pdf.set_font("CustomFont", "B", 8)
        pdf.cell(columns[0][1], tracking_row_h, f"Week {week}", border=1, fill=fill_active, align="C")

        pdf.set_font("CustomFont", "", 8)
        for _, width in columns[1:]:
            pdf.cell(width, tracking_row_h, "", border=1, fill=fill_active, align="C")
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("CustomFont", "", 8)
    pdf.set_text_color(110, 110, 120)
    pdf.cell(190,5,"* Consistent monitoring is the cornerstone of adherence and sustainable habit formation.",align="C")
def draw_meal_table(pdf, meal_macros):#
    w_meal = 38
    w_calories = 36
    w_carbs = 39
    w_protein = 39
    w_fat = 38

    pdf.set_font("CustomFont", "B", 8.5)
    pdf.set_fill_color(74, 25, 110)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w_meal, 7, "Meal", border=1, fill=True, align="C", ln=0)
    pdf.cell(w_calories, 7, "Total Energy", border=1, fill=True, align="C", ln=0)
    pdf.cell(w_carbs, 7, "Carbohydrates", border=1, fill=True, align="C", ln=0)
    pdf.cell(w_protein, 7, "Protein", border=1, fill=True, align="C", ln=0)
    pdf.cell(w_fat, 7, "Fat", border=1, fill=True, align="C", ln=1)

    for meal_name, nutrients in meal_macros.items():
        calories_val = nutrients.get("Total Meal Energy", "-").replace(" --> ", "\n")
        carbs_val = nutrients.get("Carbohydrates", "-").replace(" --> ", "\n")
        protein_val = nutrients.get("Protein", "-").replace(" --> ", "\n")
        fat_val = nutrients.get("Fat", "-").replace(" --> ", "\n")

        y_start = pdf.get_y()

        pdf.set_font("CustomFont", "", 8)
        pdf.set_text_color(20, 20, 20)

        h_row = 11.0

        pdf.set_xy(10, y_start)
        pdf.set_font("CustomFont", "B", 8.5)
        pdf.set_fill_color(248, 245, 254)
        pdf.set_text_color(74, 25, 110)
        pdf.cell(w_meal, h_row, meal_name, border=1, fill=True, align="C", ln=0)

        pdf.set_font("CustomFont", "B", 9)
        pdf.set_text_color(50, 20, 75)
        pdf.set_xy(10 + w_meal, y_start)
        pdf.cell(w_calories, h_row, calories_val, border=1, align="C", ln=0)

        pdf.set_font("CustomFont", "", 7.5)
        pdf.set_text_color(30, 30, 30)

        x_carbs = 10 + w_meal + w_calories
        pdf.set_xy(x_carbs, y_start + 1.2)
        pdf.multi_cell(w_carbs, 4.2, carbs_val, align="C")
        pdf.rect(x_carbs, y_start, w_carbs, h_row)

        x_protein = x_carbs + w_carbs
        pdf.set_xy(x_protein, y_start + 1.2)
        pdf.multi_cell(w_protein, 4.2, protein_val, align="C")
        pdf.rect(x_protein, y_start, w_protein, h_row)

        x_fat = x_protein + w_protein
        pdf.set_xy(x_fat, y_start + 1.2)
        pdf.multi_cell(w_fat, 4.2, fat_val, align="C")
        pdf.rect(x_fat, y_start, w_fat, h_row)

        pdf.set_xy(10, y_start + h_row)
def generate_full_report(file_name, data, workout_schedule):#
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")

    try:
        pdf.add_font(
            "CustomFont",
            "",
            "LiberationSerif-Regular.ttf",
            uni=True
        )
        pdf.add_font(
            "CustomFont",
            "B",
            "LiberationSerif-Bold.ttf",
            uni=True
        )
        pdf.set_font("CustomFont", "", 10)
    except Exception:
        pdf.set_font("Helvetica", "", 10)

    pdf.set_auto_page_break(auto=False)

    plot_reference_ranges(
        weight=data["weight"],
        min_weight=data["min_weight"],
        max_weight=data["max_weight"],
        body_fat_percentage=data["body_fat_percentage"],
        gender=data["gender"],
        filename="reference_ranges.png",
    )

    generate_page_1(pdf, data)
    generate_page_2(pdf, data)
    generate_pages_3_4_5(pdf, data, workout_schedule)

    pdf.output(file_name)

def main():
    print("Welcome to My Digital Dietitian Application ✨️")

    name = input("What is your name? \n")
    surname = input("What is your surname? \n")

    while True:
        try:
            gender = input(
                "What is your gender? \n" "Please specify F or M.\n"
            ).upper()
            pattern = r"^(?:\s*)((F|M){1})(?:\s*)$"
            match = re.search(pattern, gender)
            if match:
                gender = match.group(1)
                break
            else:
                print("Invalid gender entered.")
        except ValueError:
            print("Please specify your gender.")

    while True:
        try:
            age = int(input("What is your age? \n").strip())
            if 16 <= age <= 90:
                break
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            height_cm = int(input("Enter your height in 'cm': \n").strip())
            if 130 <= height_cm <= 230:
                break
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            weight = float(
                input(
                    "Enter your current weight:\n"
                    "Specify as kg.g\n"
                ).strip()
            )
            if 35 <= weight <= 200:
                break
        except ValueError:
            print("Please enter valid information.")

    print(
        "\nIn the next step, we will learn about your body composition with the information you provide.\n"
    )

    while True:
        try:
            waist = int(
                input(
                    "What is your waist circumference? \n"
                    "Enter value in cm.\n"
                ).strip()
            )
            if 45 <= waist <= 180:
                break
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            neck = int(
                input(
                    "What is your neck circumference?\n"
                    "Enter value in cm.\n"
                ).strip()
            )
            if 25 <= neck <= 60:
                break
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            if gender == "F":
                hip = int(
                    input(
                        "What is your hip circumference?\n"
                        "Enter value in cm.\n"
                    ).strip()
                )
                if 60 <= hip <= 190:
                    break
            else:
                hip = "--"
                break
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            if gender == "F":
                if (waist + hip) - neck <= 0 or hip < waist:
                    print("The entered measurements are invalid.")
                    waist = int(input("What is your waist circumference? (cm): ").strip())
                    neck = int(input("What is your neck circumference? (cm): ").strip())
                    hip = int(input("What is your hip circumference? (cm): ").strip())
                    if not (45 <= waist <= 180 and 25 <= neck <= 60 and 60 <= hip <= 190):
                        print("Measurements out of valid physical range. Please enter again.")
                    continue
            else:
                if (waist - neck) <= 0:
                    print("The entered measurements are invalid.")
                    waist = int(input("What is your waist circumference? (cm): ").strip())
                    neck = int(input("What is your neck circumference? (cm): ").strip())
                    if not (45 <= waist <= 180 and 25 <= neck <= 60):
                        print("Measurements out of valid physical range. Please enter again.")
                    continue
            break
        except ValueError:
            print("Please enter valid numerical values.")

    while True:
        try:
            specified_goal = input(
                "Specify your overall goal:\n"
                "1-) Weight Gain\n"
                "2-) Muscle Gain / Body Recomposition\n"
                "3-) Weight Maintenance\n"
                "4-) Fat Loss / Weight Loss\n"
                "Enter a number between 1 and 4:"
            ).strip()
            goal_id = int(specified_goal)
            if 1 <= goal_id <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
            continue

    if goal_id == 1:
        goal = "Weight Gain / Hypertrophy"
    elif goal_id == 2:
        goal = "Muscle Gain / Body Recomposition"
    elif goal_id == 3:
        goal = "Weight Maintenance"
    else:
        goal = "Fat Loss / Weight Loss"

    while True:
        try:
            meals_count = int(
                input(
                    "How many meals do you eat? \n"
                    "Enter 2 or 3 for 2 or 3 meal options. \n"
                ).strip()
            )
            if meals_count == 2 or meals_count == 3:
                break
            else:
                print("Enter a valid number of meals.")
                continue
        except ValueError:
            print("Please enter valid information.")

    while True:
        try:
            activity_level = input(
                "Please specify your target activity level.\n"
                "1-) Beginner / Sedentary (2-3 days light exercise per week)\n"
                "2-) Light - Moderately Active (3-4 days regular exercise & walking per week)\n"
                "3-) Highly Active (5-6 days structured sports & conditioning per week)\n"
                "4-) Very Intense / Athletic (6 days advanced intense training per week)\n"
                "Enter a number between 1 and 4:\n"
            ).strip()
            activity_no = int(activity_level)
            if 1 <= activity_no <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
            continue

    if activity_no == 1:
        activity = "Beginner / Sedentary (2-3 days light exercise per week)"
    elif activity_no == 2:
        activity = "Light - Moderately Active (3-4 days regular exercise & walking per week)"
    elif activity_no == 3:
        activity = "Highly Active (5-6 days structured sports & conditioning per week)"
    else:
        activity = "Very Intense / Athletic (6 days advanced intense training per week)"

    while True:
        try:
            workout_env = int(
                input(
                    "In which environment will you work out? \n"
                    "Enter -> 1 for Home Workout or -> 2 for Gym Workout "
                ).strip()
            )
            if workout_env == 1 or workout_env == 2:
                break
        except ValueError:
            print("Please enter valid information.")

    # 1. Calculation Functions Calling
    bmi, bmr, tdee = calculate_bmr(gender, weight, height_cm, age, activity_no)

    (
        body_fat_percentage,
        fat_mass,
        lean_mass,
        skeletal_muscle_mass,
    ) = analyze_body_composition(waist, neck, hip, gender, height_cm, weight)

    recommended_water_l = calculate_water_intake(weight, gender)

    recommended_goal_text = get_recommended_goal(gender, body_fat_percentage, bmi)

    (
        target_calories_1,
        protein_calories_1,
        protein_1,
        carb_calories_1,
        carbs_1,
        fat_calories_1,
        fat_1,
    ) = calculate_nutrition_plan(gender, goal_id, tdee, month=1)

    (
        target_calories_2,
        protein_calories_2,
        protein_2,
        carb_calories_2,
        carbs_2,
        fat_calories_2,
        fat_2,
    ) = calculate_nutrition_plan(gender, goal_id, tdee, month=2)

    meal_macros_1 = distribute_meal_macros(
        target_calories_1, protein_1, carbs_1, fat_1, meals_count
    )

    meal_macros_2 = distribute_meal_macros(
        target_calories_2, protein_2, carbs_2, fat_2, meals_count
    )

    workout_schedule = generate_workout_plan(workout_env, activity_no)

    (
        month_1_end,
        month_2_end,
        weight_projection_table,
        monthly_change,
    ) = calculate_weight_projection(tdee, target_calories_1, weight)

    (
        muscle_change_1,
        fat_mass_change_1,
        fat_pct_change_1,
        muscle_change_2,
        fat_mass_change_2,
        fat_pct_change_2,
    ) = calculate_composition_changes(
        monthly_change,
        skeletal_muscle_mass,
        fat_mass,
        body_fat_percentage,
        goal_id,
        weight,
    )

    generate_progress_charts(
        weight,
        month_1_end,
        month_2_end,
        skeletal_muscle_mass,
        muscle_change_1,
        muscle_change_2,
        fat_mass,
        fat_mass_change_1,
        fat_mass_change_2,
        body_fat_percentage,
        fat_pct_change_1,
        fat_pct_change_2,
    )

    min_weight, max_weight = calculate_healthy_weight(height_cm)

    # 2. Data Dictionary Construction (Retaining exact mapping structure)
    data = {
        "first_name": name,
        "last_name": surname,
        "age": age,
        "height_cm": height_cm,
        "weight": weight,
        "bmi": bmi,
        "tdee": tdee,
        "gender": gender,
        "waist": waist,
        "neck": neck,
        "hip": hip,
        "skeletal_muscle_mass": skeletal_muscle_mass,
        "fat_mass": fat_mass,
        "body_fat_percentage": body_fat_percentage,
        "recommended_goal": recommended_goal_text,
        "selected_goal": goal,
        "activity_title": activity,
        "meals_count": meals_count,
        "calories_1": target_calories_1,
        "calories_2": target_calories_2,
        "protein_1": protein_1,
        "carbs_1": carbs_1,
        "fat_1": fat_1,
        "protein_2": protein_2,
        "carbs_2": carbs_2,
        "fat_2": fat_2,
        "water_l": recommended_water_l,
        "target_weight": month_2_end,
        "target_fat_mass": fat_mass_change_2,
        "target_muscle_mass": muscle_change_2,
        "target_fat_pct": fat_pct_change_2,
        "min_weight": min_weight,
        "max_weight": max_weight,
    }

    generate_full_report(
        file_name="individual_development_report.pdf",
        data=data,
        workout_schedule=workout_schedule,
    )

    return (
        name,
        surname,
        gender,
        activity_no,
        activity,
        weight,
        height_cm,
        age,
        goal_id,
        meals_count,
        meal_macros_1,
        meal_macros_2,
        workout_env,
    )


if __name__ == "__main__":
    main()

