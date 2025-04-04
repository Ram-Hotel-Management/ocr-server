from .logger import log_request
# from .routes import router
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)
# app.include_router(router=router)


from docling.datamodel.base_models import DocumentStream
from io import BytesIO
from typing import Annotated, Union
from fastapi import UploadFile, File, Depends, Request, Form
from PIL import Image

@app.post('/ocr/invoice')
async def tfn(file: Union[UploadFile, None] = None):

    if not file:
        return {"message": "No upload file sent"}

    file = await file.read()
    # img = Image.open(file)
    return len(file)
