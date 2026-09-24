import json
import time

from groq import Groq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    VISION_MODEL
)


# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(
    api_key=GROQ_API_KEY,
    timeout=30.0
)


# =====================================================
# NORMAL TEXT LLM
# =====================================================

def call_llm(prompt: str) -> str:

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model=GROQ_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                max_completion_tokens=2048
            )

            return response.choices[0].message.content

        except Exception as e:

            print(
                "Groq request failed:",
                e
            )

            if attempt < 2:

                print(
                    "Retrying..."
                )

                time.sleep(
                    2 ** attempt
                )


    raise RuntimeError(
        "LLM request failed after 3 attempts."
    )


# =====================================================
# VISION LLM
# =====================================================

def call_vision_llm_json(
    prompt: str,
    image_url: str
) -> dict:

    for attempt in range(3):

        try:

            print(
                "Sending image to Vision LLM..."
            )


            response = client.chat.completions.create(

                model=VISION_MODEL,

                messages=[
                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "text",

                                "text": prompt
                            },

                            {
                                "type": "image_url",

                                "image_url": {
                                    "url": image_url
                                }
                            }

                        ]
                    }
                ],

                temperature=0.2,

                max_completion_tokens=1024,

                response_format={
                    "type": "json_object"
                }
            )


            print(
                "Vision response received."
            )


            result = (
                response
                .choices[0]
                .message
                .content
            )


            print(
                "Vision output:"
            )

            print(result)


            return json.loads(
                result
            )


        except Exception as e:

            print(
                "Vision request failed:",
                e
            )


            if attempt < 2:

                print(
                    "Retrying..."
                )

                time.sleep(
                    2 ** attempt
                )


    raise RuntimeError(
        "Vision LLM request failed after 3 attempts."
    )


# =====================================================
# NORMAL JSON LLM
# =====================================================

def call_llm_json(
    prompt: str,
    agent_name: str
) -> dict:


    prompt = prompt + """

Return only valid JSON.
Do not use markdown.
Do not put the JSON inside code blocks.

Use this structure:

{
    "agent": "AGENT_NAME",

    "findings": [
        {
            "finding": "string",
            "evidence": "string",
            "confidence": 0.0
        }
    ],

    "possible_conditions": [
        "string"
    ],

    "uncertainties": [
        "string"
    ],

    "contradictions": [
        "string"
    ]
}

possible_conditions, uncertainties, and contradictions
must contain only strings.

Do not use objects or dictionaries inside these lists.
"""


    prompt = prompt.replace(
        "AGENT_NAME",
        agent_name
    )


    result = call_llm(
        prompt
    )


    try:

        return json.loads(
            result
        )


    except json.JSONDecodeError:

        start = result.find(
            "{"
        )

        end = result.rfind(
            "}"
        ) + 1


        if start == -1 or end == 0:

            raise ValueError(
                "The model did not return valid JSON."
            )


        return json.loads(
            result[start:end]
        )