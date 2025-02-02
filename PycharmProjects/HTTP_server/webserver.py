from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os

app = FastAPI()

#directory to store uploaded images
IMAGE_DIR = 'images'

#creates directory if it doesn't exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

#upload image through post request
@app.post("/upload/")
async def upload_image(file:UploadFile = File(...)):
    image_path = os.path.join(IMAGE_DIR, file.filename)
    with open(image_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)
    return {"filename": file.filename}

@app.post("/images/")
async def get_all_images(index:int):
    images = os.listdir(IMAGE_DIR)
    if index < 0 or index >= len(images):
        raise HTTPException(status_code = 404, detail = "Image not found")
    image_name = images[index]
    return FileResponse(os.path.join(IMAGE_DIR,image_name))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) #need to update to what port works
