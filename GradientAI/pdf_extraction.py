
import os

from dotenv import load_dotenv

from gradientai import Gradient

load_dotenv()


GRADIENT_ACCESS_TOKEN  = os.getenv("GRADIENT_ACCESS_TOKEN")
GRADIENT_WORKSPACE_ID  = os.getenv("GRADIENT_WORKSPACE_ID")


gradient = Gradient()

filepath = r"C:\Users\CVHS\pavan\New_email\attachments\ponnusamy5k2valuehealthsol5com__enrollment-form(fully filled)_signed.pdf"
result = gradient.extract_pdf(
    filepath=filepath
)
print(type(result["text"]))

with open("result_","w+") as f:
    f.write(result["text"])


