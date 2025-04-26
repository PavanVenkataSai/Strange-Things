# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import io

# def add_signature_to_pdf(input_filename, output_filename, signature_image_path):
#     # Read the PDF
#     reader = PdfReader(input_filename)
#     writer = PdfWriter()

#     # Add each page to the writer except the last one
#     for page in reader.pages[:-1]:
#         writer.add_page(page)

#     # Create a new page for the signature
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)

#     # Calculate the position for the signature at the bottom right corner
#     # Assuming the signature image is 200x20 pixels
#     signature_width = 300
#     signature_height = 150
#     page_width, page_height = letter
#     x = page_width - signature_width - 50 # Adjust the x position to place it at the bottom right
#     y = page_height - signature_height - 50 # Adjust the y position to place it at the bottom right

#     print(x,y)
#     # Draw the signature image at the calculated position
#     can.drawImage(signature_image_path, 400, 400, width=signature_width, height=signature_height)   #For the neuravie pdf
#     # can.drawImage(signature_image_path, 350, 20, width=signature_width, height=signature_height)

#     can.save()

#     # Move to the beginning of the StringIO buffer
#     packet.seek(0)
#     signature_pdf = PdfReader(packet)
#     signature_page = signature_pdf.pages[0]

#     # Merge the signature page with the last page of the original PDF
#     last_page = reader.pages[-1]
#     last_page.merge_page(signature_page)

#     # Add the merged page to the writer
#     writer.add_page(last_page)

#     # Write out the new PDF
#     with open(output_filename, "wb") as output_pdf:
#         writer.write(output_pdf)



# # Example usage
# input_pdf_path = r"C:\Users\CVHS\pavan\Strange_things\Neuravive HCP.pdf"
# output_pdf_path = r"output.pdf"
# signature_image_path = r"C:\Users\CVHS\pavan\Strange_things\Digital_signature.jpg"


# add_signature_to_pdf(input_pdf_path, output_pdf_path, signature_image_path)
import os
import requests
import os
import requests
# from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = "prasanthvijayaraj2002@gmail.com_r2Y9jE76r8JNKNr5Do6M6K09B7uVi9M5VPJ4k704Pd9TJK3l99FciS81JWQQWfpY"


# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Direct URL of source PDF file.
SourceFileUrl = "https://preciumweb-dev.s3.amazonaws.com/dummy.pdf"

# Destination PDF file name
DestinationFile = "./result.pdf"

# Image params
Width = 300
Height = 150
ImageUrl = "https://drive.google.com/file/d/1aZ19C0uhcr-S0OaeuGP2mCodVpdpHmrs/view?usp=sharing"


def addImageToExistingPdf(destinationFile):
    import json

    # Prepare requests params as JSON
    payload = json.dumps({
        "name": os.path.basename(destinationFile),
        "password": "",
        "url": SourceFileUrl,
        "images": []
    })

    # Prepare URL for 'PDF Edit' API request
    url = f"{BASE_URL}/pdf/edit/add"

    # Execute request and get response as JSON
    response = requests.post(url, data=payload, headers={"x-api-key": API_KEY})

    if response.status_code == 200:
        json_response = response.json()

        if not json_response["error"]:
            result_file_url = json_response["url"]

            # Download result file
            r = requests.get(result_file_url, stream=True)

            if r.status_code == 200:
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            print(json_response["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def add_signature_to_bottom_of_each_page(destinationFile):
    # Load existing PDF
    with open(destinationFile, "rb") as file:
        existing_pdf = PdfReader(file)
        output_pdf = PdfWriter()

        # Iterate through each page
        for i in range(existing_pdf.pages):
            page = existing_pdf.getPage(i)

            # Get page dimensions
            page_width = page.mediaBox.getWidth()

            # Calculate signature position
            x = (page_width - Width) / 2
            y = Height  # Distance from the bottom
            page.mergeTranslatedPage(ImageReader(ImageUrl), x, y, Width, Height)

            # Add modified page to output PDF
            output_pdf.addPage(page)

        # Write output PDF to file
        with open("output.pdf", "wb") as output_file:
            output_pdf.write(output_file)


def main():
    addImageToExistingPdf(DestinationFile)
    add_signature_to_bottom_of_each_page(DestinationFile)


if __name__ == '__main__':
    main()

