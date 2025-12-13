from utils.call_ai import call_ai
import json

def plan_website(outline):
    system_prompt = (
        "You are a senior planning agent for an agentic frontend code generation system similar to v0.dev.\n\n"
        "You will receive a JSON array representing a website outline. Each item contains:\n"
        "- sectionName\n"
        "- description\n\n"
        "Your responsibilities:\n"
        "1) Normalize section names (clear, concise, Title Case)\n"
        "2) Finalize a single global design theme\n"
        "3) Decide the required routes/pages\n"
        "4) Assign each section to an appropriate page\n"
        "5) Classify each section as one of:\n"
        "   - layout (page-level structural wrapper)\n"
        "   - section (major visible page section)\n"
        "   - component (reusable UI element)\n"
        "6) Define dependencies between sections when required\n\n"
        "Strict rules:\n"
        "- Output ONLY valid JSON\n"
        "- No explanations, no markdown, no comments\n"
        "- Be deterministic and consistent\n"
        "- Do not invent extra sections beyond the outline\n"
        "- Prefer minimal routes (combine sections when reasonable)\n\n"
        "Output JSON must follow this exact schema:\n"
        "{\n"
        '  "theme": {\n'
        '    "mode": "light | dark",\n'
        '    "primaryColor": "string",\n'
        '    "radius": "sm | md | lg",\n'
        '    "spacing": "compact | comfortable | spacious"\n'
        "  },\n"
        '  "pages": [\n'
        "    {\n"
        '      "route": "string",\n'
        '      "title": "string",\n'
        '      "sections": [\n'
        "        {\n"
        '          "id": "string",\n'
        '          "sectionName": "string",\n'
        '          "type": "layout | section | component",\n'
        '          "dependencies": ["string"]\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Example input:\n"
        "[\n"
        '  { "sectionName": "hero area", "description": "main introduction with call to action" },\n'
        '  { "sectionName": "pricing cards", "description": "plans and pricing information" },\n'
        '  { "sectionName": "contact form", "description": "user inquiry form" }\n'
        "]\n\n"
        "Example output:\n"
        "{\n"
        '  "theme": {\n'
        '    "mode": "light",\n'
        '    "primaryColor": "indigo",\n'
        '    "radius": "lg",\n'
        '    "spacing": "comfortable"\n'
        "  },\n"
        '  "pages": [\n'
        "    {\n"
        '      "route": "/",\n'
        '      "title": "Home",\n'
        '      "sections": [\n'
        "        {\n"
        '          "id": "layout-root",\n'
        '          "sectionName": "Root Layout",\n'
        '          "type": "layout",\n'
        '          "dependencies": []\n'
        "        },\n"
        "        {\n"
        '          "id": "hero-section",\n'
        '          "sectionName": "Hero Section",\n'
        '          "type": "section",\n'
        '          "dependencies": ["layout-root"]\n'
        "        },\n"
        "        {\n"
        '          "id": "pricing-section",\n'
        '          "sectionName": "Pricing Section",\n'
        '          "type": "section",\n'
        '          "dependencies": ["layout-root"]\n'
        "        },\n"
        "        {\n"
        '          "id": "contact-form",\n'
        '          "sectionName": "Contact Form",\n'
        '          "type": "component",\n'
        '          "dependencies": ["layout-root"]\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    # Convert Pydantic models to dictionaries if needed
    outline_data = outline
    if hasattr(outline, '__iter__') and outline and hasattr(outline[0], 'model_dump'):
        outline_data = [item.model_dump() for item in outline]
    
    messages = [
        {
            "role": "user",
            "content": json.dumps(outline_data)
        }
    ]

    result = call_ai(messages, system_prompt=system_prompt)

    try:
        parsed = json.loads(result)
        return parsed.get("theme"), parsed.get("pages")
    except Exception:
        raise ValueError("Planner agent returned invalid JSON")
