from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Telangana Schools AI API",
    description="Backend API for Telangana Schools AI application with Firestore integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #update this with your requirements.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # Check if Firebase app is already initialized
    from firebase_admin import _apps
    
    if not _apps:
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try to get credentials path from environment variable
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # If not set in env, use the default path in the Backend directory
        if not cred_path:
            cred_path = os.path.join(current_dir, "serviceAccountKey.json")
        # If it's a relative path, make it absolute relative to current directory
        elif not os.path.isabs(cred_path):
            cred_path = os.path.join(current_dir, cred_path)
        
        print(f"🔍 Looking for Firebase credentials at: {cred_path}")
        
        if os.path.exists(cred_path):
            print(f"✅ Found credentials file")
            cred = credentials.Certificate(cred_path)
            initialize_app(cred)
            print("✅ Firebase initialized successfully")
        else:
            print(f"❌ Credentials file not found at: {cred_path}")
            print("⚠️  Attempting to initialize without credentials (will use default credentials if available)")
            initialize_app()
            print("✅ Firebase initialized with default credentials")
    else:
        print("ℹ️  Firebase already initialized (hot reload)")
    
    db = firestore.client()
        
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    db = None

# Pydantic models for request/response
# Pydantic models for response
class ChapterData(BaseModel):
    class_number: int
    chapter_number: int
    video_url: Optional[str] = None
    audio_url: Optional[str] = None

# Routes
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Telangana Schools AI API",
        "status": "running",
        "version": "1.0.0",
        "firestore_connected": db is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    firestore_status = "connected" if db is not None else "disconnected"
    return {
        "status": "healthy",
        "firestore": firestore_status
    }

@app.get("/chapter", response_model=ChapterData)
async def get_chapter(class_number: int, chapter_number: int):
    """
    Get chapter data by class and chapter number
    
    Parameters:
    - class_number: The class/grade number (e.g., 9, 10)
    - chapter_number: The chapter number (e.g., 1, 2, 3)
    
    Returns:
    - Chapter data including video URL and audio URL
    
    Example:
    - GET /chapter?class_number=9&chapter_number=1
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Firestore not initialized")
    
    try:
        # Construct document ID based on your Firestore structure
        # Format: class{class_number}chapter{chapter_number}
        doc_id = f"class{class_number}chapter{chapter_number}"
        
        # Get document from 'content' collection
        doc_ref = db.collection('content').document(doc_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(
                status_code=404, 
                detail=f"Chapter {chapter_number} not found for class {class_number}"
            )
        
        # Get the document data
        chapter_data = doc.to_dict()
        
        return {
            "class_number": chapter_data.get("class", class_number),
            "chapter_number": chapter_data.get("Chapter", chapter_number),
            "video_url": chapter_data.get("video_url"),
            "audio_url": chapter_data.get("audio_url")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chapter: {str(e)}")

# Run the application
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


