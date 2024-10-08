# commercial imports
import json
import logging
import traceback
from pint import UnitRegistry

# constants
VALID_UNITS = ["Fahrenheit", "Celsius", "Kelvin", "Rankine"]
REQUIRED_KEYS = ['input_value', 'input_unit', 'target_unit', 'student_response']
ERROR_INVAlID_JSON = "Invalid JSON body"
ERROR_MISSING_KEY = "Missing required key: {}"
ERROR_INVALID_INPUT = "Input value must be a number"
ERROR_INVALID_UNIT = "Invalid {} unit. Supported units are: {}"
ERROR_INVALID_RESPONSE = "Student response must be a number"

# Set up logging for Lambda to CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO) # Change to DEBUG for more verbose logging

def lambda_handler(event, context):
    """
    Lambda function handler.

    Parameters:
        event (dict): A dictionary containing input values.
        context (object): An object containing information about the Lambda function's execution environment.

    Raises:
        Exception: If an error occurs during processing.

    Returns:
        dict: A dictionary containing the result of the comparison.
    """
    logger.info(f"Received event: {event}")

    try:
        # If the event body is a string, parse it as JSON
        if isinstance(event.get("body"), str):
            try:
                event = json.loads(event["body"])
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": ERROR_INVAlID_JSON})
                }

        # Check if all required keys are present in the event
        for key in REQUIRED_KEYS:
            if key not in event:
                raise KeyError(ERROR_MISSING_KEY.format(key))


        input_value = event['input_value']
        input_unit = event['input_unit']
        target_unit = event['target_unit']
        student_response = event['student_response']

        logger.info(f"Processing input_value: {input_value}, input_unit: {input_unit}, target_unit: {target_unit}, student_response: {student_response}")

        input_validation(event)

        authoritative_answer = convert_unit(input_value, input_unit, target_unit)
        response_status = check_response(authoritative_answer, student_response)

        # Log the result along with the input values
        logger.info(f"authoritative answer: {authoritative_answer}, response status: {response_status}")

        # Return a properly formatted response
        return {
            "statusCode": 200,
            "body": json.dumps({"result": response_status}),
        }
    except KeyError as e:
        logger.error(f"Missing required key: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        logger.error(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def input_validation(event):
    """
    Validate the input values in the event.

    Parameters:
        event (dict): A dictionary containing input values.

    Raises:
        ValueError: If the input value is not a number, or if the input or target units are invalid.

    Returns:
        None
    """
    try:
        input_value = event['input_value']
        input_unit = event['input_unit']
        target_unit = event['target_unit']
        student_response = event['student_response']

        logger.info(f"Validating input_value: {input_value}, input_unit: {input_unit}, target_unit: {target_unit}, student_response: {student_response}")

        if not isinstance(input_value, (int, float)):  # Check if the input value is a number
            raise ValueError(ERROR_INVALID_INPUT)
        if input_unit not in VALID_UNITS:  # Check if the input unit is valid
            raise ValueError(ERROR_INVALID_UNIT.format("input", ", ".join(VALID_UNITS)))
        if target_unit not in VALID_UNITS:  # Check if the target unit is valid
            raise ValueError(ERROR_INVALID_UNIT.format("target", ", ".join(VALID_UNITS)))
        if not isinstance(student_response, (int, float)):  # Check if the student response is a number
            raise ValueError(ERROR_INVALID_RESPONSE)
    except ValueError as e:
        logger.error(f"Input validation error: {e}")
        raise

# Convert a temperature value from one unit to another rounded to the nearest tenth
def convert_unit(value, from_unit, to_unit):
    """
    Convert a temperature value from one unit to another.

    Parameters:
        value (float): The temperature value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The unit to convert the value to.

    Raises:
        ValueError: If the input or target units are invalid.

    Returns:
        float: The converted temperature value rounded to the nearest tenth.
    """
    # Using the pint library to handle unit conversions
    ureg = UnitRegistry()

    # Create a dictionary of conversion factors
    conversion_factors = {
        "Fahrenheit": ureg.degF,
        "Celsius": ureg.degC,
        "Kelvin": ureg.K,
        "Rankine": ureg.degR,
    }

    # Ensure the from_unit and to_unit are valid
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        raise ValueError(ERROR_INVALID_UNIT.format("input or target",', '.join(conversion_factors.keys())))

    try:
        # Convert the input value to a Pint Quantity object
        input_quantity = ureg.Quantity(value, conversion_factors[from_unit])

        # Convert the input quantity to the target unit
        output_quantity = input_quantity.to(conversion_factors[to_unit])

        # Return the value of the output quantity
        return round(output_quantity.magnitude, 1)
    except Exception as e:
        logger.error(f"Error converting units: {e}")
        raise


def check_response(authoritative, student):
    """
    Check the student's response against the authoritative answer.

    Parameters:
        authoritative (float): The authoritative answer.
        student (float/int): The student's response.

    Raises:
        ValueError: If the student's response is not a valid number.

    Returns:
        str: The result of the comparison ("correct", "incorrect", or "invalid").
    """
    try:
        if round(float(student), 1) == authoritative:
            return "correct"
        else:
            return "incorrect"
    except ValueError:
        return "invalid response"
