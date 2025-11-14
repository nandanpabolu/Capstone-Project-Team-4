# Patent Partners Assistant - API Documentation

**Version**: 0.1.0  
**Base URL**: `http://localhost:8000`  
**Protocol**: HTTP/1.1  
**Content-Type**: `application/json`

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Generate Invention Memo](#generate-invention-memo)
  - [Generate Patent Draft](#generate-patent-draft)
  - [Export to DOCX](#export-to-docx)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Overview

The Patent Partners Assistant API provides RESTful endpoints for AI-powered patent document generation and export. All processing is performed locally using the Ollama + Mistral-7B model, ensuring complete privacy and offline operation.

### Key Features

- ✅ Type-safe request/response validation using Pydantic
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling
- ✅ Request/response logging
- ✅ Offline operation (no external API calls)

### Interactive Documentation

Once the API server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Authentication

Currently, the API **does not require authentication** for local development and deployment. All endpoints are publicly accessible on localhost.

For production deployments, consider adding:
- API key authentication
- JWT tokens
- IP whitelisting
- HTTPS/TLS

---

## Endpoints

### Health Check

**GET** `/health`

Check the API server status and Ollama availability.

#### Request

```bash
curl -X GET http://localhost:8000/health
```

#### Response

**Status**: `200 OK`

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "offline_mode": true,
  "ollama_available": true,
  "timestamp": "2024-11-14T10:30:00.123456Z"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Server health status: "healthy" or "unhealthy" |
| `version` | string | API version number |
| `offline_mode` | boolean | Whether offline mode is enabled |
| `ollama_available` | boolean | Whether Ollama service is accessible |
| `timestamp` | string | ISO 8601 timestamp of the response |

#### Example Responses

**Success (Ollama Available)**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "offline_mode": true,
  "ollama_available": true,
  "timestamp": "2024-11-14T10:30:00.123456Z"
}
```

**Ollama Unavailable**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "offline_mode": true,
  "ollama_available": false,
  "timestamp": "2024-11-14T10:30:00.123456Z"
}
```

---

### Generate Invention Memo

**POST** `/generate/memo`

Generate a comprehensive invention disclosure memo with technical analysis and patentability assessment.

#### Request

```bash
curl -X POST http://localhost:8000/generate/memo \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "A smart delivery drone system...",
    "context_chunks": null,
    "include_citations": true,
    "max_tokens": 2000,
    "temperature": 0.7
  }'
```

#### Request Body

```json
{
  "invention_description": "string",
  "context_chunks": null,
  "include_citations": true,
  "max_tokens": 2000,
  "temperature": 0.7
}
```

#### Request Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `invention_description` | string | ✅ Yes | - | Description of the invention (50-10,000 chars) |
| `context_chunks` | array\|null | No | `null` | Prior art context (not yet implemented) |
| `include_citations` | boolean | No | `true` | Whether to include citations |
| `max_tokens` | integer | No | `2048` | Maximum output tokens (100-8000) |
| `temperature` | float | No | `0.7` | Creativity level (0.0-1.0) |

#### Response

**Status**: `200 OK`

```json
{
  "draft": "# INVENTION DISCLOSURE MEMO\n\n## Executive Summary...",
  "generation_time_ms": 87340.5,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": [
    "Executive Summary",
    "Invention Overview",
    "Technical Analysis",
    "Prior Art",
    "Patentability"
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `draft` | string | Generated memo text (markdown formatted) |
| `generation_time_ms` | float | Generation time in milliseconds |
| `model_used` | string | LLM model identifier |
| `citations` | array | List of citation objects (empty if no prior art) |
| `sections` | array | List of section titles in the memo |

#### Generation Modes

The system uses different prompt templates based on `max_tokens`:

**Fast & Concise Mode** (< 2000 tokens):
- Generation time: 60-90 seconds
- Output length: ~1500 tokens
- Focused, essential sections only

**Detailed & Comprehensive Mode** (≥ 2000 tokens):
- Generation time: 120-180 seconds
- Output length: ~3500 tokens
- Comprehensive analysis with recommendations

#### Example

**Request**:
```json
{
  "invention_description": "A smart delivery drone system that uses advanced computer vision and machine learning to navigate obstacles in urban environments. The drone can autonomously detect and avoid birds, buildings, power lines, and other aircraft. It uses a combination of LIDAR, cameras, and GPS for navigation. The system includes a package delivery mechanism with secure locking and real-time tracking capabilities.",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "draft": "# INVENTION DISCLOSURE MEMO\n\n## Executive Summary\n\nThe disclosed invention relates to an autonomous delivery drone system...",
  "generation_time_ms": 87340.5,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": [
    "Executive Summary",
    "Technical Field",
    "Invention Overview",
    "Prior Art Analysis",
    "Novelty Assessment",
    "Patentability Evaluation"
  ]
}
```

---

### Generate Patent Draft

**POST** `/generate/draft`

Generate a USPTO-compliant patent application draft including title, abstract, background, summary, detailed description, and claims.

#### Request

```bash
curl -X POST http://localhost:8000/generate/draft \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "A smart delivery drone system...",
    "max_tokens": 3000,
    "temperature": 0.7
  }'
```

#### Request Body

```json
{
  "invention_description": "string",
  "context_chunks": null,
  "include_citations": true,
  "max_tokens": 3000,
  "temperature": 0.7
}
```

#### Request Fields

Same as [Generate Invention Memo](#request-fields), but recommended `max_tokens` is higher (3000-4500) for comprehensive patent drafts.

#### Response

**Status**: `200 OK`

```json
{
  "draft": "TITLE OF INVENTION\n\nSmart Delivery Drone with Autonomous Navigation...",
  "generation_time_ms": 92180.3,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": [
    "Title",
    "Abstract",
    "Technical Field",
    "Background",
    "Summary",
    "Detailed Description",
    "Claims"
  ]
}
```

#### Response Fields

Same as [Generate Invention Memo Response](#response-fields-1).

#### USPTO Sections Generated

1. **Title**: Concise invention title
2. **Abstract**: 150-word technical summary
3. **Technical Field**: Area of technology
4. **Background of Invention**: Prior art and problems
5. **Summary of Invention**: Solution overview
6. **Detailed Description**: Comprehensive technical details
7. **Claims**: 
   - Independent claims (broad protection)
   - Dependent claims (specific embodiments)

#### Example

**Request**:
```json
{
  "invention_description": "A smart delivery drone system with autonomous navigation using computer vision and machine learning...",
  "max_tokens": 3000,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "draft": "TITLE OF INVENTION\n\nAutonomous Delivery Drone System with Intelligent Obstacle Avoidance\n\nABSTRACT\n\nAn autonomous delivery drone system comprises...",
  "generation_time_ms": 92180.3,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": [
    "Title",
    "Abstract",
    "Technical Field",
    "Background of Invention",
    "Summary of Invention",
    "Detailed Description",
    "Claims"
  ]
}
```

---

### Export to DOCX

**POST** `/export/docx`

Export generated content to Microsoft Word (DOCX) format with professional legal formatting.

#### Request

```bash
curl -X POST http://localhost:8000/export/docx \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Patent Draft\n\nContent here...",
    "filename": "patent_draft.docx",
    "document_type": "draft"
  }'
```

#### Request Body

```json
{
  "content": "string",
  "filename": "patent_draft.docx",
  "document_type": "draft"
}
```

#### Request Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `content` | string | ✅ Yes | - | Content to export (markdown or plain text) |
| `filename` | string | No | Auto-generated | Desired filename |
| `document_type` | string | No | `"draft"` | Document type: "draft" or "memo" |

#### Response

**Status**: `200 OK`

```json
{
  "filename": "patent_draft.docx",
  "file_path": "/data/exports/patent_draft.docx",
  "file_size": 25600
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `filename` | string | Generated filename |
| `file_path` | string | Full path to saved file |
| `file_size` | integer | File size in bytes |

#### Document Formatting

The exported DOCX includes:
- **Heading 1**: Main titles
- **Heading 2**: Section headers
- **Heading 3**: Subsections
- **Body Text**: Normal paragraphs
- **Lists**: Bullet and numbered lists
- **Page Breaks**: Between major sections
- **Metadata**: Creation date, author info

#### Example

**Request**:
```json
{
  "content": "# Patent Draft\n\n## Title\n\nSmart Delivery Drone\n\n## Abstract\n\nAn invention for...",
  "filename": "drone_patent.docx",
  "document_type": "draft"
}
```

**Response**:
```json
{
  "filename": "drone_patent.docx",
  "file_path": "/Users/user/Project/data/exports/drone_patent.docx",
  "file_size": 28672
}
```

---

## Data Models

### GenerateRequest

```typescript
{
  invention_description: string (50-10000 chars),
  context_chunks?: Passage[] | null,
  include_citations?: boolean = true,
  max_tokens?: integer (100-8000) = 2048,
  temperature?: float (0.0-1.0) = 0.7
}
```

### DraftOut

```typescript
{
  draft: string,
  generation_time_ms: float,
  model_used: string,
  citations: Citation[],
  sections: string[]
}
```

### HealthResponse

```typescript
{
  status: "healthy" | "unhealthy",
  version: string,
  offline_mode: boolean,
  ollama_available: boolean,
  timestamp: string (ISO 8601)
}
```

### ExportRequest

```typescript
{
  content: string,
  filename?: string,
  document_type?: "draft" | "memo" = "draft"
}
```

### ExportResponse

```typescript
{
  filename: string,
  file_path: string,
  file_size: integer
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid request parameters |
| `422` | Unprocessable Entity | Validation error (Pydantic) |
| `500` | Internal Server Error | Unexpected server error |
| `503` | Service Unavailable | Ollama service not available |

### Error Response Format

```json
{
  "detail": "Human-readable error message",
  "error": "ERROR_CODE",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

### Common Errors

#### 422 Validation Error

**Cause**: Invalid request parameters

**Example Response**:
```json
{
  "detail": [
    {
      "loc": ["body", "invention_description"],
      "msg": "ensure this value has at least 50 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

#### 503 Service Unavailable

**Cause**: Ollama service not accessible

**Example Response**:
```json
{
  "detail": "Ollama service is not available. Please ensure Ollama is running.",
  "error": "OLLAMA_UNAVAILABLE",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

#### 500 Internal Server Error

**Cause**: Unexpected error during generation

**Example Response**:
```json
{
  "detail": "Generation failed after 3 retries. Check logs for details.",
  "error": "GENERATION_FAILED",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

---

## Rate Limiting

Currently, the API has **no rate limiting** for local deployment. 

For production environments, consider implementing:
- Request rate limits (e.g., 10 requests/minute per IP)
- Concurrent request limits (e.g., 2 concurrent generations per user)
- Token bucket algorithm for fair usage

---

## Examples

### Python Example

```python
import requests

API_BASE = "http://localhost:8000"

# Check health
response = requests.get(f"{API_BASE}/health")
print(response.json())

# Generate memo
payload = {
    "invention_description": "A smart drone with obstacle avoidance...",
    "max_tokens": 2000,
    "temperature": 0.7
}

response = requests.post(
    f"{API_BASE}/generate/memo",
    json=payload,
    timeout=180
)

if response.status_code == 200:
    result = response.json()
    print(f"Generated memo: {len(result['draft'])} chars")
    print(f"Time taken: {result['generation_time_ms']/1000:.1f}s")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### JavaScript Example

```javascript
const API_BASE = "http://localhost:8000";

// Generate draft
async function generateDraft(description) {
  const response = await fetch(`${API_BASE}/generate/draft`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      invention_description: description,
      max_tokens: 3000,
      temperature: 0.7
    })
  });

  if (response.ok) {
    const result = await response.json();
    console.log(`Draft generated: ${result.draft.length} chars`);
    return result;
  } else {
    console.error(`Error: ${response.status}`);
    throw new Error(await response.text());
  }
}

// Usage
generateDraft("A smart delivery drone system...")
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

### cURL Examples

**Health Check**:
```bash
curl -X GET http://localhost:8000/health | jq
```

**Generate Memo (Fast Mode)**:
```bash
curl -X POST http://localhost:8000/generate/memo \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "A smart drone system with AI navigation",
    "max_tokens": 1500,
    "temperature": 0.7
  }' | jq '.draft' -r
```

**Generate Draft (Detailed Mode)**:
```bash
curl -X POST http://localhost:8000/generate/draft \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "An innovative medical device...",
    "max_tokens": 4000,
    "temperature": 0.7
  }' | jq
```

**Export to DOCX**:
```bash
curl -X POST http://localhost:8000/export/docx \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Patent Draft\n\nContent here...",
    "filename": "my_patent.docx"
  }' | jq
```

---

## Performance Considerations

### Generation Times

| Operation | Fast Mode | Detailed Mode |
|-----------|-----------|---------------|
| Memo Generation | 60-90s | 120-180s |
| Draft Generation | 60-90s | 120-180s |
| DOCX Export | 1-2s | 1-2s |

**Factors Affecting Speed**:
- CPU performance (single-threaded)
- RAM availability
- Input length
- Cold start (first request slower)

### Timeout Recommendations

```python
# Client-side timeouts
HEALTH_TIMEOUT = 5       # 5 seconds
EXPORT_TIMEOUT = 10      # 10 seconds
GENERATION_TIMEOUT = 240 # 4 minutes (buffer included)
```

### Best Practices

1. **Use Appropriate Timeouts**: Set client timeouts higher than server timeouts
2. **Handle Cold Starts**: First generation after server start is slower
3. **Check Health First**: Verify Ollama availability before generating
4. **Queue Requests**: Don't send concurrent generation requests (single worker)
5. **Cache Results**: Store generated content to avoid regeneration

---

## Versioning

**Current Version**: `0.1.0` (MVP)

**Version Format**: `MAJOR.MINOR.PATCH` (Semantic Versioning)

### Changelog

**v0.1.0** (November 2024):
- Initial MVP release
- Memo generation endpoint
- Draft generation endpoint
- DOCX export functionality
- Health check endpoint
- Offline operation support

---

## Support & Contact

- **Repository**: https://github.com/nandanpabolu/Capstone-Project-Team-4
- **Issues**: https://github.com/nandanpabolu/Capstone-Project-Team-4/issues
- **Documentation**: See `README.md` and `docs/ARCHITECTURE.md`

---

**Last Updated**: November 14, 2024  
**API Version**: 0.1.0  
**Team**: Team 4 - Patent Partners
