import base64

from llm_client import call_vision_llm_json


print("Starting vision test...")


with open(
    "test_image.jpeg",
    "rb"
) as image_file:

    image_data = base64.b64encode(
        image_file.read()
    ).decode("utf-8")


image_url = (
    "data:image/jpeg;base64,"
    + image_data
)


print(
    "Image loaded."
)


prompt = """
Look at this image.

Return ONLY JSON:

{
    "finding": "brief description of visible findings",
    "confidence": 0.0
}
"""


print(
    "Calling vision model..."
)


result = call_vision_llm_json(
    prompt,
    image_url
)


print(
    "\nRESULT:"
)

print(result)