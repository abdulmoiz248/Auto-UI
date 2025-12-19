from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from utils.call_gemini import call_gemini
import json


class DesignTheme(BaseModel):
    mode: Literal["light", "dark", "auto"] = Field(..., description="Color mode")
    primaryColor: str = Field(..., description="Primary brand color (hex or color name)")
    secondaryColor: str = Field(..., description="Secondary accent color")
    radius: Literal["sm", "md", "lg", "xl"] = Field(..., description="Border radius style")
    spacing: Literal["compact", "comfortable", "spacious"] = Field(..., description="Spacing style")
    typography: Literal["modern", "classic", "futuristic", "minimal"] = Field(..., description="Typography style")
    layoutStyle: Literal["centered", "full-width", "asymmetric", "grid"] = Field(..., description="Layout approach")
    animationLevel: Literal["none", "subtle", "moderate", "dynamic"] = Field(..., description="Animation intensity")
    colorPalette: dict = Field(default_factory=dict, description="Extended color palette")


class DesignRecommendations(BaseModel):
    theme: DesignTheme = Field(...)
    designPrinciples: list[str] = Field(..., description="Key design principles to follow")
    componentGuidelines: dict = Field(default_factory=dict, description="Guidelines for specific components")
    modernPatterns: list[str] = Field(..., description="Modern UI patterns to incorporate")


parser = PydanticOutputParser(pydantic_object=DesignRecommendations)


def generate_design(user_requirement, outline=None):
    """
    Generate modern, futuristic design recommendations using Gemini.
    
    Args:
        user_requirement: User's original prompt/requirement
        outline: Optional outline data for context
    
    Returns:
        DesignRecommendations object
    """
    outline_context = ""
    if outline:
        outline_data = outline
        if hasattr(outline, '__iter__') and outline and hasattr(outline[0], 'model_dump'):
            outline_data = [item.model_dump() for item in outline]
        outline_context = f"""
Website Outline Context:
{json.dumps(outline_data, indent=2)}
"""
    
    prompt = f"""You are an expert UI/UX designer specializing in modern, futuristic, and cutting-edge web design.

User Requirement: "{user_requirement}"
{outline_context}

Your task is to create a comprehensive design system that is:
1. Modern and futuristic - think glassmorphism, neumorphism, gradient meshes, micro-interactions
2. Visually striking - bold colors, creative layouts, innovative patterns
3. User-friendly - accessible, intuitive, responsive
4. Trend-forward - incorporate latest 2024-2025 design trends

Design considerations:
- Use modern color schemes (gradients, vibrant colors, dark mode support)
- Implement contemporary UI patterns (floating elements, blurred backgrounds, smooth animations)
- Consider glassmorphism, neumorphism, or other modern effects
- Ensure excellent contrast and readability
- Make it mobile-first and responsive
- Include micro-interactions and smooth transitions

Generate a complete design system including:
- Color palette (primary, secondary, accent colors)
- Typography style (modern, futuristic, minimal, etc.)
- Layout approach (centered, full-width, asymmetric, grid-based)
- Animation preferences (subtle, moderate, or dynamic)
- Design principles to follow
- Component-specific guidelines
- Modern UI patterns to incorporate

{parser.get_format_instructions()}

Return ONLY valid JSON matching the schema above.
"""
    
    response = call_gemini(
        [{"content": prompt}],
        system_prompt="You are an expert UI/UX designer. Always respond with valid JSON matching the requested schema."
    )
    
    parsed = parser.parse(response)
    return parsed


if __name__ == "__main__":
    requirement = "A modern SaaS dashboard for project management"
    design = generate_design(requirement)
    print("Design Theme:", design.theme.model_dump())
    print("Design Principles:", design.designPrinciples)
    print("Modern Patterns:", design.modernPatterns)

