from utils.call_ai import call_ai
import json

def generate_component_specs(planned_structure):
    """
    Input: planned_structure = {
        "theme": {...},
        "pages": [...]
    }
    Output: {
        "pageRoute": {
            "componentId": {
                "name": str,
                "type": "layout | section | component",
                "props": [...],
                "state": {...},
                "libraries": [...],
                "usage": "guideline or description"
            }
        }
    }
    """

    system_prompt = (
        "You are a component spec generator for a frontend code generation system.\n"
        "You will receive a JSON object containing the planned pages and theme.\n"
        "For each page, generate specs for every section/component in a structured JSON format.\n\n"
        "Each component spec should include:\n"
        "- name: human-readable name\n"
        "- type: layout, section, or component\n"
        "- props: array of props it should receive\n"
        "- state: what internal state it may have (empty object if none)\n"
        "- libraries: any npm packages or UI libs required\n"
        "- usage: guidelines or description of purpose\n\n"
        "Output JSON structure example:\n"
        "{\n"
        '  "/": {\n'
        '    "layout-root": {\n'
        '      "name": "Root Layout",\n'
        '      "type": "layout",\n'
        '      "props": [],\n'
        '      "state": {},\n'
        '      "libraries": ["react", "next"],\n'
        '      "usage": "Main page wrapper for consistent layout across the app"\n'
        "    },\n"
        '    "landing-page": {\n'
        '      "name": "Landing Page",\n'
        '      "type": "section",\n'
        '      "props": ["title", "subtitle", "ctaText"],\n'
        '      "state": {"showPopup": false},\n'
        '      "libraries": ["react", "tailwindcss"],\n'
        '      "usage": "Hero section of the homepage with call-to-action"\n'
        "    }\n"
        "  }\n"
        "}\n\n"
        "CRITICAL Rules:\n"
        "- Output ONLY valid JSON - no explanations, no notes, no extra text\n"
        "- Do NOT add any text after the closing brace\n"
        "- Use theme information where relevant\n"
        "- Recommend only commonly used frontend libraries\n"
        "- Do not add sections/components not in the planned structure\n"
        "- Be deterministic and concise"
    )

    messages = [
        {
            "role": "user",
            "content": json.dumps(planned_structure)
        }
    ]

    print(f"Sending to AI - Input structure keys: {planned_structure.keys()}")
    print(f"Number of pages: {len(planned_structure.get('pages', []))}")
    
    result = call_ai(messages, system_prompt=system_prompt)

    try:
        if not result or result.strip() == "":
            print("ERROR: AI returned empty response")
            raise ValueError("Component Spec Agent returned empty response")
        
        print(f"Raw AI response length: {len(result)} chars")
        
        # Clean up the response - remove markdown blocks and extra text
        cleaned_result = result.strip()
        
        # Remove markdown code blocks
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result[7:]
        elif cleaned_result.startswith("```"):
            cleaned_result = cleaned_result[3:]
        if cleaned_result.endswith("```"):
            cleaned_result = cleaned_result[:-3]
        cleaned_result = cleaned_result.strip()
        
        # Find the last closing brace and cut everything after it
        last_brace = cleaned_result.rfind('}')
        if last_brace != -1:
            cleaned_result = cleaned_result[:last_brace + 1]
        
        print(f"✓ JSON cleaned and ready to parse")
        return json.loads(cleaned_result)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Cleaned result preview: {cleaned_result[:500]}...")
        raise ValueError(f"Component Spec Agent returned invalid JSON: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise ValueError(f"Component Spec Agent error: {str(e)}")
