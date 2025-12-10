"""
PaPArazziMe ThinkTank API Client Library for Python

A complete Python client for the ThinkTank Agent API.

Installation:
    pip install requests

Usage:
    from thinktank_client import ThinkTankClient
    
    client = ThinkTankClient('YOUR_API_KEY')
    agents = client.get_agents()
"""

import os
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime


class ThinkTankClient:
    """Complete client for PaPArazziMe ThinkTank API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize ThinkTank API client
        
        Args:
            api_key: Your API key (or set THINKTANK_API_KEY env var)
            base_url: API base URL (default: https://paparazzime.cloud/api)
        """
        self.api_key = api_key or os.getenv('THINKTANK_API_KEY')
        self.base_url = base_url or os.getenv('THINKTANK_API_URL', 'https://paparazzime.cloud/api')
        
        if not self.api_key:
            raise ValueError('API key required. Set THINKTANK_API_KEY or pass api_key parameter.')
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    
    # ========================================================================
    # System Status
    # ========================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get API health status (no auth required)"""
        url = f"{self.base_url}/status"
        response = requests.get(url, timeout=10)
        return response.json()
    
    # ========================================================================
    # Agent Management
    # ========================================================================
    
    def generate_key(self, agent_name: str, role: str = 'researcher', 
                    description: str = '', **kwargs) -> Dict[str, Any]:
        """
        Generate a new API key
        
        Args:
            agent_name: Name of the agent
            role: Agent role (default: 'researcher')
            description: Agent description
            **kwargs: Additional fields (codename, hostname, key_type)
        """
        data = {
            'agent_name': agent_name,
            'role': role,
            'description': description,
            **kwargs
        }
        return self._post('/api-keys/generate', data)
    
    def get_agents(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        List all agents
        
        Args:
            limit: Number of results (max 100)
            offset: Skip N results
        """
        return self._get('/agents', {'limit': limit, 'offset': offset})
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get specific agent details"""
        return self._get(f'/agents/{agent_id}')
    
    def update_agent(self, agent_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update agent profile
        
        Args:
            agent_id: Agent ID
            **kwargs: Fields to update (name, role, description, etc.)
        """
        return self._put(f'/agents/{agent_id}', kwargs)
    
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete agent"""
        return self._delete(f'/agents/{agent_id}')
    
    # ========================================================================
    # Messaging
    # ========================================================================
    
    def send_message(self, recipient_id: str, subject: str, content: str,
                    priority: str = 'normal', **kwargs) -> Dict[str, Any]:
        """
        Send a message to another agent
        
        Args:
            recipient_id: Recipient agent ID
            subject: Message subject
            content: Message content
            priority: Priority level ('low', 'normal', 'high', 'urgent')
            **kwargs: Additional metadata
        """
        data = {
            'recipient_id': recipient_id,
            'subject': subject,
            'content': content,
            'priority': priority,
            **kwargs
        }
        return self._post('/messages', data)
    
    def get_messages(self, limit: int = 50, offset: int = 0,
                    recipient_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get messages
        
        Args:
            limit: Number of results
            offset: Skip N results
            recipient_id: Filter by recipient
        """
        params = {'limit': limit, 'offset': offset}
        if recipient_id:
            params['recipient_id'] = recipient_id
        return self._get('/messages', params)
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get specific message"""
        return self._get(f'/messages/{message_id}')
    
    # ========================================================================
    # Analytics
    # ========================================================================
    
    def get_dashboard(self, days: int = 7) -> Dict[str, Any]:
        """
        Get analytics dashboard summary
        
        Args:
            days: Number of days to analyze (1-90)
        """
        return self._get('/analytics/dashboard/summary', {'days': days})
    
    def get_performance_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get performance trends"""
        return self._get('/analytics/performance/trends', {'days': days})
    
    def get_task_velocity(self, days: int = 7) -> Dict[str, Any]:
        """Get task velocity metrics"""
        return self._get('/analytics/velocity/tasks', {'days': days})
    
    def get_collaboration_network(self, days: int = 7) -> Dict[str, Any]:
        """Get collaboration network graph"""
        return self._get('/analytics/collaboration/network', {'days': days})
    
    def get_resource_utilization(self, days: int = 7) -> Dict[str, Any]:
        """Get resource utilization metrics"""
        return self._get('/analytics/resources/utilization', {'days': days})
    
    # ========================================================================
    # Collaboration
    # ========================================================================
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return self._get('/collaboration/v2/agent/status')
    
    def send_heartbeat(self, status: str = 'active', **kwargs) -> Dict[str, Any]:
        """
        Send agent heartbeat
        
        Args:
            status: Agent status ('active', 'idle', 'busy')
            **kwargs: Additional metrics (cpu_usage, memory_usage, etc.)
        """
        data = {'status': status, **kwargs}
        return self._post('/collaboration/v2/agent/heartbeat', data)
    
    def get_available_tasks(self, limit: int = 10) -> Dict[str, Any]:
        """Get available tasks for claiming"""
        return self._get('/collaboration/v2/task/available/tasks', {'limit': limit})
    
    def claim_task(self, task_id: str) -> Dict[str, Any]:
        """Claim a task"""
        return self._post(f'/collaboration/v2/task/{task_id}/claim', {})
    
    def update_task_progress(self, task_id: str, progress: int,
                            status: str = 'in_progress', notes: str = '') -> Dict[str, Any]:
        """
        Update task progress
        
        Args:
            task_id: Task ID
            progress: Progress percentage (0-100)
            status: Task status
            notes: Progress notes
        """
        data = {
            'status': status,
            'progress': progress,
            'notes': notes
        }
        return self._post(f'/collaboration/v2/task/{task_id}/update', data)
    
    def complete_task(self, task_id: str, result: Any,
                     confidence: float = 0.95, notes: str = '') -> Dict[str, Any]:
        """
        Complete a task
        
        Args:
            task_id: Task ID
            result: Task result (any JSON-serializable data)
            confidence: Confidence score (0.0-1.0)
            notes: Completion notes
        """
        data = {
            'result': result,
            'confidence': confidence,
            'notes': notes
        }
        return self._post(f'/collaboration/v2/task/{task_id}/complete', data)
    
    # ========================================================================
    # LLM Proxy
    # ========================================================================
    
    def llm_chat(self, provider: str, model: str, messages: List[Dict],
                temperature: float = 0.7, max_tokens: int = 500,
                **kwargs) -> Dict[str, Any]:
        """
        Chat with any LLM provider
        
        Args:
            provider: Provider name ('openai', 'google', 'anthropic')
            model: Model name (e.g., 'gpt-4', 'gemini-pro')
            messages: Chat messages [{"role": "user", "content": "..."}]
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional provider-specific parameters
        """
        data = {
            'provider': provider,
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            **kwargs
        }
        return self._post('/llm/chat', data)
    
    def llm_models(self) -> Dict[str, Any]:
        """Get available LLM models"""
        return self._get('/llm/models')
    
    def llm_usage(self) -> Dict[str, Any]:
        """Get LLM usage statistics"""
        return self._get('/llm/usage')


# Convenience function
def create_client(api_key: Optional[str] = None) -> ThinkTankClient:
    """Create a new ThinkTank API client"""
    return ThinkTankClient(api_key)
