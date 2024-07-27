FastAPI User Management API
===========================

This project is a unified API using FastAPI to handle user management for three different projects, with data stored in AWS DynamoDB. The API supports operations such as creating, retrieving, updating, and deleting users.

Table of Contents
-----------------

*   [Features](#features)
*   [Requirements](#requirements)
*   [Installation](#installation)
*   [Configuration](#configuration)
*   [Usage](#usage)
*   [Endpoints](#endpoints)
*   [Contributing](#contributing)
*   [License](#license)

Features
--------

*   Create, retrieve, update, and delete user information
*   Dynamic JSON handling without static field definitions
*   Optimized for handling large data sets with DynamoDB
*   Detailed error handling and logging

Requirements
------------

*   Python 3.7+
*   FastAPI
*   AWS DynamoDB
*   Git

Installation
------------

1.  **Clone the repository:**
    
        git clone https://github.com/prakharkhare999/API-For-User.git
        cd API-For-User
    
2.  **Create a virtual environment:**
    
        python -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
    
3.  **Install dependencies:**
    
        pip install -r requirements.txt
    

Configuration
-------------

1.  **Create a `.env` file in the root directory and add your AWS credentials:**
    
        AWS_ACCESS_KEY_ID=your_access_key_id
        AWS_SECRET_ACCESS_KEY=your_secret_access_key
        AWS_REGION=your_aws_region
        DYNAMODB_TABLE=your_dynamodb_table_name
    
2.  **Ensure your `.env` file is listed in `.gitignore` to prevent it from being pushed to the repository.**

Usage
-----

1.  **Run the FastAPI application:**
    
        uvicorn main:app --reload
    
2.  **Access the API documentation:**
    *   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI.

Endpoints
---------

*   **Create User**: `POST /users/`
*   **Get User by ID**: `GET /users/{user_id}`
*   **Update User by ID**: `PUT /users/{user_id}`
*   **Delete User by ID**: `DELETE /users/{user_id}`

Contributing
------------

Contributions are welcome! Please follow these steps to contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature-branch`).
6.  Open a pull request.

 
