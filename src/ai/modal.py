from enum import Enum
from transformers import pipeline
import torch
from PIL.Image import Image
from platform import system
from ..invoice import Invoice

# runs on the fastest device possible
def device() -> str:
    if torch.cuda.is_available():
        return "cuda:0"
    
    if system() == "Darwin":
        return "mps"
    
    return "cpu"

class ModalName(Enum):
    GEMMA3_4B = "./gemma-3-4b-it"
    GEMMA3_12B = "./gemma-3-12b-it"

class Modal:
    def __init__(self,  name: ModalName):
        try:
            self.modal = pipeline(
                "image-text-to-text",
                model=name.value,
                device=device(),
                torch_dtype=torch.bfloat16,
            )
        except Exception as e:
            raise e.add_note("An error occurred while loading the modal")
       
    
    def invoice_info(self, img: Image) -> Invoice:
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a OCR Engine with advanced reasoning on invoices"}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img},
                    {"type": "text", "text": "Who is the vendor?"},
                    {"type": "text", "text": "What is the invoice number?"},
                    {"type": "text", "text": "What is the account number?"},
                    {"type": "text", "text": "What is the date of the invoice in MM/DD/YYYY format?"},
                    {"type": "text", "text": "What is the due date in MM/DD/YYYY format?"},
                    {"type": "text", "text": "What is the total amount?"}
                ]
            }
        ]

        output = self.modal(text=messages, max_new_tokens=200)
        output = output[0]["generated_text"][-1]["content"]
        return Invoice.from_gemma3(output)


