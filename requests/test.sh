#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing Capitol AI API...${NC}"

# API configuration
API_ENDPOINT="https://api.capitol.ai/chat/async"
DOMAIN="https://aigrants.co/"
API_KEY="1tNHcGMBXaUxcicZmNF0aKnyEX/IcRWXr3xS96VMMmI="

# Request payload
PAYLOAD='{
    "story-id": "5d9c6076-f2fd-44a8-9ca1-de4014ff6299",
    "user_config_params": {
        "format": "custom",
        "cot": true,
        "audience": "General",
        "responseLength": "",
        "responseLanguage": "english",
        "heroImage": false,
        "title": false,
        "headers": true,
        "paragraphs": true,
        "images": false,
        "aiImages": false,
        "imageStyle": "auto",
        "aiGraphs": false,
        "webGraphs": false,
        "metrics": false,
        "tables": false,
        "quotes": false,
        "tweets": false,
        "tweetCharacterLimit": 280,
        "generalWebSearch": false,
        "academicWebSearch": false,
        "usePerplexity": false,
        "ragBudget": "default",
        "userQuery": "Use the provided grantee profile to write a grant volume according to additional instructions.",
        "customInstructions": "Please create a Technical Proposal demonstrating your capability to implement the grant project.",
        "imageHeight": 768,
        "imageWidth": 1344,
        "responseModel": "claude-3-5-sonnet-20240620",
        "userUrls": [
            "https://gist.github.com/zstone-cai/323e78d0b0e0f9f312105d2c1595bcbd"
        ],
        "userPdfDocuments": [],
        "userPdfUrls": [],
        "userImages": []
    }
}'

echo -e "${BLUE}Request Details:${NC}"
echo -e "Endpoint: ${GREEN}$API_ENDPOINT${NC}"
echo -e "Headers:"
echo -e "  X-Domain: ${GREEN}$DOMAIN${NC}"
echo -e "  X-API-Key: ${GREEN}[HIDDEN]${NC}"
echo -e "  X-User-ID: ${GREEN}1${NC}"
echo -e "\nPayload:"
echo "$PAYLOAD" | jq '.'

echo -e "\n${BLUE}Sending request...${NC}"

# Make the API request and capture both response and status code
RESPONSE_FILE=$(mktemp)
HTTP_CODE=$(curl --location "$API_ENDPOINT" \
  --header "X-Domain: $DOMAIN" \
  --header "X-API-Key: $API_KEY" \
  --header "X-User-ID: 1" \
  --header "Content-Type: application/json" \
  --write-out "%{http_code}" \
  --silent \
  --output "$RESPONSE_FILE" \
  --data "$PAYLOAD")

echo -e "\n${BLUE}Response Details:${NC}"
echo -e "Status Code: ${GREEN}$HTTP_CODE${NC}"
echo -e "\nResponse Body:"
if [ -f "$RESPONSE_FILE" ]; then
    if jq -e . >/dev/null 2>&1 <<<"$(cat $RESPONSE_FILE)"; then
        # Pretty print JSON response
        cat "$RESPONSE_FILE" | jq '.'
    else
        # Print raw response if not JSON
        cat "$RESPONSE_FILE"
    fi
    rm "$RESPONSE_FILE"
fi

# Check HTTP status code
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
    echo -e "\n${GREEN}Success!${NC} API request completed with status code: $HTTP_CODE"
else
    echo -e "\n${RED}Error!${NC} API request failed with status code: $HTTP_CODE"
fi
