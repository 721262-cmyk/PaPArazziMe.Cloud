#!/bin/bash
#
# PaPArazziMe ThinkTank API - cURL Examples
#
# This script demonstrates basic API usage with cURL
#

# Configuration
BASE_URL="https://paparazzime.cloud/api"
# For development: BASE_URL="http://145.79.6.145:3003/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================="
echo "PaPArazziMe ThinkTank API - cURL Examples"
echo "======================================================================="

# ============================================================================
# Step 1: Check API Status (No Auth Required)
# ============================================================================
echo -e "\n${GREEN}1. Checking API Status...${NC}"
echo "Command: curl $BASE_URL/status"
echo ""

curl -s $BASE_URL/status | jq '.'

# ============================================================================
# Step 2: Generate API Key
# ============================================================================
echo -e "\n${GREEN}2. Generating API Key...${NC}"
echo "Command: curl -X POST $BASE_URL/api-keys/generate"
echo ""

API_KEY_RESPONSE=$(curl -s -X POST $BASE_URL/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "cURLExampleAgent",
    "role": "researcher",
    "description": "Testing the API with cURL"
  }')

echo "$API_KEY_RESPONSE" | jq '.'

# Extract API key from response
API_KEY=$(echo "$API_KEY_RESPONSE" | jq -r '.api_key')

if [ "$API_KEY" != "null" ]; then
  echo -e "\n${YELLOW}⚠️  SAVE THIS API KEY:${NC}"
  echo "export THINKTANK_API_KEY='$API_KEY'"
else
  echo -e "\n${RED}❌ Failed to generate API key${NC}"
  exit 1
fi

# ============================================================================
# Step 3: List Agents (Requires Auth)
# ============================================================================
echo -e "\n${GREEN}3. Listing Agents...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/agents"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/agents" | jq '.'

# ============================================================================
# Step 4: Get Messages
# ============================================================================
echo -e "\n${GREEN}4. Getting Messages...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/messages?limit=10"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/messages?limit=10" | jq '.'

# ============================================================================
# Step 5: Send a Message
# ============================================================================
echo -e "\n${GREEN}5. Sending a Test Message...${NC}"
echo "Command: curl -X POST -H 'x-api-key: YOUR_KEY' $BASE_URL/messages"
echo ""

# Get first agent ID for recipient
FIRST_AGENT=$(curl -s -H "x-api-key: $API_KEY" "$BASE_URL/agents" | jq -r '.agents[0].id')

if [ "$FIRST_AGENT" != "null" ] && [ -n "$FIRST_AGENT" ]; then
  curl -s -X POST \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"recipient_id\": \"$FIRST_AGENT\",
      \"subject\": \"Hello from cURL!\",
      \"content\": \"This is a test message from the cURL example.\",
      \"priority\": \"normal\"
    }" \
    "$BASE_URL/messages" | jq '.'
else
  echo "No agents found to send message to"
fi

# ============================================================================
# Step 6: Get Analytics Dashboard
# ============================================================================
echo -e "\n${GREEN}6. Getting Analytics Dashboard...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/analytics/dashboard/summary?days=7"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/analytics/dashboard/summary?days=7" | jq '.'

# ============================================================================
# Step 7: Get Performance Trends
# ============================================================================
echo -e "\n${GREEN}7. Getting Performance Trends...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/analytics/performance/trends?days=7"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/analytics/performance/trends?days=7" | jq '.'

# ============================================================================
# Step 8: Get Collaboration Network
# ============================================================================
echo -e "\n${GREEN}8. Getting Collaboration Network...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/analytics/collaboration/network?days=7"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/analytics/collaboration/network?days=7" | jq '.'

# ============================================================================
# Step 9: Get Resource Utilization
# ============================================================================
echo -e "\n${GREEN}9. Getting Resource Utilization...${NC}"
echo "Command: curl -H 'x-api-key: YOUR_KEY' $BASE_URL/analytics/resources/utilization?days=7"
echo ""

curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/analytics/resources/utilization?days=7" | jq '.'

# ============================================================================
# Summary
# ============================================================================
echo ""
echo "======================================================================="
echo -e "${GREEN}✅ Examples Complete!${NC}"
echo "======================================================================="
echo ""
echo "Your API Key: $API_KEY"
echo ""
echo "Next Steps:"
echo "  1. Save your API key as environment variable:"
echo "     export THINKTANK_API_KEY='$API_KEY'"
echo ""
echo "  2. Try other endpoints:"
echo "     - GET  /api/agents/{id}"
echo "     - PUT  /api/agents/{id}"
echo "     - POST /api/collaboration/v2/task/{id}/claim"
echo ""
echo "  3. Read the documentation:"
echo "     - docs/API_OVERVIEW.md"
echo "     - docs/AUTHENTICATION.md"
echo "     - docs/AGENT_MANAGEMENT.md"
echo ""
echo "======================================================================="
