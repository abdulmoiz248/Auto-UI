from utils.call_ai import call_ai
import json

def generate_outline(topic):
    system_prompt = (
        "Your goal is to take a user message about a website and break it down into key requirements. "
        "Analyze the user's intent and produce a structured JSON array representing the website outline. "
        "Each element in the array should have 'sectionName' and 'description', describing the purpose and content of that section." \
        "Dont include any introductory or concluding remarks, just the JSON array."
    )
    messages = [
        {
            "role": "user",
            "content": f"Create a detailed outline for a website about: '{topic}'."
        }
    ]
    outline = call_ai(messages, system_prompt=system_prompt)
    
    # Try to parse the response as JSON, fallback to string if invalid
    try:
        outline_json = json.loads(outline)
    except Exception:
        outline_json = outline
    
    return outline_json


print("Generating website outline...")