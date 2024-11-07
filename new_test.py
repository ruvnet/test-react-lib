import os
from dotenv import load_dotenv
import json
import requests
import uuid
from datetime import datetime
import time

# Load environment variables from .env file
load_dotenv()

def get_env_config():
    """Get environment configuration"""
    return {
        'capitol_api_key': os.getenv('VITE_CAPITOL_API_KEY'),
        'capitol_api_url': os.getenv('VITE_CAPITOL_API_URL').rstrip('/')  # Remove trailing slash if present
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
    
    headers = {
        'Authorization': f'Bearer {config["capitol_api_key"]}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Print the environment variables for debugging
    print("\nEnvironment Variables:")
    print(f"VITE_CAPITOL_API_URL: {config['capitol_api_url']}")
    print(f"VITE_CAPITOL_API_KEY: {'*' * len(config['capitol_api_key'])}")
    
    # Construct URL properly
    url = f"{config['capitol_api_url']}/generate"
    
    # Story data matching App.jsx structure
    story_data = {
        "storyId": story_id,
        "userPrompt": "Use the provided grantee profile to write a grant volume according to additional instructions.",
        "storyPlanConfig": story_config
    }
    
    print(f"\nMaking request to: {url}")
    print("\nRequest Headers:")
    print(json.dumps({k: v if k != 'Authorization' else '[HIDDEN]' for k, v in headers.items()}, indent=2))
    print("\nRequest Body:")
    print(json.dumps(story_data, indent=2))
    
    try:
        response = requests.post(url, headers=headers, json=story_data)
        print("\nAPI Response:")
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        print(json.dumps(dict(response.headers), indent=2))
        print("Response Body:")
        print(response.text)
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nError making API request: {e}")
    except json.JSONDecodeError as e:
        print(f"\nError decoding JSON response: {e}")
    return None

def main():
    # Generate abstract story
    print("\nGenerating Abstract Story...")
    story1 = generate_story(abstract_report_config)
    if story1 and story1.get('created', {}).get('id'):
        print(f"Abstract Story ID: {story1['created']['id']}")
    
    # Wait between requests to avoid rate limiting
    time.sleep(2)
    
    # Generate technical story
    print("\nGenerating Technical Story...")
    story2 = generate_story(technical_report_config)
    if story2 and story2.get('created', {}).get('id'):
        print(f"Technical Story ID: {story2['created']['id']}")

if __name__ == "__main__":
    main()
