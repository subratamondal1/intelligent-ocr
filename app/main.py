import base64
import io

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from starlette.requests import Request

from services.ocr_pipeline import ocr_pipeline

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    # Read image content from the uploaded file
    contents = await file.read()

    # Convert to a PIL Image
    image = Image.open(io.BytesIO(contents))

    # Convert PIL Image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Save the image to the buffer in JPEG format
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Create the image source to use in the HTML template
    image_src = f"data:image/jpeg;base64,{image_base64}"

    # Dummy text for OCR
    ocr_text = ocr_pipeline(image=image)

    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "file_name": file.filename,
            "uploaded_image": image_src,
            "ocr_text": ocr_text,
        },
    )


# @app.post("/upload/", response_class=HTMLResponse)
# async def upload_image(request: Request, file: UploadFile = File(...)):
#     # Read image content from the uploaded file
#     contents = await file.read()

#     # Convert to a PIL Image
#     image = Image.open(io.BytesIO(contents))

#     # Convert PIL Image to base64
#     buffered = io.BytesIO()
#     image.save(buffered, format="JPEG")  # Save the image to the buffer in JPEG format
#     image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

#     # Create the image source to use in the HTML template
#     image_src = f"data:image/jpeg;base64,{image_base64}"

#     # Perform OCR
#     ocr_text = ocr_pipeline(image=image)

#     return templates.TemplateResponse(
#         "upload.html",
#         {
#             "request": request,
#             "file_name": file.filename,
#             "uploaded_image": image_src,
#             "ocr_text": ocr_text,
#         },
#     )
