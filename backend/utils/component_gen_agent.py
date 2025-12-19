import json
import asyncio
from pydantic import BaseModel, Field
from call_ai import call_ai


class GeneratedApp(BaseModel):
    files: dict[str, str] = Field(..., description="Dictionary mapping file paths to their content")


NEXT_PACKAGE_JSON = {
    "name": "generated-next-app",
    "version": "1.0.0",
    "scripts": {"dev": "next dev", "build": "next build", "start": "next start"},
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "next": "^14.0.0",
        "tailwindcss": "^3.3.3"
    }
}

NEXT_CONFIG_JS = "export default {}"

GLOBAL_CSS = "@tailwind base;\n@tailwind components;\n@tailwind utilities;"

async def generate_full_next_app(component_specs):
    # Simple file dictionary without Sandpack format
    files = {}

    # Add static Next.js boilerplate
    files["package.json"] = json.dumps(NEXT_PACKAGE_JSON, indent=2)
    files["next.config.js"] = NEXT_CONFIG_JS
    files["styles/globals.css"] = GLOBAL_CSS

    # Generate TSX components sequentially with delay to avoid rate limits
    print(f"Generating components for {len(component_specs)} pages...")
    
    comp_tasks = []
    for page_route, components in component_specs.items():
        page_folder = f"app{page_route}" if page_route != "/" else "app"
        for comp_id, spec in components.items():
            folder_path = f"{page_folder}/components"
            file_path = f"{folder_path}/{comp_id}.tsx"
            comp_tasks.append((file_path, spec, comp_id))
    
    print(f"Total components to generate: {len(comp_tasks)}")
    
    # Generate components one by one with delay
    for idx, (file_path, spec, comp_id) in enumerate(comp_tasks, 1):
        print(f"[{idx}/{len(comp_tasks)}] Generating {comp_id}...")
        path, code = await call_ai_component(file_path, spec)
        files[path] = code
        
        # Add delay between calls except for the last one
        if idx < len(comp_tasks):
            print(f"Waiting 30s to avoid rate limit...")
            await asyncio.sleep(30)

    # assemble main page.tsx per page route
    for page_route, components in component_specs.items():
        page_folder = f"app{page_route}" if page_route != "/" else "app"
        import_lines = []
        jsx_lines = []
        for comp_id in components.keys():
            comp_path = f"./components/{comp_id}"
            import_lines.append(f"import {to_camel_case(comp_id)} from '{comp_path}'")
            jsx_lines.append(f"<{to_camel_case(comp_id)} />")
        page_code = "\n".join(import_lines) + "\n\n" + "export default function Page() {\n  return (\n    <>\n      " + "\n      ".join(jsx_lines) + "\n    </>\n  )\n}"
        files[f"{page_folder}/page.tsx"] = page_code

    print("✓ All components generated")
    return GeneratedApp(files=files).model_dump()

async def call_ai_component(file_path, spec):
    prompt = (
        "You are a frontend code generator. Generate a fully functional TSX React component based on the spec below.\n\n"
        f"Component spec:\n{json.dumps(spec)}\n\n"
        "Requirements:\n"
        "- Include props and state\n"
        "- Use Tailwind CSS according to the theme\n"
        "- Use any recommended libraries\n"
        "- Functional component only\n"
        "- CRITICAL: Return ONLY the raw TSX code without any markdown code blocks, backticks, or ```tsx wrapper\n"
        "- NO explanations, NO markdown formatting, ONLY the code itself"
    )
    
    # Run the synchronous call_ai in a thread pool
    loop = asyncio.get_event_loop()
    tsx_code = await loop.run_in_executor(None, lambda: call_ai([{"content": prompt}]))
    
    # Clean up any markdown code blocks if present
    cleaned_code = tsx_code.strip()
    if cleaned_code.startswith("```tsx"):
        cleaned_code = cleaned_code[6:]
    elif cleaned_code.startswith("```"):
        cleaned_code = cleaned_code[3:]
    if cleaned_code.endswith("```"):
        cleaned_code = cleaned_code[:-3]
    cleaned_code = cleaned_code.strip()
    
    return file_path, cleaned_code

def to_camel_case(s):
    return "".join(word.title() for word in s.split("-"))
