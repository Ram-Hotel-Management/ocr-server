# Ocr Route will handle 3 sub routes
# - /ocr/doc
# - /ocr/invoice
# - /ocr/chargeback
from typing import Annotated
from fastapi import APIRouter, File, HTTPException
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from io import BytesIO
from PIL import Image
from .modal import Modal, ModalName

import json

router = APIRouter()

# OCR on a doc
docling_converter = DocumentConverter()
@router.post("/ocr/doc")
async def doc(file: Annotated[bytes, File()]):
    try:
        file_content = BytesIO(file)

        result = docling_converter.convert(DocumentStream(stream=file_content, name="unknowns"))
        dic = result.document.export_to_dict()

        return json.dumps(dic)

    except Exception as e:
        return error(e)


# Invoice parsing
ai_modal = Modal(ModalName.GEMMA3_4B)
#  Uses AI modal to retrieve trivial information from the image
@router.post("/ocr/invoice")
async def invoice(file: Annotated[bytes, File()]) :
    try:
        file_content = BytesIO(file)
        img = Image.open(file_content)
        return ai_modal.invoice_info(img).to_json()
    except Exception as e:
        return error(e)
    

def error(e: Exception, status_code=500) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": str(e)})


# Chargeback route
@router.get("/ocr/chargeback")
def chargeback():
    return {"error":"This route has not been built yet. Try again on later date."}