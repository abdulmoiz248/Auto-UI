"""
Test script for testing generated code.
This script can be used to validate the generated Next.js application structure.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.outline_agent import generate_outline
from utils.designer_agent import generate_design
from utils.project_manager_agent import manage_project
from utils.planner_agent import plan_website
from utils.component_specs_agent import generate_component_specs
from utils.component_gen_agent import generate_full_next_app
import asyncio


def test_full_flow(user_prompt: str):
    """
    Test the complete flow from user prompt to generated code.
    
    Args:
        user_prompt: User's requirement/prompt
    """
    print("=" * 80)
    print("TESTING FULL FLOW")
    print("=" * 80)
    print(f"User Prompt: {user_prompt}\n")
    
    # Step 1: Generate Outline
    print("Step 1: Generating outline...")
    try:
        outline = generate_outline(user_prompt)
        print(f"✓ Generated outline with {len(outline)} sections")
        print(f"  Sections: {[s.get('sectionName', 'N/A') for s in outline]}\n")
    except Exception as e:
        print(f"✗ Error generating outline: {e}\n")
        return
    
    # Step 2: Designer Agent
    print("Step 2: Designer agent generating design recommendations...")
    try:
        design = generate_design(user_prompt, outline)
        print(f"✓ Design theme: {design.theme.mode} mode, {design.theme.primaryColor} primary")
        print(f"  Principles: {', '.join(design.designPrinciples[:3])}...\n")
    except Exception as e:
        print(f"✗ Error generating design: {e}\n")
        design = None
    
    # Step 3: Project Manager Agent
    print("Step 3: Project manager scoping project...")
    try:
        pm_plan = manage_project(user_prompt, outline, design)
        print(f"✓ Project complexity: {pm_plan.scope.complexity}")
        print(f"  Recommended pages: {', '.join(pm_plan.recommendedPages)}\n")
    except Exception as e:
        print(f"✗ Error in project management: {e}\n")
        pm_plan = None
    
    # Step 4: Planner Agent (integrates designer and PM)
    print("Step 4: Planner agent creating final plan...")
    try:
        theme, pages = plan_website(outline, design, pm_plan, user_prompt)
        print(f"✓ Final theme: {theme.get('mode', 'N/A')} mode, {theme.get('primaryColor', 'N/A')} color")
        print(f"  Pages: {len(pages)} pages planned\n")
    except Exception as e:
        print(f"✗ Error in planning: {e}\n")
        return
    
    # Step 5: Component Specs
    print("Step 5: Generating component specs...")
    try:
        component_specs = generate_component_specs({"theme": theme, "pages": pages})
        total_components = sum(len(comps) for comps in component_specs.values())
        print(f"✓ Generated specs for {total_components} components across {len(component_specs)} pages\n")
    except Exception as e:
        print(f"✗ Error generating component specs: {e}\n")
        return
    
    # Step 6: Generate Full App
    print("Step 6: Generating full Next.js app...")
    try:
        result = asyncio.run(generate_full_next_app(component_specs, theme))
        files = result.get("files", {})
        print(f"✓ Generated {len(files)} files")
        print(f"  Key files: {', '.join(list(files.keys())[:10])}...\n")
        
        # Save to test output directory
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        for file_path, content in files.items():
            file_full_path = output_dir / file_path
            file_full_path.parent.mkdir(parents=True, exist_ok=True)
            file_full_path.write_text(content, encoding="utf-8")
        
        print(f"✓ Files saved to {output_dir}/")
        print(f"\nTo test the generated app:")
        print(f"  cd {output_dir}")
        print(f"  npm install")
        print(f"  npm run dev")
        
    except Exception as e:
        print(f"✗ Error generating app: {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


def test_individual_agents():
    """Test individual agents in isolation."""
    print("=" * 80)
    print("TESTING INDIVIDUAL AGENTS")
    print("=" * 80)
    
    test_prompt = "A modern SaaS dashboard for project management"
    
    # Test Outline Agent
    print("\n1. Testing Outline Agent...")
    try:
        outline = generate_outline(test_prompt)
        print(f"✓ Outline generated: {len(outline)} sections")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test Designer Agent
    print("\n2. Testing Designer Agent...")
    try:
        design = generate_design(test_prompt)
        print(f"✓ Design generated: {design.theme.primaryColor} theme")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test Project Manager Agent
    print("\n3. Testing Project Manager Agent...")
    try:
        pm_plan = manage_project(test_prompt)
        print(f"✓ PM plan generated: {pm_plan.scope.complexity} complexity")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the Auto-UI code generation system")
    parser.add_argument(
        "--prompt",
        type=str,
        default="A modern SaaS dashboard for project management",
        help="User prompt/requirement to test"
    )
    parser.add_argument(
        "--individual",
        action="store_true",
        help="Test individual agents instead of full flow"
    )
    
    args = parser.parse_args()
    
    if args.individual:
        test_individual_agents()
    else:
        test_full_flow(args.prompt)

