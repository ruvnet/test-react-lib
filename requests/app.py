#!/usr/bin/env python3
import asyncio
import websockets
import requests
import json
import signal
import sys

# Global flag for graceful shutdown
shutdown = False

def signal_handler(signum, frame):
    global shutdown
    print("\nShutdown signal received. Closing connection gracefully...")
    shutdown = True

async def connect_websocket(socket_address):
    headers = {
        "X-Domain": "https://aigrants.co/",
        "X-API-Key": "1tNHcGMBXaUxcicZmNF0aKnyEX/IcRWXr3xS96VMMmI=",
        "X-User-ID": "1",
        "Content-Type": "application/json"
    }

    print(f"Connecting to WebSocket at {socket_address}...")
    async with websockets.connect(socket_address, extra_headers=headers) as websocket:
        print("Connected to WebSocket. Waiting for messages...")
        try:
            while not shutdown:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    print(f"Received: {response}")
                    
                    try:
                        data = json.loads(response)
                        if data.get("type") == "terminate":
                            print("\nStream completed naturally")
                            break
                    except json.JSONDecodeError:
                        continue
                except asyncio.TimeoutError:
                    # Check shutdown flag during timeout
                    continue
                
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

def get_websocket_url():
    url = "https://api.capitol.ai/chat/async"
    headers = {
        "X-Domain": "https://aigrants.co/",
        "X-API-Key": "1tNHcGMBXaUxcicZmNF0aKnyEX/IcRWXr3xS96VMMmI=",
        "X-User-ID": "1",
        "Content-Type": "application/json"
    }

    payload = {
        "story-id": "5d9c6076-f2fd-44a8-9ca1-de4014ff6299",
        "user_config_params": {
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
    }

    print("Getting WebSocket URL from API...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"Success! API request completed with status code: {response.status_code}")
        data = response.json()
        return data.get("socketAddress")
    else:
        print(f"Error! API request failed with status code: {response.status_code}")
        print("Response:", response.text)
        return None

async def main():
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    socket_address = get_websocket_url()
    if socket_address:
        await connect_websocket(socket_address)
    else:
        print("Failed to get WebSocket URL")

if __name__ == "__main__":
    print("Starting API test...")
    asyncio.run(main())
