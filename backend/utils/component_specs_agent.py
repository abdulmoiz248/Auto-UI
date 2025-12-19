from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field, RootModel
from typing import Literal
from utils.call_ai import call_ai
import json


class ComponentSpec(BaseModel):
    name: str = Field(..., description="Human-readable name")
    type: Literal["layout", "section", "component"] = Field(...)
    props: list[str] = Field(default_factory=list, description="Array of props it should receive")
    state: dict = Field(default_factory=dict, description="Internal state it may have")
    libraries: list[str] = Field(default_factory=list, description="NPM packages or UI libs required")
    usage: str = Field(..., description="Guidelines or description of purpose")


class PageComponentSpecs(RootModel[dict[str, ComponentSpec]]):
    """Maps component IDs to their specs for a single page."""
    pass


class ComponentSpecsOutput(RootModel[dict[str, dict[str, ComponentSpec]]]):
    """Maps page routes to their component specs."""
    pass


parser = PydanticOutputParser(pydantic_object=ComponentSpecsOutput)


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

    print(f"Sending to AI - Input structure keys: {planned_structure.keys()}")
    print(f"Number of pages: {len(planned_structure.get('pages', []))}")

    prompt = f"""
You are a component spec generator for a frontend code generation system.
You will receive a JSON object containing the planned pages and theme.
For each page, generate specs for every section/component in a structured JSON format.

Each component spec should include:
- name: human-readable name
- type: layout, section, or component
- props: array of props it should receive
- state: what internal state it may have (empty object if none)
- libraries: any npm packages or UI libs required
- usage: guidelines or description of purpose

Rules:
- Use theme information where relevant
- Recommend only commonly used frontend libraries
- Do not add sections/components not in the planned structure
- Be deterministic and concise

Input structure:
{json.dumps(planned_structure)}

Return ONLY valid JSON.
Do not include extra text.

{parser.get_format_instructions()}
"""

    response = call_ai([{"content": prompt}])
    
    if not response or response.strip() == "":
        print("ERROR: AI returned empty response")
        raise ValueError("Component Spec Agent returned empty response")
    
    print(f"Raw AI response length: {len(response)} chars")
    
    parsed = parser.parse(response)
    print(f"✓ JSON parsed successfully")
    return parsed.model_dump()


if __name__ == "__main__":
    sample_structure = {
        "theme": {
            "mode": "light",
            "primaryColor": "indigo",
            "radius": "lg",
            "spacing": "comfortable"
        },
        "pages": [
            {
                "route": "/",
                "title": "Home",
                "sections": [
                    {"id": "hero-section", "sectionName": "Hero Section", "type": "section"}
                ]
            }
        ]
    }
    specs = generate_component_specs(sample_structure)
    print(specs)
