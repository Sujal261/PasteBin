from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
from app.database import create_paste, get_paste, get_paste_info, initialize_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    
    initialize_db()
    print("Database initialized")
"""Initialize the database when server starts"""
@app.post("/create/")
def create(request: Request, content: str, user_id: str, password: str = None, expires_after: int = None):
    """
    Create a new paste
    - content: The text content to store
    - user_id: Identifier for the user
    - password: Optional password protection
    - expires_after: Optional minutes until expiration
    """
    url_id = create_paste(content, user_id, password, expires_after)
    full_url = str(request.base_url) + f"view/{url_id}"
    return {"url": full_url, "url_id": url_id}

@app.get("/view/{url_id}")
def view(url_id: str, password: str = None):
    """
    View a paste
    - url_id: The unique identifier for the paste
    - password: Required if paste is password protected
    """
    paste = get_paste(url_id, password)
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    if 'error' in paste:
        raise HTTPException(status_code=403, detail=paste['error'])
    return paste

@app.get("/info/{url_id}")
def info(url_id: str):
    """
    Get basic info about a paste without viewing content
    """
    paste_info = get_paste_info(url_id)
    if not paste_info:
        raise HTTPException(status_code=404, detail="Paste not found")
    return paste_info
