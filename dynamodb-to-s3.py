import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

# Function to handle "INSERT" event in DynamoDB
def handle_insert(record):
    print("Handling Insert: ", record)
    record_dict = {}
    
    # Extract the new image (inserted data) from the DynamoDB record
    for key, value in record['dynamodb']['NewImage'].items():
        record_dict[key] = list(value.values())[0]
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame([record_dict])
    return df

# Main Lambda handler function
def lambda_handler(event, context):
    print(event)  # Print the event for debugging
    
    dfs = []  # List to hold dataframes
    
    # Loop through each record in the event
    for record in event['Records']:
        # Extract the table name from the event source ARN
        table = record['eventSourceARN'].split("/")[1]
        
        # If the event is an INSERT event, process it
        if record['eventName'] == "INSERT":
            df = handle_insert(record)
            dfs.append(df)
    
    # If there are any dataframes (records processed), concatenate them
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        df = df.astype(str)  # Convert dataframe values to string
        
        # Create a CSV buffer and write the dataframe to it
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Define the S3 bucket and key (path) to store the CSV
        s3 = boto3.client('s3')
        bucket_name = "weather-api-project-bucket"
        path = table + "_" + str(datetime.now()) + ".csv"
        key = "snowflake/" + path
        
        print(f"Uploading file to S3: {key}")
        
        try:
            # Upload the CSV data to S3
            s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
            print(f"Successfully uploaded {len(event['Records'])} records.")
        except Exception as e:
            print(f"Failed to upload records: {e}")
    else:
        print('No INSERT records found in the event.')

