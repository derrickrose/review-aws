import abc
# ----------------------------------------------------imports for image processing
import json
import sys

import boto3
from PIL import Image, ImageFont, ImageDraw
# ----------------------------------------------------imports for pdf processing
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PyPDF4 import PdfFileReader, PdfFileWriter

DESTINATION_S3_OBJECT_KEY_PREFIX = "watermarked/"
TEXT_TO_ADD = "orangebank"
SEPARATOR = "/"
# TODO use environment variable ?
# LOCAL_TEMP_SOURCE_DIRECTORY = "D:\lambda_watermark\\temp\original\\"
# LOCAL_TEMP_PROCESSED_DIRECTORY = "D:\lambda_watermark\\temp\watermarked\\"
#
LOCAL_TEMP_SOURCE_DIRECTORY = "/tmp/original/"
LOCAL_TEMP_PROCESSED_DIRECTORY = "/tmp/processed/"
# ----------------------------------------------IMAGE CONST
IMAGE_MODE = 'RGBA'
TEXT_OPACITY = 64  # 0 = transparent and 255 = full solid
TEXT_FONT_LABEL = "arial.ttf"
TEXT_FONT_SIZE = 82
TEXT_ANCHOR = "ms"

# ----------------------------------------------DOCUMENT CONST ADD HERE
s3_client = boto3.client(
    's3',
    verify=False,
)


class Processor:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text

    @abc.abstractmethod
    def put_watermark(self):
        pass


class ImageProcessor(Processor):

    def put_watermark(self):
        image = Image.open(f"{LOCAL_TEMP_SOURCE_DIRECTORY}{self.file_name}")
        font = ImageFont.truetype(TEXT_FONT_LABEL, TEXT_FONT_SIZE)
        text_layer = Image.new(IMAGE_MODE, image.size, (0, 0, 0, 0))
        if image.mode != IMAGE_MODE:
            image = image.convert(IMAGE_MODE)

        draw = ImageDraw.Draw(text_layer)
        # Positioning Text
        width, height = image.size
        text_position_x, text_position_y = int(width / 2), int(height / 2)

        draw.text((text_position_x, text_position_y), self.text, fill=(80, 80, 80, TEXT_OPACITY), font=font,
                  anchor=TEXT_ANCHOR)
        # Combining Original Image with Text and Saving
        watermarked = Image.alpha_composite(image, text_layer)
        # watermarked.show()
        watermarked.convert('RGB').save(f"{LOCAL_TEMP_PROCESSED_DIRECTORY}watermarked_{self.file_name}")


class DocumentProcessor(Processor):

    # todo find a way to optimize this call since it might be one shoot
    def _make_watermark(self):
        water_mark_document = f"{LOCAL_TEMP_SOURCE_DIRECTORY}watermark.pdf"
        pdf = canvas.Canvas(water_mark_document, pagesize=A4)
        pdf.translate(inch, inch)
        pdf.setFillColor(colors.grey, alpha=0.25)
        pdf.setFont("Helvetica", 50)
        pdf.rotate(45)
        pdf.drawCentredString(400, 100, self.text)
        pdf.save()
        return water_mark_document

    def put_watermark(self):
        watermark_document = PdfFileReader(self._make_watermark())
        watermark_page = watermark_document.getPage(0)
        pdf_reader = PdfFileReader(f"{LOCAL_TEMP_SOURCE_DIRECTORY}{self.file_name}")
        pdf_writer = PdfFileWriter()
        for page in pdf_reader.pages:
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        with open(f"{LOCAL_TEMP_PROCESSED_DIRECTORY}watermarked_{self.file_name}", 'wb') as out:
            pdf_writer.write(out)


def retrieve_file_name(key: str) -> str:
    return key.split(SEPARATOR)[-1:][0]


def lambda_handler(event, context):
    # for test, will use only the first record
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    file_name = retrieve_file_name(object_key)
    object_key_prefix = str(object_key).replace(file_name, "")

    s3_client.download_file(bucket_name, object_key, f"{LOCAL_TEMP_SOURCE_DIRECTORY}{file_name}")

    processor = None
    if file_name.lower().endswith("jpg") or file_name.lower().endswith("jpeg"):
        processor = ImageProcessor(file_name, TEXT_TO_ADD)
    elif file_name.lower().endswith("pdf"):
        processor = DocumentProcessor(file_name, TEXT_TO_ADD)
    processor.put_watermark()

    # todo send image/document to destination
    s3_client.upload_file(f"{LOCAL_TEMP_PROCESSED_DIRECTORY}watermarked_{file_name}", bucket_name,
                          f"{DESTINATION_S3_OBJECT_KEY_PREFIX}{file_name}")

    print("done")
