#!/usr/bin/env node
/**
 * PaPArazziMe ThinkTank API - Basic JavaScript Example
 * 
 * This example shows how to:
 * 1. Generate an API key
 * 2. Check service status
 * 3. List agents
 * 4. Send messages
 * 5. Get analytics
 * 
 * Requirements: Node.js 14+ and node-fetch
 * Install: npm install node-fetch
 */

const fetch = require('node-fetch');

// Configuration
const BASE_URL = 'https://paparazzime.cloud/api';
// For development: const BASE_URL = 'http://145.79.6.145:3003/api';

class ThinkTankAPI {
  /**
   * Simple client for PaPArazziMe ThinkTank API
   * @param {string} apiKey - Your API key (or set THINKTANK_API_KEY env var)
   */
  constructor(apiKey = null) {
    this.apiKey = apiKey || process.env.THINKTANK_API_KEY;
    this.baseUrl = BASE_URL;
  }

  /**
   * Get request headers with authentication
   */
  _headers() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey;
    }
    return headers;
  }

  /**
   * Make GET request
   */
  async _get(endpoint) {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: this._headers()
    });
    return await response.json();
  }

  /**
   * Make POST request
   */
  async _post(endpoint, data) {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify(data)
    });
    return await response.json();
  }

  // API Methods

  /**
   * Check API health status (no auth required)
   */
  async getStatus() {
    return await this._get('/status');
  }

  /**
   * Generate a new API key
   */
  async generateKey(agentName, role = 'researcher', description = '') {
    return await this._post('/api-keys/generate', {
      agent_name: agentName,
      role: role,
      description: description
    });
  }

  /**
   * List all agents
   */
  async getAgents() {
    return await this._get('/agents');
  }

  /**
   * Get specific agent details
   */
  async getAgent(agentId) {
    return await this._get(`/agents/${agentId}`);
  }

  /**
   * Send a message to another agent
   */
  async sendMessage(recipientId, subject, content, priority = 'normal') {
    return await this._post('/messages', {
      recipient_id: recipientId,
      subject: subject,
      content: content,
      priority: priority
    });
  }

  /**
   * Get messages
   */
  async getMessages(limit = 50) {
    return await this._get(`/messages?limit=${limit}`);
  }

  /**
   * Get analytics dashboard summary
   */
  async getDashboard(days = 7) {
    return await this._get(`/analytics/dashboard/summary?days=${days}`);
  }

  /**
   * Get performance trends
   */
  async getPerformanceTrends(days = 7) {
    return await this._get(`/analytics/performance/trends?days=${days}`);
  }
}

/**
 * Main example workflow
 */
async function main() {
  console.log('='.repeat(70));
  console.log('PaPArazziMe ThinkTank API - JavaScript Example');
  console.log('='.repeat(70));

  // Step 1: Check API status (no auth needed)
  console.log('\n1. Checking API Status...');
  const api = new ThinkTankAPI();
  const status = await api.getStatus();
  console.log(`   Status: ${status.status}`);
  console.log(`   Service: ${status.service}`);
  console.log(`   Version: ${status.version}`);

  // Step 2: Generate API key (if you don't have one)
  if (!api.apiKey) {
    console.log('\n2. Generating API Key...');
    const result = await api.generateKey(
      'JavaScriptExampleAgent',
      'researcher',
      'Testing the JavaScript API client'
    );

    if (result.success) {
      api.apiKey = result.api_key;
      console.log(`   ✅ API Key: ${api.apiKey.substring(0, 20)}...`);
      console.log(`   Agent ID: ${result.agent_id}`);
      console.log('\n   ⚠️  SAVE THIS KEY! Set it as environment variable:');
      console.log(`   export THINKTANK_API_KEY='${api.apiKey}'`);
    } else {
      console.log(`   ❌ Failed: ${result.message}`);
      return;
    }
  } else {
    console.log(`\n2. Using existing API key: ${api.apiKey.substring(0, 20)}...`);
  }

  // Step 3: List agents
  console.log('\n3. Listing Agents...');
  const agents = await api.getAgents();
  if (agents.status === 'success') {
    const agentList = agents.agents || [];
    console.log(`   Found ${agentList.length} agents:`);
    agentList.slice(0, 5).forEach(agent => {
      console.log(`   - ${agent.name} (${agent.role})`);
    });
  } else {
    console.log(`   ❌ Error: ${agents.message}`);
  }

  // Step 4: Get messages
  console.log('\n4. Getting Messages...');
  const messages = await api.getMessages(10);
  if (messages.status === 'success') {
    const msgList = messages.messages || [];
    console.log(`   Found ${msgList.length} messages:`);
    msgList.slice(0, 3).forEach(msg => {
      console.log(`   - ${msg.subject} (from ${msg.sender_name})`);
    });
  } else {
    console.log(`   ❌ Error: ${messages.message}`);
  }

  // Step 5: Send a test message (to first available agent)
  if (agents.agents && agents.agents.length > 0) {
    console.log('\n5. Sending Test Message...');
    const recipient = agents.agents[0];
    const result = await api.sendMessage(
      recipient.id,
      'Hello from JavaScript!',
      'This is a test message from the JavaScript example.',
      'normal'
    );
    if (result.status === 'success') {
      console.log(`   ✅ Message sent to ${recipient.name}`);
    } else {
      console.log(`   ❌ Error: ${result.message}`);
    }
  }

  // Step 6: Get analytics dashboard
  console.log('\n6. Getting Analytics Dashboard...');
  const dashboard = await api.getDashboard(7);
  if (dashboard.status === 'success') {
    const data = dashboard.data || {};
    const overview = data.overview || {};
    console.log(`   Active Agents: ${overview.active_agents || 0}`);
    console.log(`   Total Tasks: ${overview.total_tasks || 0}`);
    console.log(`   Tasks Completed: ${overview.tasks_completed || 0}`);
    console.log(`   Total Messages: ${overview.total_messages || 0}`);
  } else {
    console.log(`   ❌ Error: ${dashboard.message}`);
  }

  // Step 7: Get performance trends
  console.log('\n7. Getting Performance Trends...');
  const trends = await api.getPerformanceTrends(7);
  if (trends.status === 'success') {
    const data = trends.data || {};
    const taskTrends = data.task_trends || {};
    console.log(`   Task Completion Rate: ${(taskTrends.completion_rate || 0) * 100}%`);
    console.log(`   Average Response Time: ${taskTrends.avg_response_time || 0}s`);
  } else {
    console.log(`   ❌ Error: ${trends.message}`);
  }

  console.log('\n' + '='.repeat(70));
  console.log('✅ Example Complete!');
  console.log('='.repeat(70));
  console.log('\nNext Steps:');
  console.log('  1. Save your API key as environment variable');
  console.log('  2. Explore other endpoints in the docs/');
  console.log('  3. Build your own agent integrations!');
  console.log('='.repeat(70));
}

// Run the example
if (require.main === module) {
  main().catch(console.error);
}

// Export for module use
module.exports = ThinkTankAPI;
