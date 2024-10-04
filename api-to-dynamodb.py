import json
import requests
import boto3
from datetime import datetime
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("weatherdata")

# Function to fetch weather data from the API
def get_weather_data(city):
    api_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "q": city,
        "key": "_____________________________"  # Replace with your actual API key
    }
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

# Lambda handler function
def lambda_handler(event, context):
    cities = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Kashmir", "Dehradun", "Kochi", "Kerala", "Hyderabad", "Sikkim"]
    
    for city in cities:
        # Fetch data for each city
        data = get_weather_data(city)
        temp = data['current']['temp_c']
        wind_speed = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        pressure_mb = data['current']['pressure_mb']
        humidity = data['current']['humidity']
        
        # Print the extracted weather data (optional for debugging)
        print(f"{city}: Temp={temp}, Wind Speed={wind_speed}, Wind Dir={wind_dir}, Pressure={pressure_mb}, Humidity={humidity}")
        
        # Get the current timestamp
        current_timestamp = datetime.utcnow().isoformat()
        # Create an item for DynamoDB
        item = {
            'city': city,
            'time': str(current_timestamp),
            'temp': temp,
            'wind_speed': wind_speed,
            'wind_dir': wind_dir,
            'pressure_mb': pressure_mb,
            'humidity': humidity
        }
        
        # Convert item data types to DynamoDB compatible format
        item = json.loads(json.dumps(item), parse_float=Decimal)
        
        # Insert data into DynamoDB
        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data stored successfully!')
    }