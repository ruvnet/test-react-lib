import os
from dotenv import load_dotenv
import json

# Test Configuration Options
# Uncomment and modify these values to customize test behavior
"""
--test-options--
# Skip integration tests
pytest.mark.skip_integration = True

# Mock API responses
mock_api_responses = True 

# Test timeouts
test_timeout = 30  # seconds

# Verbose output
debug_output = True

# API retry attempts
max_retries = 3

# Test data paths
test_data_dir = "tests/data"
"""
import requests
import uuid
from datetime import datetime, UTC
import pytest
from unittest.mock import patch, Mock

# Load environment variables from .env file
load_dotenv()

def get_env_config():
    """Get environment configuration"""
    return {
        'api_url': os.getenv('API_URL'),
        'capitol_api_key': os.getenv('VITE_CAPITOL_API_KEY'),
        'capitol_api_url': os.getenv('VITE_CAPITOL_API_URL')
    }

# Configuration matching App.jsx
technical_report_config = {
    "format": "custom",
    "cot": True,
    "audience": "General",
    "responseLength": "",
    "responseLanguage": "english",
    "heroImage": False,
    "title": False,
    "headers": True,
    "paragraphs": True,
    "images": False,
    "aiImages": False,
    "imageStyle": "auto",
    "aiGraphs": False,
    "webGraphs": False,
    "metrics": False,
    "tables": False,
    "quotes": False,
    "tweets": False,
    "tweetCharacterLimit": 280,
    "generalWebSearch": False,
    "academicWebSearch": False,
    "usePerplexity": False,
    "ragBudget": "default",
    "customInstructions": "Please create a Technical Proposal demonstrating your capability to implement the grant project, organized with the following sections: 1) **Project Description** (50 points), detailing services in counseling, training, access to capital, and knowledge transfer, including defining your geographic area and entrepreneurial ecosystem, describing measurable activities to support women entrepreneurs, identifying key stakeholders and partners with proof of third-party commitments, explaining how you will engage with SBA resources, and addressing efforts to engage women entrepreneurs from underserved communities; 2) **Applicant Capability** (25 points), providing a concise summary of your organization's mission, programs, relevant experience, proof of capability including financial and management infrastructure, organizational structure with duties and reporting, and one-page biographies or resumes of key personnel; 3) **Data Collection and Program Evaluation** (25 points), outlining your data collection plan including specific participant data and collection methods, plans to document lessons learned, identification of effective service models for potential replication, and how data will inform program delivery; 4) **Applicant Budget** (10 points), including the required Standard Forms SF-424 and SF-424A, and a Detailed Expenditure Worksheet with detailed justification for all budget items; and 5) **Agency Priority Points** (10 points), addressing at least two of SBA's priority areas such as promoting entrepreneurship among returning citizens, supporting rural entrepreneurial ecosystems, or increasing women's capacity to access government contracting opportunities, describing current efforts, past results, and execution plans through the WBC project. Ensure all required attachments, such as proof of third-party commitments and resumes, are included, and incorporate required travel costs for key personnel to attend specified events.",
    "imageHeight": 768,
    "imageWidth": 1344,
    "responseModel": "claude-3-5-sonnet-20240620",
    "userUrls": ["https://gist.github.com/zstone-cai/323e78d0b0e0f9f312105d2c1595bcbd"],
    "userPdfDocuments": [],
    "userPdfUrls": [],
    "userImages": []
}

abstract_report_config = {
    "format": "custom",
    "cot": False,
    "audience": "General",
    "responseLength": "1 page",
    "responseLanguage": "english",
    "heroImage": False,
    "title": False,
    "headers": True,
    "paragraphs": True,
    "images": False,
    "aiImages": False,
    "imageStyle": "auto",
    "aiGraphs": False,
    "webGraphs": False,
    "metrics": False,
    "tables": False,
    "quotes": False,
    "tweets": False,
    "tweetCharacterLimit": 280,
    "generalWebSearch": False,
    "academicWebSearch": False,
    "usePerplexity": False,
    "ragBudget": "default",
    "customInstructions": "Please generate an abstract of no more than one page summarizing the proposed project, including the scope of the project and proposed outcomes. The abstract must include the following sections: 1) Applicant's name; 2) Designated point of contact's telephone number and email address; 3) Web address; 4) Project title; 5) Description of the area to be served; 6) Number of participants to be served; and 7) Funding level requested.",
    "imageHeight": 768,
    "imageWidth": 1344,
    "responseModel": "claude-3-5-sonnet-20240620",
    "userUrls": ["https://gist.github.com/zstone-cai/323e78d0b0e0f9f312105d2c1595bcbd"],
    "userPdfDocuments": [],
    "userPdfUrls": [],
    "userImages": []
}

def generate_story(story_config):
    """Generate a story using Capitol AI API"""
    config = get_env_config()
    story_id = str(uuid.uuid4())
    current_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Get and validate API key
    api_key = config["capitol_api_key"]
    if not api_key:
        raise ValueError("Capitol API key is missing")
    
    # Validate API URL
    api_url = config["api_url"]
    if not api_url:
        raise ValueError("API URL is missing")
    if not api_url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid API URL format: {api_url}")
    
    # Clean and validate API key format
    api_key = api_key.strip()
    
    # Handle different API key formats
    if api_key.lower().startswith('bearer '):
        api_key = api_key[7:].strip()  # Remove existing Bearer prefix
    
    # Validate API key format
    if len(api_key) < 32:  # Typical minimum length for API keys
        raise ValueError(f"API key seems too short: {len(api_key)} chars")
    
    # Allow common API key special characters including Base64 chars
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._/+=')
    if not all(c in valid_chars for c in api_key):
        invalid_chars = [c for c in api_key if c not in valid_chars]
        raise ValueError(f"API key contains invalid characters: {invalid_chars}")
    
    # Ensure no whitespace in the key itself
    if any(c.isspace() for c in api_key):
        raise ValueError("API key contains whitespace characters")
        
    # Format with Bearer prefix
    api_key = f'Bearer {api_key}'
    
    headers = {
        'Authorization': api_key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Capitol-AI-Test/1.0'  # Add User-Agent header
    }
    
    # Enhanced debug logging
    print("\nAPI Request Details:")
    print(f"- API URL: {config['api_url']}")
    print(f"- API Key Format:")
    print(f"  - Total length: {len(api_key)} chars")
    print(f"  - Prefix: '{api_key[:10]}...'")
    print(f"  - Contains whitespace: {any(c.isspace() for c in api_key)}")
    print(f"  - Contains non-ASCII: {any(ord(c) >= 128 for c in api_key)}")
    
    # Log full headers except sensitive data
    print("\nRequest Headers:")
    for key, value in headers.items():
        if key.lower() == 'authorization':
            print(f"  {key}: Bearer [REDACTED]")
        else:
            print(f"  {key}: {value}")
    
    url = f"{config['api_url']}/api/latest/stories/story"
    
    # Story data with required fields and fixed validation issues
    story_data = {
        "id": story_id,
        "version": "1.0.0",
        "headline": "Grant Proposal",
        "headline-id": story_id,
        "headline-event-id": story_id,
        "authors": ["AI Generated"],
        "chapters": [
            {
                "id": str(uuid.uuid4()),
                "block-type": "chapter",
                "sections": []
            }
        ],
        "createdAt": current_time,  # Changed from created-at to createdAt
        "updatedAt": current_time,  # Changed from updated-at to updatedAt
        "storyId": story_id,
        "userPrompt": "Use the provided grantee profile to write a grant volume according to additional instructions.",
        "storyPlanConfig": story_config
    }
    
    try:
        # Make request with detailed error handling
        response = requests.post(url, headers=headers, json=story_data)
        
        print("\nAPI Response Details:")
        print(f"- Status Code: {response.status_code}")
        print(f"- Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
            
        # Print request details for debugging
        print("\nRequest Details:")
        print(f"- URL: {url}")
        print("- Headers:")
        safe_headers = headers.copy()
        safe_headers['Authorization'] = 'Bearer [REDACTED]'
        for key, value in safe_headers.items():
            print(f"  {key}: {value}")
        
        # Check for specific error conditions
        if response.status_code == 401:
            print("\nAuthentication Error Details:")
            print("- Please verify:")
            print("  1. API key is valid and not expired")
            print("  2. API key has correct permissions")
            print("  3. API key is for the correct environment")
            print("\nTroubleshooting steps:")
            print("  1. Check if API key is from the correct Capitol AI environment")
            print("  2. Verify API key has not been revoked")
            print("  3. Ensure API URL matches the key's environment")
            print("  4. Try generating a new API key")
            print(f"\nEndpoint being accessed: {url}")
            try:
                error_details = response.json()
                print(f"Error response: {json.dumps(error_details, indent=2)}")
            except:
                print(f"Raw error response: {response.text}")
            
        # Try to parse response body
        try:
            response_data = response.json()
            print(f"\nResponse Body: {json.dumps(response_data, indent=2)}")
            return response_data
        except json.JSONDecodeError as e:
            print(f"\nInvalid JSON Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Failed: {str(e)}")
        return None
    
    return None

def main():
    # Generate abstract story
    story1 = generate_story(abstract_report_config)
    if story1 and story1.get('created', {}).get('id'):
        print(f"Abstract Story ID: {story1['created']['id']}")
    
    # Generate technical story
    story2 = generate_story(technical_report_config)
    if story2 and story2.get('created', {}).get('id'):
        print(f"Technical Story ID: {story2['created']['id']}")

# Test cases
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('API_URL', 'https://api.example.com')
    monkeypatch.setenv('VITE_CAPITOL_API_KEY', 'test-api-key')
    monkeypatch.setenv('VITE_CAPITOL_API_URL', 'https://capitol.example.com')

def test_get_env_config(mock_env_vars):
    config = get_env_config()
    assert config['api_url'] == 'https://api.example.com'
    assert config['capitol_api_key'] == 'test-api-key'
    assert config['capitol_api_url'] == 'https://capitol.example.com'

@pytest.mark.parametrize("config_type,expected_length", [
    (technical_report_config, ""),
    (abstract_report_config, "1 page")
])
def test_report_configs(config_type, expected_length):
    assert config_type["format"] == "custom"
    assert config_type["responseLength"] == expected_length
    assert config_type["responseLanguage"] == "english"
    assert isinstance(config_type["customInstructions"], str)

@patch('requests.post')
def test_generate_story_success(mock_post):
    # Mock successful API response
    mock_response = Mock()
    mock_response.headers = {'content-type': 'application/json'}
    mock_response.json.return_value = {
        'created': {'id': 'test-story-id'}
    }
    mock_post.return_value = mock_response

    result = generate_story(abstract_report_config)
    assert result is not None
    assert result['created']['id'] == 'test-story-id'

@patch('requests.post')
def test_generate_story_failure(mock_post):
    # Mock failed API response
    mock_post.side_effect = requests.exceptions.RequestException()
    
    result = generate_story(abstract_report_config)
    assert result is None

@pytest.mark.integration
def test_generate_story_integration():
    """Integration test using real API endpoints"""
    config = get_env_config()
    
    # More detailed environment variable checking
    missing_vars = []
    for var in ['api_url', 'capitol_api_key', 'capitol_api_url']:
        if not config[var]:
            missing_vars.append(var)
    
    if missing_vars:
        pytest.skip(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Print debug info (remove in production)
    print(f"Using API URL: {config['api_url']}")
    print(f"Capitol API URL: {config['capitol_api_url']}")
    print(f"API Key present: {'Yes' if config['capitol_api_key'] else 'No'}")
        
    # Test with abstract report config
    result1 = generate_story(abstract_report_config)
    assert result1 is not None, "API response should not be None"
    print(f"API Response for abstract report: {json.dumps(result1, indent=2)}")
    
    if result1 is None:
        pytest.skip("API returned None response - check previous error logs")
    
    if 'error' in result1:
        error_msg = result1.get('error', {})
        if isinstance(error_msg, dict):
            error_msg = json.dumps(error_msg, indent=2)
        pytest.skip(f"API returned error:\n{error_msg}\n\nCheck API key permissions and configuration")
    
    assert 'created' in result1, f"Expected 'created' in response, got: {result1}"
    assert 'id' in result1['created']
    
    # Test with technical report config
    result2 = generate_story(technical_report_config)
    assert result2 is not None, "API response should not be None"
    print(f"API Response for technical report: {json.dumps(result2, indent=2)}")
    assert 'created' in result2, f"Expected 'created' in response, got: {result2}"
    assert 'id' in result2['created']
    
    # Verify the response structure
    for result in [result1, result2]:
        assert isinstance(result, dict)
        assert isinstance(result['created']['id'], str)
        assert len(result['created']['id']) > 0

if __name__ == "__main__":
    main()
