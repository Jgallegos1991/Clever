#!/bin/bash
# Clever Endpoint Smoke Tests
# Usage: bash docs/test_endpoints.sh

BASE_URL="http://127.0.0.1:5000"
echo "🧪 Starting Clever endpoint smoke tests..."
echo "🔗 Target: $BASE_URL"

# Check if server is running
echo "0. Checking if Clever is running..."
if ! curl -f -s "$BASE_URL/health" > /dev/null 2>&1; then
    echo "❌ Clever is not running on port 5000"
    echo "💡 Start with: python3 app.py"
    exit 1
fi
echo "✅ Clever is running"

# Test 1: Health check
echo
echo "1. Testing health endpoint..."
HEALTH_RESPONSE=$(curl -f -s "$BASE_URL/health")
if echo "$HEALTH_RESPONSE" | grep -q '"status": "ok"'; then
    echo "✅ Health check passed"
    echo "$HEALTH_RESPONSE" | jq . 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
    echo "Response: $HEALTH_RESPONSE"
fi

# Test 2: Capabilities
echo
echo "2. Testing capabilities endpoint..."
CAPABILITIES_RESPONSE=$(curl -f -s "$BASE_URL/capabilities")
if echo "$CAPABILITIES_RESPONSE" | grep -q '"name": "Clever"'; then
    echo "✅ Capabilities endpoint passed"
    echo "$CAPABILITIES_RESPONSE" | jq .name 2>/dev/null || echo "Name: Clever"
else
    echo "❌ Capabilities endpoint failed"
    echo "Response: $CAPABILITIES_RESPONSE"
fi

# Test 3: Main page
echo
echo "3. Testing main page..."
MAIN_RESPONSE=$(curl -f -s "$BASE_URL/")
if echo "$MAIN_RESPONSE" | grep -q -i "synaptic\|clever"; then
    echo "✅ Main page loads successfully"
    echo "Page contains expected content"
else
    echo "❌ Main page failed"
    echo "Response length: ${#MAIN_RESPONSE} characters"
fi

# Test 4: Chat endpoint (POST)
echo
echo "4. Testing chat endpoint..."
CHAT_RESPONSE=$(curl -f -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Clever, this is a test"}')
if echo "$CHAT_RESPONSE" | grep -q '"reply":'; then
    echo "✅ Chat endpoint passed"
    echo "$CHAT_RESPONSE" | jq '.reply' 2>/dev/null || echo "Got response from Clever"
else
    echo "❌ Chat endpoint failed"
    echo "Response: $CHAT_RESPONSE"
fi

# Test 5: Static files
echo
echo "5. Testing static file serving..."
if curl -f -s "$BASE_URL/favicon.ico" > /dev/null 2>&1; then
    echo "✅ Static files accessible"
else
    echo "❌ Static files failed"
fi

# Test 6: Service worker
echo
echo "6. Testing service worker..."
if curl -f -s "$BASE_URL/sw.js" > /dev/null 2>&1; then
    echo "✅ Service worker accessible"
else
    echo "❌ Service worker failed"
fi

echo
echo "🏁 Smoke tests completed"
echo "💡 For detailed testing, open browser to: $BASE_URL"