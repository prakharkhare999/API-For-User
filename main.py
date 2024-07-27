from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Body
import boto3
import uuid
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Boto3 session and DynamoDB resource
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
    raise ValueError("AWS credentials and region must be provided")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('demo2')  # Replace with your DynamoDB table name

# Check API is running
@app.get("/")
async def api():
    return {"message": "API is running successfully! Try '/get_users' to fetch all users"}

# Endpoint to create a user
@app.post("/add_users", status_code=201)
async def create_user(user_detail: Dict[str, Any] = Body(...)):
    try:
        # Generate a unique user_id
        user_id = str(uuid.uuid4())
        user_detail['user_id'] = user_id
        
        # Add user detail to DynamoDB
        response = table.put_item(Item=user_detail)
        logger.info("User created successfully: %s", user_detail)
        
        return {"message": "User created successfully", "user_id": user_id, "user_detail": user_detail}
    except Exception as e:
        logger.error("Error creating user: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to get all users
@app.get("/get_users")
async def get_users():
    try:
        response = table.scan()
        logger.info("Fetched all users")
        return response['Items']
    except Exception as e:
        logger.error("Error fetching users: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to get user by ID
@app.get("/get_user/{user_id}")
async def get_user(user_id: str):
    try:
        response = table.get_item(Key={'user_id': user_id})
        item = response.get('Item')
        if item:
            logger.info("Fetched user: %s", item)
            return item
        else:
            logger.warning("User not found: %s", user_id)
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Error fetching user: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to update user by ID
@app.patch("/update_user/{user_id}")
async def update_user(user_id: str, user_detail: Dict[str, Any] = Body(...)):
    try:
        # Retrieve existing user data
        existing_user_response = table.get_item(Key={'user_id': user_id})
        existing_user = existing_user_response.get('Item')
        
        if not existing_user:
            logger.warning("User not found for update: %s", user_id)
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression_parts = []
        expression_attribute_values = {}
        
        for key, value in user_detail.items():
            if key in existing_user:
                update_expression_parts.append(f"{key} = :{key}")
                expression_attribute_values[f":{key}"] = value
            else:
                logger.warning("Attribute '%s' not found in existing user details", key)
                raise HTTPException(status_code=400, detail=f"Attribute '{key}' not found in existing user details")
        
        # Build UpdateExpression
        update_expression = "SET " + ", ".join(update_expression_parts)
        
        # Update user detail in DynamoDB
        response = table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'  # Return updated item
        )
        
        updated_item = response.get('Attributes', {})
        logger.info("User updated successfully: %s", updated_item)
        return updated_item
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating user: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to delete user by ID
@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: str):
    try:
        response = table.delete_item(Key={'user_id': user_id})
        if response.get('ConsumedCapacity'):
            logger.info("User deleted successfully: %s", user_id)
            return {"message": "User deleted successfully"}
        else:
            logger.warning("User not found for deletion: %s", user_id)
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Error deleting user: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
