# Ocr Route will handle 3 sub routes
# - /ocr/doc
# - /ocr/invoice
# - /ocr/chargeback

from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from io import BytesIO
from PIL import Image
from ..ai.modal import Modal, ModalName

import json

router = APIRouter()

docling_converter = DocumentConverter()

@router.post("/ocr/doc")
async def doc(file: UploadFile):
    try:
        file_type = None
        if file.filename.endswith((".doc", ".docx")):
            file_type = "Word Document"
        elif file.filename.endswith(".pdf"):
            file_type = "PDF"
        elif file.filename.endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")):
            file_type = "Image"

        if file_type is None:
            return HTTPException(406, json.dumps({"error": "Can only accept images, documents and pdfs"}))
        

        content = await file.read()
        file_content = BytesIO(content)

        result = docling_converter.convert(DocumentStream(stream=file_content, name=file.filename))
        dic = result.document.export_to_dict()

        return json.dumps(dic)

    except Exception as e:
        return HTTPException(500, json.dumps({"error": str(e)}))



ai_modal = Modal(ModalName.GEMMA3_4B)


#  Uses AI modal to retrieve trivial information from the image
@router.post("/ocr/invoice")
async def invoice(file: UploadFile):
    try:
        if not file.filename.endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")):
            return HTTPException(406, json.dumps({"error": "Can only accept images"}))
        

        content = await file.read()
        file_content = BytesIO(content)
        img = Image.open(file_content)

        return ai_modal.invoice_info(img).to_json()

    except Exception as e:
        return HTTPException(500, json.dumps({"error": str(e)}))


# Chargeback route
@router.get("/ocr/chargeback")
def chargeback():
    return {"response":"This route has not been built yet. Try again on later date."}