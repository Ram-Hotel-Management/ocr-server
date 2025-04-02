from typing import Union
from .logger import logger, log_request
from .routes import router
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)
app.include_router(router=router)


# from ai.modal import Modal, ModalName
# from PIL import Image

# img = Image.open("./1.jpg")
# modal = Modal(ModalName.GEMMA3_4B)
# res = modal.invoice_info(img)

# print(res.unwrap().to_json())