#!/bin/bash
# 🚀 Start Apollo MCP Server in HTTP Mode
# Usage: ./start-http-server.sh [port]

PORT=${1:-3000}
echo "🚀 Starting Apollo MCP Server in HTTP mode on port $PORT..."

# Set environment variables
export TRANSPORT=http
export PORT=$PORT
export ANTHROPIC_API_KEY="sk-ant-api03-gIX1ykuqmfJQy30-fYJWDr3pWJiGwp2t_xNV1rFRsiBmEF3Uqr5nXgdCH6GqIRJIzCL_mU1dBQBKJyJ3g1T2gw-2dG_nwAA"

echo "📡 Endpoint: http://localhost:$PORT/mcp"
echo "🏥 Health Check: http://localhost:$PORT/health"
echo "⚡ Environment: HTTP Transport"
echo ""

# Start the server
npm start