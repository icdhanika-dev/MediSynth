import base64

from agents.radiology_agent import analyze_radiology


# =====================================================
# LOAD TEST IMAGE
# =====================================================

image_path = "test_image.jpeg"


with open(
    image_path,
    "rb"
) as image_file:

    image_data = base64.b64encode(
        image_file.read()
    ).decode("utf-8")


# =====================================================
# CREATE IMAGE URL
# =====================================================

image_url = (
    "data:image/jpeg;base64,"
    + image_data
)


# =====================================================
# RUN RADIOLOGY AGENT
# =====================================================

print(
    "Testing Radiology Agent..."
)

print(
    "Image loaded successfully."
)


result = analyze_radiology(
    image_url
)


# =====================================================
# DISPLAY RESULT
# =====================================================

print(
    "\nRADIOLOGY AGENT RESULT:\n"
)


print(
    result
)