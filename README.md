# Anthropic MCP Server for X (Twitter)

This MCP server integrates Claude (Anthropic), Google Sheets, and X (Twitter) to automate tweet posting. It uses Claude to improve tweets, schedules them through Google Sheets, and posts them to X without using API.

## Features

- Reads tweets from Google Sheets
- Uses Claude to review and improve tweets
- Posts tweets to X without API
- Supports scheduled tweets
- Updates tweet status in Google Sheet
- Handles rate limiting and errors

## Prerequisites

- Python 3.8+
- Google Chrome browser
- Google Cloud account
- Claude Desktop access
- X (Twitter) account

## Installation

1. Clone the repository:
2. Install dependencies: pip install -r requirements.txt

3. Set up Google Sheets:
   - Create a new Google Sheet with these columns:
     - A: Tweet Content
     - B: Scheduled Time (YYYY-MM-DD HH:MM:SS)
     - C: Status (PENDING/POSTED/FAILED)
     - D: Posted Time
     - E: Tweet URL
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Google Sheets API
   - Create Service Account credentials
   - Download credentials as `credentials.json`
   - Share your Google Sheet with the service account email

4. Configure environment:
   Create `.env` file: