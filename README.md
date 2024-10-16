# Audiobook Managment System APIs using FastAPI and Sqlite3

## Overview
This repository contains the source code developed as an assignment for the SWE role at Senquire. The project focuses on integrating the Audiobook Management System APIs with FastAPI. 

## Tech Stack
The project utilizes the following technologies:

- FastAPI
- JWT for authentication
- SQLAlchemy
- Docker

## Setup 
To run this project, you need to have Docker and Docker Compose installed on your machine. 

1. Clone the repository
2. Run the following command to start the project:
```bash
docker-compose up --build
```
3. The FastAPI server will be running on `http://localhost:8000`
4. Go to `http://localhost:8000/login` and enter the hardcoded username: `john_doe` and password: `1234` to get the JWT token.
5. Pass this token in the Authorization header as a Bearer token to access the protected routes.   

## API Documentation
The API documentation can be accessed at `http://localhost:8000/docs`

