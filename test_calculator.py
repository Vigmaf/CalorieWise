import unittest
from calculator import calculate_calories, calculate_macros
import main

class TestCalorieCalculator(unittest.TestCase):
    
    def test_male_rmr_and_tdee(self):
        result = calculate_calories(21,60,173,"male",
                                    "Moderately Active", "Maintain Weight")
        
        self.assertAlmostEqual(result["rmr"], 1581.25)
        self.assertAlmostEqual(result["tdee"], 2450.9375)
        self.assertAlmostEqual(result["target"], 2450.9375)
    
    def test_female_rmr(self):
        result = calculate_calories(21,60,173,"Female",
                                    "Sedentary","Maintain Weight")
        self.assertAlmostEqual(result["rmr"], 1415.25)
    
    
    def test_extremely_active(self):
        result  = calculate_calories(21,60,173, "Male",
                                      "Extremely Active","Maintain Weight")
        self.assertAlmostEqual(result["activity_factor"],1.9)
    
    
    def test_weight_loss_and_gain(self):
        maintenance = calculate_calories(
            21,60,173,"Male","Moderately Active",
            "Maintain Weight"
        )
        
        loss = calculate_calories(
            21,60,173,"Male","Moderately Active",
            "Lose Weight"
        )
        gain = calculate_calories(
            21,60,173, "Male","Moderately Active",
            "Gain Weight"
        )
        self.assertAlmostEqual(
            loss["target"], maintenance["target"] * 0.9
        )
        self.assertAlmostEqual(
            gain["target"], maintenance["target"] * 1.1
        )
    
    def test_invalid_activity(self):
        with self.assertRaises(ValueError):
            calculate_calories(21,60,173,"Male",
                               "Unknown Activity","Maintain Weight")
            
    
    def test_macro_calculation(self):
        result = calculate_macros(2450.9375, 60, "Maintain Weight")
        
        self.assertAlmostEqual(result["protein"], 96.0)
        self.assertAlmostEqual(result["fat"], 81.69791667)
        self.assertAlmostEqual(result["carbs"], 332.9140625)
        
        #VERYFING TOTAL CALORIES FROM MACRONUTRIENTS
        total_calories = (
            result["protein"] * 4
            + result["fat"] * 9
            + result["carbs"] * 4
        )
        self.assertAlmostEqual(total_calories, 2450.9375)
            
            
            
    def test_macro_goals(self):
        loss = calculate_macros(2400, 60, "Lose Weight")
        maintenance = calculate_macros(2400, 60, "Maintain Weight")
        gain = calculate_macros(2400, 60, "Gain Weight")
        
        self.assertAlmostEqual(loss["protein"],120)
        self.assertAlmostEqual(maintenance["protein"],96)
        self.assertAlmostEqual(gain["protein"],108)
        self.assertGreater(loss["protein"], maintenance["protein"])    
    
            
            
    def test_invalid_macro_targets(self):
        with self.assertRaises(ValueError):
            calculate_macros(-100,60,"Maintain Weight")
        with self.assertRaises(ValueError):
            calculate_macros(100,100, "Lose Weight")        
            
    
if __name__ == "__main__":
    unittest.main()