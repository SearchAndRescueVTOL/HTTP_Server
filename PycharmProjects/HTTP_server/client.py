import requests

SERVER_URL = "http://127.0.0.1:8000"


def upload_image(image_path):
    url = f"{SERVER_URL}/upload/"
    with open(image_path, "rb") as image_file:
        files = {"file": (image_path, image_file, "multipart/form-data")}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        print(f"Image uploaded successfully: {response.json()}")
        return response.json().get("filename")
    else:
        print(f"Failed to upload image. Status code: {response.status_code}")
        return None


# Function to get an image by index
def get_image_by_index(index):
    url = f"{SERVER_URL}/images/"
    params = {"index": index}  # Passing the index as a query parameter
    response = requests.post(url, params=params)

    if response.status_code == 200:
        filename = response.headers.get('Content-Disposition').split('=')[1].strip('"')
        with open(f"downloaded_{filename}", "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully as 'downloaded_{filename}'")
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}, Error: {response.json()}")


if __name__ == "__main__":
    # First, upload an image
    image_path = "path_to_your_image.jpg"  # Provide the path to the image you want to upload
    filename = upload_image(image_path)
