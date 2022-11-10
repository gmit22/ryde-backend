from app import create_app
from flask import current_app
from database.config import TestConfig
import unittest
from unittest.mock import patch
import json
from middleware import user_client

class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json.dumps(json_data)
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        
class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        self.db = self.app.db

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None
    
    def test_app(self):
        assert self.app is not None
        assert self.db is not None
          
    @patch('middleware.user_client.add_user') 
    def test_add_user_positive_x(self, mock_uid):
        
        mock_uid.return_value = '636b0c918114e498c68d5c58'
        user = {
            "name": "abc123",
            "address": "Singadspore",
            "description": "testing add usser",
            "dob": "November 8, 2001"
        }  

        actual_result = user_client.create_new_user(user)
        self.assertIsNotNone(actual_result)
        self.assertIsInstance(actual_result, str)
        
        
    @patch('middleware.user_client.create_new_user') 
    def test_add_user_nodob(self, mock_uid):
        mock_uid.side_effect = [Exception("[parse_user] Cannot create user with no valid dob")]
        
        user = {
            "name": "abc123",
            "address": "Singadspore",
            "description": "testing add usser" 
        }  
        with self.assertRaises(Exception) as context:
            user_client.create_new_user(user)
            
        self.assertEqual("[parse_user] Cannot create user with no valid dob", str(context.exception))
    
    
    def test_add_user_with_created(self):
       
        user = {
            "name": "abc123",
            "address": "Singadspore",
            "description": "testing add usser",
            "dob": "22 March 2001",
            "createdAt": "2022-11-09T00:16:37.496Z"
        }  
               
        with self.assertRaises(Exception) as context:
            user_client.create_new_user(user)
        self.assertIn("The creation timing of the user has to be stamped by API", str(context.exception))
        self.assertIsNotNone(context)
   
    def test_add_user_nodob(self):
        user = {
            "name": "abc123",
            "address": "Singadspore",
            "description": "testing add usser" 
        }  
        with self.assertRaises(Exception) as context:
            user_client.create_new_user(user)
            
        self.assertIn("Cannot create user with no valid dob", str(context.exception))
    
    @patch('middleware.user_client.get_all_users')
    def test_get_users_empty_db(self, mock_users):
        mock_users.return_value = None
        users = user_client.get_all_users()
        self.assertIsNone(users)
    
    @patch('middleware.user_client.get_all_users') 
    def test_get_users_success(self, mock_users):
        mock_users.return_value = [{
                                    '_id': {
                                        '$oid': '636b033d6079a71583c4441d'
                                        }, 
                                    'name': 'abc123', 
                                    'dob': '21 Aug 2001', 
                                    'address': 'Singapore', 
                                    'description': 'testing add usser', 
                                    'createdAt': {
                                        '$date': '2022-11-08T20:32:45.935Z'
                                        }
                                    }
            ]
        
        users = user_client.get_all_users()
        self.assertEqual(1, len(users))
        
    @patch('middleware.user_client.get_user_by_id') 
    def test_get_non_existent_user(self, mock_user):
        mock_user.return_value = None
        u_id = "636b033d6079a71583c4441d"
        user_data = user_client.get_user_by_id(u_id)
        self.assertIsNone(user_data)
        
    @patch('middleware.user_client.get_user_by_id')
    def test_get_existent_user(self, mock_user):
        user_data = {
                        '_id': {
                            '$oid': '636b033d6079a71583c4441e'
                            }, 
                        'name': 'abc123', 
                        'dob': '21 Aug 2001', 
                        'address': 'Singapore', 
                        'description': 'testing add usser', 
                        'createdAt': {
                            '$date': '2022-11-08T20:32:45.935Z'
                            }
        }
        
        mock_user.return_value = user_data
        u_id = "636b033d6079a71583c4441e"
        
        actual_user_data = user_client.get_user_by_id(u_id)
        self.assertIsNotNone(actual_user_data)
    
    
 