from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.component_gen_agent import generate_full_next_app
from utils.outline_agent import generate_outline
from utils.designer_agent import generate_design
from utils.project_manager_agent import manage_project
from classes.cache import SemanticCache
from utils.planner_agent import plan_website
from pydantic import BaseModel
from typing import List, Optional
from utils.component_specs_agent import generate_component_specs
app = FastAPI()
cache = SemanticCache(redisHost="localhost", redisPort=6379)


class Outline(BaseModel):
    sectionName: str
    description: str

class OutlineRequest(BaseModel):
    outline: List[Outline]

class GenerateCodeRequest(BaseModel):
    outline: Optional[List[Outline]] = None
    topic: Optional[str] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/generate-outline")
def get_generated_outline(topic: str):
    # generated_outline = cache.getOrGenerate(topic, lambda: generate_outline(topic))
    return {"outline":  generate_outline(topic)}


@app.post("/generate-code")
async def generate_code(request: GenerateCodeRequest):
    """
    Generate code with integrated designer and project manager agents.
    Can accept either an outline or a topic string.
    """
    # Get outline - either from request or generate from topic
    if request.outline:
        outline = request.outline
        user_requirement = "User-provided outline"
    elif request.topic:
        user_requirement = request.topic
        outline = generate_outline(request.topic)
    else:
        return {"error": "Either 'outline' or 'topic' must be provided"}
    
    # Step 1: Designer Agent (using Gemini)
    print("🎨 Designer agent generating design recommendations...")
    try:
        design_recommendations = generate_design(user_requirement, outline)
        print(f"✓ Design theme: {design_recommendations.theme.mode} mode, {design_recommendations.theme.primaryColor} primary")
    except Exception as e:
        print(f"⚠ Designer agent error: {e}, continuing without design recommendations")
        design_recommendations = None
    
    # Step 2: Project Manager Agent (using Gemini)
    print("📋 Project manager scoping project...")
    try:
        project_plan = manage_project(user_requirement, outline, design_recommendations)
        print(f"✓ Project complexity: {project_plan.scope.complexity}")
    except Exception as e:
        print(f"⚠ Project manager error: {e}, continuing without PM recommendations")
        project_plan = None
    
    # Step 3: Planner Agent (integrates all inputs, uses Groq)
    print("📐 Planner agent creating final plan...")
    theme, pages = plan_website(outline, design_recommendations, project_plan, user_requirement)
    print("Planned website structure: ", {"theme": theme, "pages": len(pages)})
    
    # Step 4: Component Specs
    components_spec = generate_component_specs({"theme": theme, "pages": pages})
    print("Generated component specs")
    
    # Step 5: Generate Full App
    preview_data = await generate_full_next_app(components_spec, theme)
    return preview_data

# Keep old endpoint for backward compatibility
@app.post("/generate-code-legacy")
async def generate_code_legacy(request: OutlineRequest):
    """Legacy endpoint that doesn't use designer/PM agents."""
    theme, pages = plan_website(request.outline)
    print("Planned website structure: ", {"theme": theme})
    components_spec= generate_component_specs({"theme": theme, "pages": pages})
    print("Generated component specs")
    preview_data = await generate_full_next_app(components_spec, theme)
    return preview_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



#docker run -d --name redis-stack -p 6379:6379 redis/redis-stack
