from .logger import log_request
from .routes import router
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)
app.include_router(router=router)

# from docling.datamodel.base_models import DocumentStream
# from io import BytesIO
# from typing import Annotated, Union

# from PIL import Image


# @app.post('/ocr/invoice')
# async def tfn(file: Annotated[bytes, File()]):
#     byt = BytesIO(file)
#     img = Image.open(byt)
#     img.show()
#     # file = await file.read()
#     return "Something1"


# @app.post('/ocr/invoice1')
# async def tfn(body: FileBody):
#     if not body.file or body.file is None:
#         return {"error": "No upload file sent"}
    
#     decoded = b64decode(body.file)
#     byt = BytesIO(decoded)
#     img = Image.open(byt)
#     img.show()
#     # file = await file.read()
#     return "Something"
