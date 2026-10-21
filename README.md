# Automated Fitness & Nutrition Report Generator

#### Video Demo: [YOUR_YOUTUBE_VIDEO_LINK_HERE]

## Description

The **Automated Fitness & Nutrition Report Generator** is an end-to-end Python application designed to evaluate an individual's biometric markers, body composition, and metabolic parameters. Based on these inputs, it automatically generates a structured, multi-page personalized PDF fitness and nutritional development plan complete with data visualizations.

Health and wellness planning frequently requires precise mathematical modeling for Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and body composition. This application streamlines that process from the command-line interface directly to an executive-style, publication-ready PDF report.

---

## Features & Scientific Foundations

1. **Biometric & Anthropometric Calculations:**
   * **BMR & TDEE:** Computes energy expenditure using the scientifically validated Mifflin-St Jeor formula paired with standardized physical activity multipliers.
   * **Body Composition:** Implements the US Navy circumference method to derive accurate body fat percentage, lean mass, and skeletal muscle metrics without requiring expensive equipment.
   * **Nutritional Breakdown:** Calculates target caloric intake adjusted for individual goals (fat loss, recomposition, muscle gain) and determines optimal macronutrient distribution.

2. **Automated Visualization:**
   * Generates dynamic health reference range charts illustrating current metrics against standardized health thresholds.
   * Produces multi-metric 8-week target progress projections via `matplotlib`.

3. **PDF Report Compilation:**
   * Employs `fpdf2` to dynamically compile comprehensive health assessments, including nutritional recommendations, goal-tailored exercise routines, and structured tracking sheets.

---

## File Overview

* **`project.py`**: The primary executable module containing the interactive CLI interface, core computational algorithms, chart generation pipelines, and PDF document construction logic.
* **`test_project.py`**: The test suite executed via `pytest`, containing unit tests for key custom functions ensuring mathematical accuracy and robust input validation.
* **`requirements.txt`**: Specifies all required external dependencies (`matplotlib`, `fpdf2`, `pytest`).

---

## Core Functions Explained

### 1. `calculate_bmr(gender, weight_kg, height_cm, age, activity_level)`
Calculates the user's Basal Metabolic Rate using the Mifflin-St Jeor equations and multiplies it by standard activity multipliers to return the estimated TDEE.

### 2. `analyze_body_composition(waist, neck, hip, gender, height_cm, weight)`
Applies the US Navy circumference equations using logarithmic transformations to calculate body fat percentage, total fat mass, and estimated skeletal muscle mass.

### 3. `calculate_water_intake(weight, gender)`
Determines the baseline recommended daily hydration volume based on body weight and physiological benchmarks.

---

## How to Run the Project

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
