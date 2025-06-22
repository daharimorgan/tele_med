import os
import json
import uuid
import datetime
import boto3
from typing import Dict, Any, List, Optional

# AWS Clients
dynamodb = boto3.resource('dynamodb')

# Tables
USERS_TABLE = dynamodb.Table(os.environ.get('USERS_TABLE', 'Users'))
PATIENTS_TABLE = dynamodb.Table(os.environ.get('PATIENTS_TABLE', 'Patients'))
CARE_TEAMS_TABLE = dynamodb.Table(os.environ.get('CARE_TEAMS_TABLE', 'CareTeams'))
CARE_PLANS_TABLE = dynamodb.Table(os.environ.get('CARE_PLANS_TABLE', 'CarePlans'))
APPOINTMENTS_TABLE = dynamodb.Table(os.environ.get('APPOINTMENTS_TABLE', 'Appointments'))

def generate_simple_token(username: str) -> str:
    """
    Generates a simple token for the given username.
    """
    return f"token_{uuid.uuid4()}_{username}"

def create_user(username: str, email: str, password: str, role: str) -> Dict[str, Any]:
    """
    Creates a new user in the system.
    """
    try:
        # Create the user in DynamoDB
        user_id = str(uuid.uuid4())
        USERS_TABLE.put_item(
            Item={
                'id': user_id,
                'username': username,
                'email': email,
                'password': password,  # Stored in plain text for now (temporary)
                'role': role,
                'created_at': datetime.datetime.now().isoformat()
            }
        )
        
        return {
            'id': user_id,
            'username': username,
            'email': email,
            'role': role
        }
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise

def get_user(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a user by username.
    """
    try:
        user = USERS_TABLE.get_item(Key={'username': username}).get('Item')
        return user
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return None

def create_care_team(patient_id: str, primary_provider_id: str, team_members: List[str]) -> Dict[str, Any]:
    """
    Creates a new care team for a patient.
    """
    try:
        # Create the care team in DynamoDB
        team_id = str(uuid.uuid4())
        CARE_TEAMS_TABLE.put_item(
            Item={
                'id': team_id,
                'patient_id': patient_id,
                'primary_provider_id': primary_provider_id,
                'team_members': team_members,
                'created_at': datetime.datetime.now().isoformat()
            }
        )
        
        return {
            'id': team_id,
            'patient_id': patient_id,
            'primary_provider_id': primary_provider_id,
            'team_members': team_members
        }
    except Exception as e:
        print(f"Error creating care team: {str(e)}")
        raise

def create_care_plan(patient_id: str, created_by: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new care plan for a patient.
    """
    try:
        # Create the care plan in DynamoDB
        plan_id = str(uuid.uuid4())
        CARE_PLANS_TABLE.put_item(
            Item={
                'id': plan_id,
                'patient_id': patient_id,
                'created_by': created_by,
                'plan_data': plan_data,
                'status': 'active',
                'created_at': datetime.datetime.now().isoformat()
            }
        )
        
        return {
            'id': plan_id,
            'patient_id': patient_id,
            'created_by': created_by,
            'plan_data': plan_data,
            'status': 'active'
        }
    except Exception as e:
        print(f"Error creating care plan: {str(e)}")
        raise

def create_appointment(patient_id: str, provider_id: str, scheduled_time: str, appointment_type: str) -> Dict[str, Any]:
    """
    Creates a new appointment for a patient.
    """
    try:
        # Create the appointment in DynamoDB
        appointment_id = str(uuid.uuid4())
        APPOINTMENTS_TABLE.put_item(
            Item={
                'id': appointment_id,
                'patient_id': patient_id,
                'provider_id': provider_id,
                'scheduled_time': scheduled_time,
                'appointment_type': appointment_type,
                'status': 'scheduled',
                'created_at': datetime.datetime.now().isoformat()
            }
        )
        
        return {
            'id': appointment_id,
            'patient_id': patient_id,
            'provider_id': provider_id,
            'scheduled_time': scheduled_time,
            'appointment_type': appointment_type,
            'status': 'scheduled'
        }
    except Exception as e:
        print(f"Error creating appointment: {str(e)}")
        raise

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    """
    try:
        # Parse the request
        http_method = event.get('httpMethod')
        path = event.get('path')
        headers = event.get('headers', {})
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        query_params = event.get('queryStringParameters', {})
        
        # Simple authentication check
        auth_header = headers.get('Authorization')
        user = None
        if auth_header:
            # In a real application, you would validate the token here
            # For now, we're using a simple check
            token_parts = auth_header.split(' ')
            if len(token_parts) == 2 and token_parts[0] == 'Bearer':
                # In a real application, you would validate the token here
                # For now, we're just checking if the token starts with 'token_'
                if token_parts[1].startswith('token_'):
                    # Extract username from token (temporary solution)
                    username = token_parts[1].split('_')[-1]
                    user = get_user(username)
        
        # Handle different routes
        if path == '/register' and http_method == 'POST':
            # Register a new user
            username = body.get('username')
            email = body.get('email')
            password = body.get('password')
            role = body.get('role', 'patient')
            
            if not username or not email or not password:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            user = create_user(username, email, password, role)
            token = generate_simple_token(username)
            return {
                'statusCode': 201,
                'body': json.dumps({'user': user, 'token': token})
            }
        
        elif path == '/login' and http_method == 'POST':
            # Login a user
            username = body.get('username')
            password = body.get('password')
            
            if not username or not password:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            user = get_user(username)
            if not user or user.get('password') != password:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Invalid credentials'})
                }
            
            token = generate_simple_token(username)
            return {
                'statusCode': 200,
                'body': json.dumps({'token': token})
            }
        
        elif path == '/care-teams' and http_method == 'POST':
            # Create a new care team
            if not user:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Unauthorized'})
                }
            
            patient_id = body.get('patient_id')
            primary_provider_id = body.get('primary_provider_id')
            team_members = body.get('team_members', [])
            
            if not patient_id or not primary_provider_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            care_team = create_care_team(patient_id, primary_provider_id, team_members)
            return {
                'statusCode': 201,
                'body': json.dumps(care_team)
            }
        
        elif path == '/care-plans' and http_method == 'POST':
            # Create a new care plan
            if not user:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Unauthorized'})
                }
            
            patient_id = body.get('patient_id')
            plan_data = body.get('plan_data', {})
            
            if not patient_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            care_plan = create_care_plan(patient_id, user['id'], plan_data)
            return {
                'statusCode': 201,
                'body': json.dumps(care_plan)
            }
        
        elif path == '/appointments' and http_method == 'POST':
            # Create a new appointment
            if not user:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Unauthorized'})
                }
            
            patient_id = body.get('patient_id')
            provider_id = body.get('provider_id')
            scheduled_time = body.get('scheduled_time')
            appointment_type = body.get('appointment_type')
            
            if not patient_id or not provider_id or not scheduled_time or not appointment_type:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            appointment = create_appointment(patient_id, provider_id, scheduled_time, appointment_type)
            return {
                'statusCode': 201,
                'body': json.dumps(appointment)
            }
        
        else:
            # Handle unknown routes
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }