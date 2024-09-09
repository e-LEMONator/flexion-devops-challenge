# commercial imports
import json
import unittest

# local imports
from lambda_function import lambda_handler, convert_unit, input_validation

class TestLambdaFunction(unittest.TestCase):

    def test_convert_unit(self):
        # Test conversions between temperature units
        self.assertAlmostEqual(convert_unit(32, "Fahrenheit", "Celsius"), 0.0)
        self.assertAlmostEqual(convert_unit(0, "Celsius", "Fahrenheit"), 32.0)
        self.assertAlmostEqual(convert_unit(273.15, "Kelvin", "Celsius"), 0.0)
        self.assertAlmostEqual(convert_unit(0, "Celsius", "Kelvin"), 273.1)
        self.assertAlmostEqual(convert_unit(491.67, "Rankine", "Fahrenheit"), 32.0)

        # Test invalid input unit
        with self.assertRaises(ValueError):
            convert_unit(100, "InvalidUnit", "Celsius")

        # Test invalid target unit
        with self.assertRaises(ValueError):
            convert_unit(100, "Celsius", "InvalidUnit")

    def test_lambda_handler(self):
        # Test correct response
        event = {
            'input_value': 32,
            'input_unit': 'Fahrenheit',
            'target_unit': 'Celsius',
            'student_response': 0.0
        }
        result = lambda_handler(event, None)
        result = json.loads(result['body'])
        self.assertEqual(result['result'], 'correct')

        # Test incorrect response
        test_event = event.copy()
        test_event['student_response'] = 1.0
        result = lambda_handler(test_event, None)
        result = json.loads(result['body'])
        self.assertEqual(result['result'], 'incorrect')

        # Test invalid JSON input
        invalid_json_event = {
            "body": "invalid"
        }
        result = lambda_handler(invalid_json_event, None)
        result_body = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result_body['error'], "Invalid JSON body")

        # Test missing required key
        missing_key_event = {
            'input_value': 32,
            'input_unit': 'Fahrenheit',
            'student_response': 0.0
        }
        result = lambda_handler(missing_key_event, None)
        result_body = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 400)
        self.assertTrue("Missing required key" in result_body['error'])

    def test_input_validation(self):
        # Test valid input
        event = {
            'input_value': 32,
            'input_unit': 'Fahrenheit',
            'target_unit': 'Celsius',
            'student_response': 0.0
        }
        input_validation(event)

        # Test invalid input value
        test_event = event.copy()
        test_event['input_value'] = 'invalid'
        with self.assertRaises(ValueError):
            input_validation(test_event)

        # Test invalid input unit
        test_event = event.copy()
        test_event['input_unit'] = 'InvalidUnit'
        with self.assertRaises(ValueError):
            input_validation(test_event)

        # Test invalid target unit
        test_event = event.copy()
        test_event['target_unit'] = 'InvalidUnit'
        with self.assertRaises(ValueError):
            input_validation(test_event)

        # Test invalid student response
        test_event = event.copy()
        event['student_response'] = "invalid"
        with self.assertRaises(ValueError):
            input_validation(event)

if __name__ == '__main__':
    unittest.main()