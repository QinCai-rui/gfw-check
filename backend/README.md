# GFW Check Backend

FastAPI backend server for checking if websites are blocked by the Great Firewall of China.

## Setup

1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python app/main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "GFW Check API"
}
```

### `POST /check?url=<url>`
Check if a URL is blocked by GFW.

**Parameters:**
- `url` (query parameter): The URL to check

**Response:**
```json
{
  "url": "https://example.com",
  "blocked": false,
  "timestamp": "2024-01-01T00:00:00"
}
```

## Running with Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

Create a `.env` file in the root directory for configuration:

```
# Add your configuration here
```

## Implementation TODO

- [ ] Implement actual GFW blocking check logic
- [ ] Add caching for repeated checks
- [ ] Add rate limiting
- [ ] Add logging
- [ ] Add tests
