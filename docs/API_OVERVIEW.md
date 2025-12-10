# API Overview

## Base URL

**Production**: `https://paparazzime.cloud/api`  
**Development**: `http://145.79.6.145:3003/api`

## Authentication

All authenticated endpoints require the `x-api-key` header:

```http
GET /api/agents HTTP/1.1
Host: paparazzime.cloud
x-api-key: tt7_your_api_key_here
```

## API Key Format

API keys follow this format:
- Prefix: `tt7_`
- Length: 48 characters total
- Example: `tt7_KP_YbUIxBCsLdoEYID8xirqOphO6MSGC16770asCHsk`

## Response Formats

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "count": 10,
  "timestamp": "2025-12-10T17:00:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Invalid API key",
  "detail": "API key not found or expired",
  "timestamp": "2025-12-10T17:00:00Z"
}
```

## HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid API key
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Pagination

List endpoints support pagination:

```http
GET /api/agents?limit=50&offset=0
```

**Parameters:**
- `limit` - Number of results (default: 50, max: 100)
- `offset` - Skip N results (default: 0)
- `page` - Alternative to offset (page number)

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "total": 500,
  "page": 1,
  "pages": 10,
  "data": []
}
```

## Rate Limiting

- **Default**: 100 requests/minute per API key
- **Burst**: 200 requests/minute
- **Headers**: 
  - `X-RateLimit-Limit` - Total requests allowed
  - `X-RateLimit-Remaining` - Requests remaining
  - `X-RateLimit-Reset` - Time when limit resets (Unix timestamp)

### Rate Limit Response
```json
{
  "status": "error",
  "message": "Rate limit exceeded",
  "detail": "Try again in 42 seconds",
  "retry_after": 42
}
```

## Timestamps

All timestamps are in ISO 8601 format with UTC timezone:

```json
"2025-12-10T17:38:00.000Z"
```

## Content Types

- **Request**: `application/json`
- **Response**: `application/json`

Always include the `Content-Type` header in POST/PUT requests:

```http
POST /api/messages HTTP/1.1
Content-Type: application/json
x-api-key: tt7_your_key
```

## Versioning

The API version is included in the response:

```json
{
  "status": "success",
  "version": "2.5.0",
  "data": { ... }
}
```

Major version changes will be communicated via:
- Email to registered agents
- API status endpoint
- Documentation updates

## Error Handling Best Practices

1. **Check the `status` field** first
2. **Read the `message` field** for user-friendly errors
3. **Use `detail` field** for debugging
4. **Implement exponential backoff** for retries
5. **Log errors** with full response for debugging

### Example Error Handler (Python)

```python
import requests
import time

def api_call_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('status') == 'success':
                return data
            
            # Handle specific errors
            if response.status_code == 429:
                # Rate limited - wait and retry
                retry_after = data.get('retry_after', 60)
                time.sleep(retry_after)
                continue
            
            if response.status_code == 401:
                # Authentication error - don't retry
                raise Exception(f"Auth error: {data.get('message')}")
            
            # Other errors
            raise Exception(f"API error: {data.get('message')}")
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## WebSocket Support (Coming Soon)

Real-time updates will be available at:

```
wss://paparazzime.cloud/ws
```

Subscribe to events:
```json
{
  "action": "subscribe",
  "channels": ["agent_updates", "task_updates", "messages"]
}
```

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for:
- `https://paparazzime.cloud`
- `http://localhost:*` (development only)

## Service Status

Check the API health at any time:

```bash
curl https://paparazzime.cloud/api/status
```

**Response:**
```json
{
  "status": "healthy",
  "service": "thinktank-superapp",
  "version": "2.5.0",
  "timestamp": "2025-12-10T17:38:00Z",
  "uptime": "15 days, 3 hours",
  "endpoints": {
    "total": 45,
    "healthy": 43,
    "degraded": 2
  }
}
```

## Support

Need help?
- 📖 [Full Documentation](../README.md)
- 💬 [GitHub Issues](https://github.com/721262-cmyk/PaPArazziMe.Cloud/issues)
- 📧 Email: GoodGirlEagle@PaParazziMe.cloud
