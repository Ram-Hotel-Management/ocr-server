import re

class Invoice():
    def __init__(self, vendor: str, invoice_no: str,  acct_no: str, inv_date: str, due_date: str, total: str):
        self.invoice_no = invoice_no
        self.vendor = vendor
        self.acct_no = acct_no
        self.inv_date = inv_date
        self.due_date = due_date
        self.total = total

    
    @staticmethod
    def from_gemma3(val: str) -> 'Invoice':
        bullet_points = [item.strip() for item in val.split("\n") if item.strip() and item.startswith("*")]

        data_point = [re.sub(r"\*\s+\*\*(.*?)\*\*\s", "", item) for item in bullet_points]

        return Invoice(data_point[0], data_point[1], data_point[2], data_point[3], data_point[4], data_point[5])


    def to_json(self) -> dict:
        return {
            "invoice_no": self.invoice_no,
            "vendor": self.vendor,
            "acct_no": self.acct_no,
            "inv_date": self.inv_date,
            "due_date": self.due_date,
            "total": self.total
        }

        