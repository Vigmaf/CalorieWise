import unittest
from pathlib import Path
from tempfile import TemporaryDirectory #creates an isolated directory that is automatically clenaed up after testing
from unittest.mock import patch # temporarliy replaces an attribute, used to redirect operations to a temporary database instead of real SQLite file
import database
from calculator import calculate_calories, calculate_macros

class TestDatabase(unittest.TestCase):
    def test_database_workflow(self):
        
        #create an silotaed tepmorary database
        with TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "test_caloriewise.db"
            
            #redicerct all databae operations
            with patch.object(database, "DB_PATH", test_path):
                database.initialize_database()
                
                # Generate sample calorie results
                results = calculate_calories(
                    21, 60, 173,
                    "Male",
                    "Moderately Active",
                    "Maintain Weight"
                )
                
                # Generate sample macronutrient results
                macros = calculate_macros(
                    results["target"],
                    60,
                    "Maintain Weight"
                )
                
                # Combine everything into one calculation
                calculation = {
                    "age": 21,
                    "weight": 60,
                    "height": 173,
                    "sex": "Male",
                    "activity": "Moderately Active",
                    "goal": "Maintain Weight",
                    **results,
                    **macros
                }


                #test 1: save
                record_id = database.save_calculation(calculation)
                self.assertIsInstance(record_id, int)

                #TEST 2: RETRIEVE
                records = database.get_calculations()

                self.assertEqual(len(records), 1)
                self.assertEqual(records[0]["id"], record_id)

                # Verify actual stored values
                self.assertAlmostEqual(
                    records[0]["target"], 2450.9375
                )

                self.assertAlmostEqual(
                    records[0]["protein"], 96.0
                )

                self.assertAlmostEqual(
                    records[0]["carbs"], 332.9140625
                )

                self.assertAlmostEqual(
                    records[0]["fat"], 81.6979166667
                )
                
                # TEST 3: DELETE EXISTING RECORD
                deleted = database.delete_calculation(record_id)

                self.assertTrue(deleted)

                # Verify the database is empty
                records = database.get_calculations()

                self.assertEqual(len(records), 0)

                # TEST 4: DELETE NONEXISTENT RECORD
                deleted_again = database.delete_calculation(record_id)

                self.assertFalse(deleted_again)
