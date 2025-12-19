from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal, Optional
from utils.call_ai import call_ai
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


def plan_website(outline, design_recommendations=None, project_plan=None, user_requirement=None):
    """
    Plan website structure, integrating inputs from designer and project manager agents.
    
    Args:
        outline: Website outline from outline agent
        design_recommendations: Optional design recommendations from designer agent
        project_plan: Optional project plan from project manager agent
        user_requirement: Optional original user requirement for context
    """
    # Convert Pydantic models to dictionaries if needed
    outline_data = outline
    if hasattr(outline, '__iter__') and outline and hasattr(outline[0], 'model_dump'):
        outline_data = [item.model_dump() for item in outline]

    # Build context from other agents
    design_context = ""
    if design_recommendations:
        design_theme = design_recommendations.theme
        design_context = f"""
DESIGN RECOMMENDATIONS (from Designer Agent):
- Color Mode: {design_theme.mode}
- Primary Color: {design_theme.primaryColor}
- Secondary Color: {design_theme.secondaryColor}
- Radius: {design_theme.radius}
- Spacing: {design_theme.spacing}
- Typography: {design_theme.typography}
- Layout Style: {design_theme.layoutStyle}
- Animation Level: {design_theme.animationLevel}
- Design Principles: {', '.join(design_recommendations.designPrinciples)}
- Modern Patterns: {', '.join(design_recommendations.modernPatterns)}

IMPORTANT: Incorporate these design recommendations into your theme and component planning.
"""

    pm_context = ""
    if project_plan:
        pm_context = f"""
PROJECT MANAGEMENT RECOMMENDATIONS (from Project Manager Agent):
- Complexity: {project_plan.scope.complexity}
- Priority Features: {', '.join(project_plan.scope.priorityFeatures)}
- Recommended Pages: {', '.join(project_plan.recommendedPages)}
- Component Priorities: {json.dumps(project_plan.componentPriorities, indent=2)}

IMPORTANT: Consider these recommendations when structuring pages and prioritizing components.
"""

    user_context = ""
    if user_requirement:
        user_context = f"\nOriginal User Requirement: \"{user_requirement}\"\n"

    prompt = f"""
You are a senior planning agent for an agentic frontend code generation system similar to v0.dev.
{user_context}
You will receive a JSON array representing a website outline. Each item contains:
- sectionName
- description
{design_context}
{pm_context}
Your responsibilities:
1) Normalize section names (clear, concise, Title Case)
2) Finalize a single global design theme (incorporate design recommendations if provided)
3) Decide the required routes/pages (consider PM recommendations if provided)
4) Assign each section to an appropriate page
5) Classify each section as one of:
   - layout (page-level structural wrapper)
   - section (major visible page section)
   - component (reusable UI element)
6) Define dependencies between sections when required
7) Prioritize components based on PM recommendations if available

Strict rules:
- Be deterministic and consistent
- Do not invent extra sections beyond the outline
- Prefer minimal routes (combine sections when reasonable)
- If design recommendations are provided, use them to inform the theme
- If PM recommendations are provided, prioritize accordingly

Input outline:
{json.dumps(outline_data, indent=2)}

Return ONLY valid JSON.
Do not include extra text.

{parser.get_format_instructions()}
"""

    response = call_ai([{"content": prompt}])
    parsed = parser.parse(response)
    result = parsed.model_dump()
    
    # Merge design theme if available
    if design_recommendations:
        design_theme = design_recommendations.theme
        result["theme"]["mode"] = design_theme.mode
        result["theme"]["primaryColor"] = design_theme.primaryColor
        result["theme"]["radius"] = design_theme.radius
        result["theme"]["spacing"] = design_theme.spacing
    
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
