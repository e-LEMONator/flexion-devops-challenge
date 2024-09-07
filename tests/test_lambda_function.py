import unittest
from unittest.mock import patch
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
        self.assertEqual(result['result'], 'correct')

        # Test incorrect response
        test_event = event.copy()
        test_event['student_response'] = 1.0
        result = lambda_handler(test_event, None)
        self.assertEqual(result['result'], 'incorrect')

        # # Test invalid response
        # test_event = event.copy()
        # test_event['student_response'] = 'invalid'
        # result = lambda_handler(test_event, None)
        # self.assertEqual(result['result'], 'invalid')
        #
        # # Test invalid unit
        # test_event = event.copy()
        # test_event['input_unit'] = 'InvalidUnit'
        # result = lambda_handler(test_event, None)
        # self.assertIn('error', result)

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