from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Directory to store images
IMAGE_DIR = "images"

# Ensure the directory exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_path = os.path.join(IMAGE_DIR, file.filename)
    with open(image_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)
    return {"filename": file.filename}

@app.get("/images/")
async def list_images():
    images = os.listdir(IMAGE_DIR)
    if not images:
        raise HTTPException(status_code=404, detail="No images found")
    return {"images": images}  # Returning a JSON response

@app.get("/images/{filename}")
async def get_image(filename: str):
    image_path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path, media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

