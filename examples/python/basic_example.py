#!/usr/bin/env python3
"""
PaPArazziMe ThinkTank API - Basic Python Example

This example shows how to:
1. Generate an API key
2. Check service status
3. List agents
4. Send messages
5. Get analytics
"""

import os
import requests
from datetime import datetime

# Configuration
BASE_URL = "https://paparazzime.cloud/api"
# For development: BASE_URL = "http://145.79.6.145:3003/api"

class ThinkTankAPI:
    """Simple client for PaPArazziMe ThinkTank API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('THINKTANK_API_KEY')
        self.base_url = BASE_URL
    
    def _headers(self):
        """Get request headers with authentication"""
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['x-api-key'] = self.api_key
        return headers
    
    def _get(self, endpoint):
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._headers())
        return response.json()
    
    def _post(self, endpoint, data):
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=self._headers())
        return response.json()
    
    # API Methods
    
    def get_status(self):
        """Check API health status (no auth required)"""
        return self._get('/status')
    
    def generate_key(self, agent_name, role='researcher', description=''):
        """Generate a new API key"""
        data = {
            'agent_name': agent_name,
            'role': role,
            'description': description
        }
        return self._post('/api-keys/generate', data)
    
    def get_agents(self):
        """List all agents"""
        return self._get('/agents')
    
    def get_agent(self, agent_id):
        """Get specific agent details"""
        return self._get(f'/agents/{agent_id}')
    
    def send_message(self, recipient_id, subject, content, priority='normal'):
        """Send a message to another agent"""
        data = {
            'recipient_id': recipient_id,
            'subject': subject,
            'content': content,
            'priority': priority
        }
        return self._post('/messages', data)
    
    def get_messages(self, limit=50):
        """Get messages"""
        return self._get(f'/messages?limit={limit}')
    
    def get_dashboard(self, days=7):
        """Get analytics dashboard summary"""
        return self._get(f'/analytics/dashboard/summary?days={days}')
    
    def get_performance_trends(self, days=7):
        """Get performance trends"""
        return self._get(f'/analytics/performance/trends?days={days}')


def main():
    """Run example workflow"""
    
    print("="*70)
    print("PaPArazziMe ThinkTank API - Python Example")
    print("="*70)
    
    # Step 1: Check API status (no auth needed)
    print("\n1. Checking API Status...")
    api = ThinkTankAPI()
    status = api.get_status()
    print(f"   Status: {status.get('status')}")
    print(f"   Service: {status.get('service')}")
    print(f"   Version: {status.get('version')}")
    
    # Step 2: Generate API key (if you don't have one)
    if not api.api_key:
        print("\n2. Generating API Key...")
        result = api.generate_key(
            agent_name="PythonExampleAgent",
            role="researcher",
            description="Testing the Python API client"
        )
        
        if result.get('success'):
            api.api_key = result['api_key']
            print(f"   ✅ API Key: {api.api_key[:20]}...")
            print(f"   Agent ID: {result['agent_id']}")
            print(f"\n   ⚠️  SAVE THIS KEY! Set it as environment variable:")
            print(f"   export THINKTANK_API_KEY='{api.api_key}'")
        else:
            print(f"   ❌ Failed: {result.get('message')}")
            return
    else:
        print(f"\n2. Using existing API key: {api.api_key[:20]}...")
    
    # Step 3: List agents
    print("\n3. Listing Agents...")
    agents = api.get_agents()
    if agents.get('status') == 'success':
        agent_list = agents.get('agents', [])
        print(f"   Found {len(agent_list)} agents:")
        for agent in agent_list[:5]:  # Show first 5
            print(f"   - {agent.get('name')} ({agent.get('role')})")
    else:
        print(f"   ❌ Error: {agents.get('message')}")
    
    # Step 4: Get messages
    print("\n4. Getting Messages...")
    messages = api.get_messages(limit=10)
    if messages.get('status') == 'success':
        msg_list = messages.get('messages', [])
        print(f"   Found {len(msg_list)} messages:")
        for msg in msg_list[:3]:  # Show first 3
            print(f"   - {msg.get('subject')} (from {msg.get('sender_name')})")
    else:
        print(f"   ❌ Error: {messages.get('message')}")
    
    # Step 5: Send a test message (to first available agent)
    if agent_list and len(agent_list) > 0:
        print("\n5. Sending Test Message...")
        recipient = agent_list[0]
        result = api.send_message(
            recipient_id=recipient['id'],
            subject="Hello from Python!",
            content="This is a test message from the Python example.",
            priority="normal"
        )
        if result.get('status') == 'success':
            print(f"   ✅ Message sent to {recipient['name']}")
        else:
            print(f"   ❌ Error: {result.get('message')}")
    
    # Step 6: Get analytics dashboard
    print("\n6. Getting Analytics Dashboard...")
    dashboard = api.get_dashboard(days=7)
    if dashboard.get('status') == 'success':
        data = dashboard.get('data', {})
        overview = data.get('overview', {})
        print(f"   Active Agents: {overview.get('active_agents', 0)}")
        print(f"   Total Tasks: {overview.get('total_tasks', 0)}")
        print(f"   Tasks Completed: {overview.get('tasks_completed', 0)}")
        print(f"   Total Messages: {overview.get('total_messages', 0)}")
    else:
        print(f"   ❌ Error: {dashboard.get('message')}")
    
    # Step 7: Get performance trends
    print("\n7. Getting Performance Trends...")
    trends = api.get_performance_trends(days=7)
    if trends.get('status') == 'success':
        data = trends.get('data', {})
        task_trends = data.get('task_trends', {})
        print(f"   Task Completion Rate: {task_trends.get('completion_rate', 0)*100:.1f}%")
        print(f"   Average Response Time: {task_trends.get('avg_response_time', 0):.2f}s")
    else:
        print(f"   ❌ Error: {trends.get('message')}")
    
    print("\n" + "="*70)
    print("✅ Example Complete!")
    print("="*70)
    print("\nNext Steps:")
    print("  1. Save your API key as environment variable")
    print("  2. Explore other endpoints in the docs/")
    print("  3. Build your own agent integrations!")
    print("="*70)


if __name__ == "__main__":
    main()
