from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from utils.call_gemini import call_gemini
import json


class ProjectScope(BaseModel):
    complexity: Literal["simple", "moderate", "complex"] = Field(..., description="Project complexity level")
    priorityFeatures: list[str] = Field(..., description="Must-have features")
    optionalFeatures: list[str] = Field(default_factory=list, description="Nice-to-have features")
    technicalRequirements: list[str] = Field(default_factory=list, description="Technical constraints or requirements")
    userPersonas: list[str] = Field(default_factory=list, description="Target user personas")


class ProjectPlan(BaseModel):
    scope: ProjectScope = Field(...)
    recommendedPages: list[str] = Field(..., description="Recommended page routes")
    componentPriorities: dict = Field(default_factory=dict, description="Component priority mapping")
    implementationPhases: list[str] = Field(default_factory=list, description="Suggested implementation phases")
    riskFactors: list[str] = Field(default_factory=list, description="Potential risks or challenges")


parser = PydanticOutputParser(pydantic_object=ProjectPlan)


def manage_project(user_requirement, outline=None, design_recommendations=None):
    """
    Act as project manager to scope and plan the project using Gemini.
    
    Args:
        user_requirement: User's original prompt/requirement
        outline: Optional outline data
        design_recommendations: Optional design recommendations from designer agent
    
    Returns:
        ProjectPlan object
    """
    outline_context = ""
    if outline:
        outline_data = outline
        if hasattr(outline, '__iter__') and outline and hasattr(outline[0], 'model_dump'):
            outline_data = [item.model_dump() for item in outline]
        outline_context = f"""
Initial Outline:
{json.dumps(outline_data, indent=2)}
"""
    
    design_context = ""
    if design_recommendations:
        design_context = f"""
Design Recommendations:
- Theme: {design_recommendations.theme.model_dump()}
- Principles: {design_recommendations.designPrinciples}
- Patterns: {design_recommendations.modernPatterns}
"""
    
    prompt = f"""You are an expert project manager for web development projects.

User Requirement: "{user_requirement}"
{outline_context}
{design_context}

Your responsibilities:
1. Analyze the project scope and complexity
2. Identify priority features vs optional features
3. Recommend optimal page structure and routes
4. Prioritize components based on importance
5. Suggest implementation phases if needed
6. Identify potential risks or challenges

Consider:
- User requirements and expectations
- Design recommendations (if provided)
- Technical feasibility
- User experience priorities
- Modern web development best practices

Focus on creating a realistic, achievable plan that balances:
- User needs
- Design aspirations
- Technical constraints
- Development efficiency

{parser.get_format_instructions()}

Return ONLY valid JSON matching the schema above.
"""
    
    response = call_gemini(
        [{"content": prompt}],
        system_prompt="You are an expert project manager. Always respond with valid JSON matching the requested schema."
    )
    
    parsed = parser.parse(response)
    return parsed


if __name__ == "__main__":
    requirement = "A modern SaaS dashboard for project management"
    plan = manage_project(requirement)
    print("Project Scope:", plan.scope.model_dump())
    print("Recommended Pages:", plan.recommendedPages)
    print("Implementation Phases:", plan.implementationPhases)

