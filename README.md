# DevOps Challenge - Unit Conversion Application

## Overview
This application is built to assist science teachers in grading unit conversion problems. It allows teachers to input a numerical value, the input unit of measure, the target unit of measure, and the student's response, and it will determine whether the student's response is correct, incorrect, or invalid.

The system performs conversions between Kelvin, Celsius, Fahrenheit, and Rankine units, and evaluates the student's response based on the correct conversion, rounded to the tenths place.

This application is deployed using AWS Lambda and integrates with AWS API Gateway to expose a REST API for users to interact with.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Deployment](#deployment)
4. [API Usage](#api-usage)
5. [Improvements](#improvements)
6. [Conclusion](#conclusion)

---

## Prerequisites
To set up and run this project locally, you'll need the following:

- AWS CLI (version 2) installed and configured
- AWS SAM (Serverless Application Model) CLI installed
- Python 3.11+ installed
- Access to an AWS account with permissions to deploy AWS Lambda and API Gateway
- A code editor (e.g., VSCode, IntelliJ IDEA) for development

---

## Setup

### 1. Clone the repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-repo-url/devops-challenge.git
cd devops-challenge
```

### 2. Install dependencies
Make sure you have Python 3.11 or higher. Install any necessary dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Run the application locally (optional)
You can test the application locally using AWS SAM:
```bash
sam local invoke -e events/event.json
```
This will invoke the Lambda function locally using a test event specified in `event.json`.

---

## Deployment

To deploy the application to AWS using AWS Lambda and API Gateway, follow these steps:

### 1. Build the application
Build the serverless application using SAM:
```bash
sam build
```

### 2. Deploy the application
Deploy the built application to AWS:
```bash
sam deploy --guided
```
You will be prompted to provide configuration details such as the stack name, AWS region, and an S3 bucket for deployment.

After deployment, SAM will provide an API Gateway URL that you can use to interact with the application.

---

## API Usage

Once deployed, you can interact with the application via the exposed REST API. The API accepts a POST request with the following JSON body format:

### Request
```json
{
  "input_value": 84.2,
  "input_unit": "Fahrenheit",
  "target_unit": "Rankine",
  "student_response": "543.9"
}
```

### Response
- **Correct**: The student's response matches the correct answer after rounding to the tenths place.
- **Incorrect**: The student's response does not match.
- **Invalid**: The student response or units provided are invalid.

### Example cURL Request
```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/convert \
-d '{
  "input_value": 84.2,
  "input_unit": "Fahrenheit",
  "target_unit": "Rankine",
  "student_response": "543.9"
}'
```

---

## Improvements
Here are some potential improvements for the application that can be implemented in future iterations:

1. **Additional Unit Conversions**: Add support for additional units of measure beyond temperature conversions (e.g., length, weight).
2. **UI/UX Improvements**: Create a simple web interface that allows non-technical users (teachers) to interact with the system.
3. **Error Handling**: Improve error handling for invalid inputs and units with more user-friendly messages.
4. **Logging and Monitoring**: Integrate AWS CloudWatch for detailed logging and monitoring of API requests and Lambda executions.
5. **Scalability**: Implement database integration (e.g., DynamoDB) for storing student responses and results for further analysis and reporting.

---

## Conclusion
This application demonstrates a simple yet effective way to handle unit conversion problems in a serverless environment using AWS Lambda and API Gateway. Teachers can now easily input data and get responses in real time, improving the efficiency of their grading process.
