# get the latest news
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-pro",
    "messages": [
      {
        "role": "user", 
        "content": "What are the major AI developments and announcements from today across the tech industry?"
      }
    ]
  }' | jq

```python
import requests

response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'sonar-pro',
        'messages': [
            {
                'role': 'user',
                'content': "What are the major AI developments and announcements from today across the tech industry?"
            }
        ]
    }
)

print(response.json())
```

# Domain search
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {
        "role": "user", 
        "content": "What are the most promising machine learning breakthroughs in computer vision and multimodal AI from recent arXiv publications?"
      }
    ],
    "search_domain_filter": ["arxiv.org"],
    "search_recency_filter": "month"
  }' | jq

```python
import requests

response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'sonar',
        'messages': [
            {
                'role': 'user',
                'content': 'What are the most promising machine learning breakthroughs in computer vision and multimodal AI from recent arXiv publications?'
            }
        ],
        'search_domain_filter': ['arxiv.org'],
        'search_recency_filter': 'month'
    }
)

print(response.json())
```
# Academic search
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {
        "role": "user", 
        "content": "What are the latest peer-reviewed findings on CRISPR gene editing applications in treating genetic disorders?"
      }
    ],
    "search_filter": "academic"
  }' | jq

```python
import requests

response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'sonar',
        'messages': [
            {
                'role': 'user',
                'content': 'What are the latest peer-reviewed findings on CRISPR gene editing applications in treating genetic disorders?'
            }
        ],
        'search_filter': 'academic'
    }
)

print(response.json())
```

# Structured search

curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-pro",
    "messages": [
      {
        "role": "user",
        "content": "Find the top 3 trending AI startups with recent funding. Include company name, funding amount, and focus area."
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "schema": {
          "type": "object",
          "properties": {
            "startups": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "company_name": {"type": "string"},
                  "funding_amount": {"type": "string"},
                  "focus_area": {"type": "string"}
                },
                "required": ["company_name", "funding_amount", "focus_area"]
              }
            }
          },
          "required": ["startups"]
        }
      }
    }
  }' | jq

```python
import requests

response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'sonar-pro',
        'messages': [
            {
                'role': 'user',
                'content': 'Find the top 3 trending AI startups with recent funding. Include company name, funding amount, and focus area.'
            }
        ],
        'response_format': {
            'type': 'json_schema',
            'json_schema': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'startups': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'company_name': {'type': 'string'},
                                    'funding_amount': {'type': 'string'},
                                    'focus_area': {'type': 'string'}
                                },
                                'required': ['company_name', 'funding_amount', 'focus_area']
                            }
                        }
                    },
                    'required': ['startups']
                }
            }
        }
    }
)

print(response.json())
```