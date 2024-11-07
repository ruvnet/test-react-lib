import os
import json
import uuid
import pytest
from unittest.mock import patch
from app import app as flask_app
from config import TestConfig

# Configure the Flask app for testing
flask_app.config.from_object(TestConfig)

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

# Mock data for Capitol AI API responses
def mock_generate_story_success(*args, **kwargs):
    return {
        "created": {
            "id": str(uuid.uuid4()),
            "content": "Generated story content."
        }
    }

def mock_get_story_success(*args, **kwargs):
    return {
        "id": kwargs.get('story_id'),
        "content": "Existing story content."
    }

def mock_update_story_success(*args, **kwargs):
    return {
        "id": kwargs.get('story_id'),
        "content": kwargs.get('content')
    }

# Test the home page GET request
def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Generate Stories' in response.data

# Test the home page POST request to generate stories
@patch('app.generate_story')
def test_home_post_generate_stories(mock_generate_story, client):
    # Configure the mock to return a successful response
    mock_generate_story.side_effect = [
        {"created": {"id": "story-id-1"}},
        {"created": {"id": "story-id-2"}}
    ]
    
    response = client.post('/', data={'userPrompt': 'Test prompt'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Edit Story: story-id-1' in response.data
    assert b'Edit Story: story-id-2' in response.data
    assert mock_generate_story.call_count == 2

# Test the edit_story GET request
@patch('app.get_story')
def test_edit_story_get(mock_get_story, client):
    mock_get_story.return_value = {
        "id": "story-id-1",
        "content": "Existing story content."
    }
    
    response = client.get('/story/story-id-1')
    assert response.status_code == 200
    assert b'Edit Story: story-id-1' in response.data
    assert b'Existing story content.' in response.data
    mock_get_story.assert_called_once_with('story-id-1')

# Test the edit_story POST request to update a story
@patch('app.update_story')
def test_edit_story_post(mock_update_story, client):
    mock_update_story.return_value = {
        "id": "story-id-1",
        "content": "Updated story content."
    }
    
    response = client.post('/story/story-id-1', data={'storyData': 'Updated story content.'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Edit Story: story-id-1' in response.data
    assert b'Updated story content.' in response.data
    mock_update_story.assert_called_once_with('story-id-1', {'content': 'Updated story content.'})

# Test error handling for story generation failure
@patch('app.generate_story')
def test_home_post_generate_stories_failure(mock_generate_story, client):
    # Configure the mock to return None indicating failure
    mock_generate_story.return_value = None
    
    response = client.post('/', data={'userPrompt': 'Test prompt'}, follow_redirects=True)
    assert response.status_code == 200
    # Since stories failed to generate, no story links should be present
    assert b'Edit Story' not in response.data
    assert mock_generate_story.call_count == 2  # Still attempted to generate two stories

# Test error handling for retrieving a non-existent story
@patch('app.get_story')
def test_edit_story_get_nonexistent(mock_get_story, client):
    mock_get_story.return_value = None
    
    response = client.get('/story/nonexistent-id')
    assert response.status_code == 200
    assert b'Edit Story: nonexistent-id' in response.data
    assert b'' == response.data.strip()  # No content
    mock_get_story.assert_called_once_with('nonexistent-id')

# Test authentication by ensuring API_KEY is used in generate_story
@patch('app.requests.post')
def test_generate_story_authentication(mock_post, client):
    # Mock successful API response
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "created": {
            "id": "story-id-3",
            "content": "Generated story content."
        }
    }
    
    response = client.post('/', data={'userPrompt': 'Test prompt'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Edit Story: story-id-3' in response.data
    
    # Verify that the API_KEY was used in the Authorization header
    args, kwargs = mock_post.call_args
    headers = kwargs.get('headers')
    assert headers['Authorization'] == f"Bearer {flask_app.config['API_KEY']}"

# Test CSRF protection is disabled in testing
def test_csrf_disabled(client):
    # Since CSRF is disabled, this form should be accepted without CSRF token
    response = client.post('/', data={'userPrompt': 'Test prompt'}, follow_redirects=True)
    # Assuming successful generation, but since we mocked generate_story in previous tests, 
    # here without mocking, it may fail. Adjust accordingly based on your implementation.
    # For demonstration, we'll just check the response status.
    assert response.status_code == 200
