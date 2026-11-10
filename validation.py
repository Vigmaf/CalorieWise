import math

def validate_inputs(age_text, weight_text, height_text):
    """VALIDATE AND CONVERT USER INPUT INTO NUMERIC VALUES"""
    
    #1. CHECKING FOR MISSING VALUES
    if not all([
        age_text.strip(), weight_text.strip(), height_text.strip()
    ]):
        raise ValueError("All fields mut be filled in")
    
    #2. VALIDATE AGE
    try:
        age = int(age_text)
    except ValueError:
        raise ValueError("Age must be a whole number.")
    if not 18 <= age <= 120:
        raise ValueError("Age must be between 18 and 120")
    
    #3. VALIDATE WEIGHT AND HEIGH
    try:
        weight = float(weight_text.replace(",","."))
        height = float(height_text.replace(",","."))
    except ValueError:
        raise ValueError("Weight and height must be valid numbers")
    
    #4. REJECTING INFIRTY AND NAN
    if not math.isfinite(weight) or not math.isfinite(height):
        raise ValueError("Weight and height must be finite numbers")
    
    #5. CHECKING REASABLE RANGES
    if not 20 <= weight <= 200:
        raise ValueError("Weight must be between 20 and 200 kg")
    if not 100 <= height <= 250:
        raise ValueError("Height must be between 100 and 250 cm")
    
    return age, weight, height