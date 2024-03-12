# Barcode + GPhoto

Simple python script that reads a barcode from the reader (any text actually)
and takes a photo using GPhoto2.
The photos are prefixed with the text from the barcode.

## Workflow

1. Capture image with gphoto (RAW + JPEG) on new barcode .
2. Transfer image to local machine.
3. Rename with barcode as prefix.
4. Open the preview of the JPEG.
5. Save barcode to a list (must be unique) for later use.

## Docker usage

`docker compose run --rm barcode-gphoto python main.py`
