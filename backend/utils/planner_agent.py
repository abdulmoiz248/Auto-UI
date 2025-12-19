from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from call_ai import call_ai
import json


class Theme(BaseModel):
    mode: Literal["light", "dark"] = Field(...)
    primaryColor: str = Field(...)
    radius: Literal["sm", "md", "lg"] = Field(...)
    spacing: Literal["compact", "comfortable", "spacious"] = Field(...)


class SectionItem(BaseModel):
    id: str = Field(...)
    sectionName: str = Field(...)
    type: Literal["layout", "section", "component"] = Field(...)
    dependencies: list[str] = Field(default_factory=list)


class Page(BaseModel):
    route: str = Field(...)
    title: str = Field(...)
    sections: list[SectionItem] = Field(...)


class WebsitePlan(BaseModel):
    theme: Theme = Field(...)
    pages: list[Page] = Field(...)


parser = PydanticOutputParser(pydantic_object=WebsitePlan)


def plan_website(outline):
    # Convert Pydantic models to dictionaries if needed
    outline_data = outline
    if hasattr(outline, '__iter__') and outline and hasattr(outline[0], 'model_dump'):
        outline_data = [item.model_dump() for item in outline]

    prompt = f"""
You are a senior planning agent for an agentic frontend code generation system similar to v0.dev.

You will receive a JSON array representing a website outline. Each item contains:
- sectionName
- description

Your responsibilities:
1) Normalize section names (clear, concise, Title Case)
2) Finalize a single global design theme
3) Decide the required routes/pages
4) Assign each section to an appropriate page
5) Classify each section as one of:
   - layout (page-level structural wrapper)
   - section (major visible page section)
   - component (reusable UI element)
6) Define dependencies between sections when required

Strict rules:
- Be deterministic and consistent
- Do not invent extra sections beyond the outline
- Prefer minimal routes (combine sections when reasonable)

Input outline:
{json.dumps(outline_data)}

Return ONLY valid JSON.
Do not include extra text.

{parser.get_format_instructions()}
"""

    response = call_ai([{"content": prompt}])
    parsed = parser.parse(response)
    result = parsed.model_dump()
    return result.get("theme"), result.get("pages")


if __name__ == "__main__":
    sample_outline = [
        {"sectionName": "hero area", "description": "main introduction with call to action"},
        {"sectionName": "pricing cards", "description": "plans and pricing information"},
        {"sectionName": "contact form", "description": "user inquiry form"}
    ]
    theme, pages = plan_website(sample_outline)
    print("Theme:", theme)
    print("Pages:", pages)
