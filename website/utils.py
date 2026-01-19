import os
from django.conf import settings
from PIL import Image


def save_library_image(library_code, uploaded_file):
    folder = os.path.join(settings.MEDIA_ROOT, "libraries")
    os.makedirs(folder, exist_ok=True)

    image_path = os.path.join(folder, f"{library_code.lower()}.jpg")

    # Overwrite if already exists
    if os.path.exists(image_path):
        os.remove(image_path)

    image = Image.open(uploaded_file)

    # Ensure JPEG compatibility
    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(image_path, "JPEG", quality=85, optimize=True)
