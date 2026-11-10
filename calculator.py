# calculator.py
# calorie calculation engine


# ACTIVITY MULTIPLIERS
ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "lightly active": 1.375,
    "moderately active": 1.55,
    "very active": 1.725,
    "extremely active": 1.9
}


# GOAL-BASED CALORIE ADJUSTMENTS
GOAL_FACTORS = {
    "lose weight": 0.90,
    "maintain weight": 1.0,
    "gain weight": 1.10
}

MACRO_PRESETS = {
    "lose weight" : {
        "protein_factor": 2.0,
        "fat_fraction": 0.30
    },
    "maintain weight" : {
        "protein_factor": 1.6,
        "fat_fraction": 0.30
    },
    "gain weight" : {
        "protein_factor": 1.8,
        "fat_fraction": 0.25
    }
}


def calculate_calories(age,weight,height,sex,activity, goal):
    """
    calculate estimated daily calorie requirements
    
    assumes age, weight and height have already passed input validatioin ligc
    """
    
    #nomralize text inputs
    sex = sex.strip().casefold()
    activity = activity.strip().casefold()
    goal = goal.strip().casefold()
    
    # VALIDATE SELCETED OPTIONS
    if sex not in ("male", "female"):
        raise ValueError("Invalid sex parameter")
    if activity not in ACTIVITY_FACTORS:
        raise ValueError("Invalid activity level")
    if goal not in GOAL_FACTORS:
        raise ValueError("Invalid fitness goal")
    
    
    #STEP 1 RESTING METABOLIC RATE
    base_rmr = (
        10 * weight + 6.25 * height - 5 * age
    )
    
    if sex == "male":
        rmr = base_rmr + 5
    else:
        rmr = base_rmr - 161
        
    #STEP 2 TOTAL DAILTY ENERGY EXPENDITURE
    activity_factor = ACTIVITY_FACTORS[activity]
    tdee = rmr * activity_factor
    
    #STEP 3 GOAL-BASED CALORIE TARGET
    goal_factor = GOAL_FACTORS[goal]
    calorie_target = tdee * goal_factor
    
    #eRETURNING RESULTS WITHOUT ROUNDING
    return {
        "rmr": rmr,
        "tdee": tdee,
        "target": calorie_target,
        "activity_factor": activity_factor,
        "goal_factor": goal_factor
    }
    
    
def calculate_macros(target_calories, weight, goal):
    """CALCULATE DAILY MACRONUTRITENT TARGETS"""
    
    goal = goal.strip().casefold()
    
    if goal not in MACRO_PRESETS:
        raise ValueError("Invalid fitness goal")
    if target_calories <=0 or weight <=0:
        raise ValueError("Calories and weight must be positive")
    
    preset= MACRO_PRESETS[goal]
    
    #PROTEIN BASED ON BODY WIGHT
    protein = weight * preset["protein_factor"]
    
    #FAT BASED ON A PERCENTAGE OF CALORIES
    fat = (target_calories * preset["fat_fraction"]) /9
    
    #CARBS - REAMINGI
    remaining_cals = (target_calories - protein * 4 - fat * 9)
    
    if remaining_cals <0:
        raise ValueError("Calorie target is too low for these macros")
    
    carbs = remaining_cals /4
    
    return {
        "protein": protein,
        "fat": fat,
        "carbs": carbs
    }
