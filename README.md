# Automated Fitness & Nutrition Report Generator

#### Video Demo: https://youtu.be/TXIfEz0h1Ds

## Description
The Automated Fitness & Nutrition Report Generator is an end-to-end Python application designed to evaluate an individual's biometric markers, body composition, and metabolic parameters. Based on these inputs, it automatically generates a structured, multi-page personalized PDF fitness and nutritional development plan complete with data visualizations.

Health and wellness planning frequently requires precise mathematical modeling for Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and body composition. This application streamlines that process from the command-line interface directly to an executive-style, publication-ready PDF report.

The primary motivation behind designing this project is to empower individuals to gain clear, non-clinical preliminary insights into their health parameters and personal wellness targets, helping them stay structured, informed, and motivated throughout their fitness journey.

---

## Mathematical Models & Scientific Foundations

The analytical engine relies on standardized physiological equations to guarantee reproducible calculations:

1. **Basal Metabolic Rate (BMR):**  
   Computed via the validated **Mifflin-St Jeor Equation**, which accounts for sexual dimorphism and lean mass distribution:
   * **Men:** $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (y)} + 5$
   * **Women:** $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (y)} - 161$

2. **Total Daily Energy Expenditure (TDEE):**  
   Derived by scaling BMR against empirical physical activity multipliers (sedentary $1.2$, lightly active $1.375$, moderately active $1.55$, highly active $1.725$).

3. **Body Composition Analysis (US Navy Circumference Method):**  
   Implements the **Hodgdon-Beckett Formula** utilizing logarithmic transformations of circumferences:
   * **Men:** $\text{Body Fat \%} = 495 / (1.0324 - 0.19077 \times \log_{10}(\text{waist} - \text{neck}) + 0.15456 \times \log_{10}(\text{height})) - 450$
   * **Women:** $\text{Body Fat \%} = 495 / (1.29579 - 0.35004 \times \log_{10}(\text{waist} + \text{hip} - \text{neck}) + 0.22100 \times \log_{10}(\text{height})) - 450$
   * Fat Mass, Lean Body Mass (LBM), and Skeletal Muscle estimations are calculated dynamically from these proportions.

4. **Caloric Deficit/Surplus & Macronutrient Partitioning:**  
   Calculated based on metabolic targets, where 1 kg of adipose tissue corresponds to an energetic equivalent of approximately $7700\text{ kcal}$. Protein, carbohydrate, and fat splits are scaled by body weight benchmarks and caloric energy ratios ($4\text{ kcal/g}$ for proteins/carbs, $9\text{ kcal/g}$ for lipids).

5. **Daily Hydration Needs:**  
   Based on baseline metabolic demand ($30\text{--}35\text{ ml}$ of water per kg of total body mass, adjusted for activity).

---

## Design Decisions & Technical Challenges

### Unicode Support & Font Management
During the PDF generation stage with `fpdf2`, handling diverse typographic requirements and non-ASCII character sets presented an initial challenge. To avoid text corruption and rendering errors across different operating environments, embedded TrueType fonts (`LiberationSerif-Regular.ttf` and `LiberationSerif-Bold.ttf`) were bundled directly into the repository. The PDF generation functions explicitly register and apply these fonts, while fallback standard fonts were integrated into the error-handling pipeline to maintain uninterrupted execution if an asset fails to load.

### Automated Visualization Pipelines
To ensure that target metrics and baseline states are tangible, intuitive, and visually rewarding, raw tabular data is paired with graphical representations built via `matplotlib`:
* **Health Reference Ranges (`reference_ranges.png`):** Maps the user's current metrics against standardized physiological health thresholds.
* **8-Week Progress Projections (`progress_charts.png`):** Illustrates trajectory milestones across two consecutive four-week phases.

Both charts are programmatically generated, proportioned to fit the document layout, and dynamically embedded into the final PDF report.

### Defensive Input Validation
To ensure runtime stability and prevent unexpected application termination during CLI interactions, user data collection routines are enclosed within `while True` loops supported by comprehensive `try-except` blocks. Any invalid inputs—such as alphabetical inputs where numeric measurements are required, or values outside realistic biological limits—trigger informative guidance prompts until valid data is supplied.

---

## Testing Strategy (`test_project.py`)

Deterministic mathematical accuracy is critical when computing physiological parameters. The test suite implemented with `pytest` verifies each independent algorithmic module:

* **`test_calculate_bmr`**: Validates calculations for BMI, BMR, and TDEE across diverse gender categories, heights, weights, ages, and activity multiplier tiers.
* **`test_analyze_body_composition`**: Evaluates the US Navy circumference algorithm to verify that body fat percentage, total fat mass, lean body mass, and skeletal muscle mass compute accurately across varying anatomical measurement sets.
* **`test_calculate_water_intake`**: Tests baseline hydration volume formulas scaled against individual body weight and physiological baselines.
* **`test_calculate_nutrition_plan`**: Confirms that caloric targets and macro distributions (calories and grams for protein, carbohydrates, and fats) are precisely partitioned for Month 1 and Month 2 progression models based on activity level, TDEE, and training methodology.
* **`test_calculate_weight_projection`**: Ensures accurate predictive modeling for expected weight changes over 4-week and 8-week horizons using energy deficits/surpluses relative to TDEE.
* **`test_calculate_body_composition_change`**: Validates projected monthly changes in skeletal muscle mass, fat mass, and overall body fat percentage across the 4-week and 8-week projection milestones.
* **`test_calculate_healthy_weight`**: Verifies that lower and upper bounds of healthy body mass ranges are calculated accurately relative to user height.

---

## How to Run the Project

### 1. Clone the Repository
```bash
git clone [https://github.com/iremmozer/CS50P-Final-Project-Automated-Fitness-and-Nutrition-Report-Generator.git](https://github.com/iremmozer/CS50P-Final-Project-Automated-Fitness-and-Nutrition-Report-Generator.git)
cd CS50P-Final-Project-Automated-Fitness-and-Nutrition-Report-Generator


