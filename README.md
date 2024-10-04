# Real-Time Weather Data Pipeline using lambda

## Project Overview
This project implements a real-time data pipeline for fetching weather data from the Weather API, storing it in DynamoDB, transferring it to S3, and loading it into Snowflake for analysis. The architecture leverages AWS Lambda functions to facilitate data extraction and movement across services, ensuring a seamless flow of weather data.

## Architecture Diagram
![Architecture Diagram](path/to/architecture_diagram.png)  <!-- Update with the path to your architecture diagram -->

## Architecture Explanation
1. **Weather API**: Data is extracted from the Weather API, which provides real-time weather information based on city queries.
2. **AWS Lambda Functions**:
   - **api-to-dynamodb**: Fetches weather data from the API and stores it in DynamoDB.
   - **dynamodb-to-s3**: Listens for DynamoDB stream events and transfers the new data to S3.
3. **DynamoDB**: Serves as the primary data store for weather data, with a partition key of `city` and a sort key of `time`.
4. **Amazon S3**: Stores the weather data in CSV format, ready to be loaded into Snowflake.
5. **Snowflake**: Utilizes Snowpipe to load data from S3 into Snowflake tables for analysis.


## Technologies and Tools Used
- **AWS Lambda**: Serverless compute service for running code without provisioning servers.
- **DynamoDB**: NoSQL database service for storing structured data.
- **Amazon S3**: Scalable storage service for storing and retrieving data.
- **Snowflake**: Cloud data platform for data warehousing and analytics.
- **Weather API**: External API for retrieving real-time weather data.
- **Python**: Programming language used for writing Lambda function code.


## Workflow
1. **Create Weather API Account**: 
   - Go to [Weather API](https://www.weatherapi.com/) to create an account and obtain an API key.

2. **Create Lambda Function for API to DynamoDB**: 
   - In AWS Lambda, create a function named `api-to-dynamodb` with the runtime set to Python 3.11.

3. **Create DynamoDB Table**: 
   - Create a table named `weatherdata` with the partition key as `city` and the sort key as `time`.

4. **Write Code for Data Extraction**: 
   - Implement the code to fetch weather data from the Weather API and store it in DynamoDB.

5. **Set Permissions**: 
   - Go to the configuration section of the Lambda function and add necessary permissions (DynamoDB full access) to the automatically created IAM role.

6. **Add Dependencies**: 
   - Include any necessary dependencies in a Lambda layer.

7. **Deploy and Test the Lambda Function**: 
   - Deploy the Lambda function and test it to ensure data is stored in the DynamoDB table successfully.

8. **Create Second Lambda Function for DynamoDB to S3**: 
   - Create another function named `dynamodb-to-s3`. In this function, set permissions for both S3 full access and DynamoDB full access.

9. **Create S3 Bucket**: 
   - Create an S3 bucket named `weather-api-project-bucket` to store the CSV files.

10. **Write Code for Data Transfer**: 
    - Implement the code to transfer data from DynamoDB to S3.

11. **Set Up DynamoDB Stream**: 
    - Add a trigger to the second Lambda function to link it to the DynamoDB table's stream. This allows the function to be invoked automatically when new records are added.

12. **Load Data into Snowflake**: 
    - Utilize Snowpipe to load data from S3 into Snowflake tables. Create a role called `aws-snowflake` to manage necessary permissions for this operation.

13. **Analyze Data**: 
    - Perform analysis on the data loaded into Snowflake.

## Error Resolution
During testing, an issue arose where the second Lambda function, responsible for handling DynamoDB stream events, was not triggered upon new record inserts into the DynamoDB table. This resulted in data being added to the table without being processed or uploaded to S3.
### Investigation and Resolution Steps:
1. **Issue Identification**: Confirmed that the second Lambda function was not receiving events from the DynamoDB stream.
2. **Investigation**: Verified that the DynamoDB stream was enabled and configured to capture new item inserts. Checked CloudWatch logs for the second Lambda function and confirmed that no events were being processed.
3. **Root Cause**: Discovered that the second Lambda function lacked a DynamoDB trigger, which prevented it from being invoked automatically when new records were added.
4. **Solution**: Added a trigger to the second Lambda function in the AWS Management Console, linking it to the DynamoDB table’s stream. After setting up the trigger, manually inserted a new record into the DynamoDB table to confirm that the function was triggered successfully, uploading the data to S3.
5. **Outcome**: With the trigger correctly configured, the second Lambda function now processes new inserts from the DynamoDB stream, ensuring a consistent data flow from DynamoDB to S3.

## Conclusion
The real-time weather data pipeline successfully fetches weather data, stores it in DynamoDB, transfers it to S3, and loads it into Snowflake for analysis. The architecture is designed to ensure a seamless flow of data while utilizing serverless technologies for scalability and efficiency.

