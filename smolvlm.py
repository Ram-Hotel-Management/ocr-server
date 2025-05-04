from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import torch

model_path = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    # device="mps",
    # torch_dtype=torch.,
    _attn_implementation="eager"
).to("mps")

img = Image.open("./5.png")

messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "You are a OCR Engine with advanced reasoning on invoices. Only return the answer don't complete the sentence"
                    },
                    {"type": "image", "image": img},
                    {"type": "text", "text": "Who sent this invoice?"},
                     {"type": "text", "text": "What is the invoice number?"},

                ]
            },
            # {
            #     "role": "user",
            #     "content": [
            #     ]
            # },
            # {
            #     "role": "user",
            #     "content": [
            #          {"type": "text", "text": "What is the account or customer number?"},
            #     ]
            # },
            # {
            #     "role": "user",
            #     "content": [
            #         {"type": "text", "text": "What is the date of the invoice in MM/DD/YYYY format?"},
            #     ]
            # },
            # {
            #     "role": "user",
            #     "content": [
            #         {"type": "text", "text": "What is the due date in MM/DD/YYYY format?"},
            #     ]
            # },
            # {
            #     "role": "user",
            #     "content": [
            #         {"type": "text", "text": "What is the total amount?"}
            #     ]
            # },
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

generated_ids = model.generate(**inputs, do_sample=False, max_new_tokens=1024)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)
print(generated_texts[0])
