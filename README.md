# Telangana Schools AI - Backend API

FastAPI backend for the Telangana Schools AI application with Google Firestore integration.

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Firebase/Firestore

#### Option A: Using Service Account Key (Recommended for Development)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Go to Project Settings > Service Accounts
4. Click "Generate New Private Key"
5. Save the JSON file as `serviceAccountKey.json` in the Backend folder
6. Update `.env` file with the path:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json
   ```

#### Option B: Using Default Credentials (For Production/GCP)

If running on Google Cloud Platform, the application will automatically use default credentials.

### 4. Configure Environment Variables

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` and set your Firebase credentials path.

### 5. Run the Development Server

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Available Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Items (Example CRUD)
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get a specific item
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

## Project Structure

```
Backend/
├── app.py              # Main FastAPI application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Development

### Adding New Endpoints

1. Define Pydantic models for request/response validation
2. Create route handlers using FastAPI decorators
3. Add proper error handling with HTTPException
4. Document endpoints with docstrings

### Testing the API

You can test the API using:
- The interactive Swagger UI at `/docs`
- curl commands
- Postman or similar API testing tools
- Python requests library

Example curl command:
```bash
# Create an item
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item"}'

# Get all items
curl "http://localhost:8000/items"
```

## Next Steps

- Add database integration (PostgreSQL, MongoDB, etc.)
- Implement authentication and authorization
- Add more specific endpoints for your application
- Set up logging and monitoring
- Add unit tests
- Configure production deployment
