from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import os
import shutil
import firebase_admin
from firebase_admin import credentials, storage
import jwt

app = FastAPI()
SECRET_KEY = "your_secret_key"

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"storageBucket": "your-bucket-name.appspot.com"})

# JWT Authentication Middleware
def verify_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
async def root():
    return {"message": "GameSync AI Backend Running"}

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...), token: str = Depends(verify_token)):
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file)
    return {"file_url": blob.public_url}
