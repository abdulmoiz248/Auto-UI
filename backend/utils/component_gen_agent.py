import json
import asyncio
from pydantic import BaseModel, Field
from utils.call_gemini import call_gemini 


class GeneratedApp(BaseModel):
    files: dict[str, str] = Field(..., description="Dictionary mapping file paths to their content")


# Modern Next.js 14+ dependencies with shadcn/ui support
NEXT_PACKAGE_JSON = {
    "name": "generated-next-app",
    "version": "1.0.0",
    "private": True,
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "next": "^14.2.0",
        "tailwindcss": "^3.4.0",
        "tailwindcss-animate": "^1.0.7",
        "@radix-ui/react-slot": "^1.0.2",
        "class-variance-authority": "^0.7.0",
        "clsx": "^2.1.0",
        "tailwind-merge": "^2.2.0",
        "lucide-react": "^0.400.0"
    },
    "devDependencies": {
        "@types/node": "^20.0.0",
        "@types/react": "^18.2.0",
        "@types/react-dom": "^18.2.0",
        "typescript": "^5.3.0",
        "autoprefixer": "^10.4.0",
        "postcss": "^8.4.0"
    }
}

NEXT_CONFIG_JS = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
"""

TS_CONFIG_JSON = {
    "compilerOptions": {
        "target": "ES2017",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": True,
        "skipLibCheck": True,
        "strict": True,
        "noEmit": True,
        "esModuleInterop": True,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": True,
        "isolatedModules": True,
        "jsx": "preserve",
        "incremental": True,
        "plugins": [
            {
                "name": "next"
            }
        ],
        "paths": {
            "@/*": ["./*"]
        }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}

TAILWIND_CONFIG_JS = """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
"""

POSTCSS_CONFIG_MJS = """/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

export default config
"""

GLOBAL_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""

UTILS_TS = """import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""


async def generate_full_next_app(component_specs, theme=None):
    """
    Generate a complete Next.js 14+ App Router application.
    
    Args:
        component_specs: Dict mapping page routes to component specs
        theme: Optional theme configuration from planner
    """
    files = {}
    
    # Generate config files first
    generate_config_files(files)
    
    # Generate root layout
    generate_root_layout(files, theme)
    
    # Generate components and pages in batches (one API call per page)
    print(f"Generating components for {len(component_specs)} pages...")
    
    for page_idx, (page_route, components) in enumerate(component_specs.items(), 1):
        print(f"[{page_idx}/{len(component_specs)}] Generating page: {page_route}")
        
        # Generate all components for this page in one batch
        page_components = await generate_page_components_batch(
            page_route, components, theme
        )
        files.update(page_components)
        
        # Assemble the page.tsx file
        page_code = assemble_page_with_types(page_route, components)
        page_folder = get_page_folder(page_route)
        files[f"{page_folder}/page.tsx"] = page_code
    
    print("✓ All components and pages generated")
    return GeneratedApp(files=files).model_dump()


def generate_config_files(files):
    """Generate all necessary configuration files."""
    files["package.json"] = json.dumps(NEXT_PACKAGE_JSON, indent=2)
    files["next.config.js"] = NEXT_CONFIG_JS
    files["tsconfig.json"] = json.dumps(TS_CONFIG_JSON, indent=2)
    files["tailwind.config.js"] = TAILWIND_CONFIG_JS
    files["postcss.config.mjs"] = POSTCSS_CONFIG_MJS
    files["app/globals.css"] = GLOBAL_CSS
    files["lib/utils.ts"] = UTILS_TS
    
    # Generate basic shadcn/ui components
    generate_shadcn_components(files)


def generate_root_layout(files, theme=None):
    """Generate the root layout.tsx file."""
    theme_class = ""
    if theme and theme.get("mode") == "dark":
        theme_class = ' className="dark"'
    
    layout_code = f"""import type {{ Metadata }} from "next"
import {{ Inter }} from "next/font/google"
import "./globals.css"

const inter = Inter({{ subsets: ["latin"] }})

export const metadata: Metadata = {{
  title: "Generated App",
  description: "Generated by Auto-UI",
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en"{theme_class}>
      <body className={{inter.className}}>{{children}}</body>
    </html>
  )
}}
"""
    files["app/layout.tsx"] = layout_code


async def generate_page_components_batch(page_route, components, theme=None):
    """
    Generate all components for a single page in one API call.
    
    Returns a dict mapping file paths to component code.
    """
    page_folder = get_page_folder(page_route)
    
    # Build the prompt for batch generation
    components_spec_list = []
    for comp_id, spec in components.items():
        components_spec_list.append({
            "id": comp_id,
            "spec": spec
        })
    
    prompt = build_batch_component_prompt(components_spec_list, theme, page_route)
    
    # Call AI to generate all components at once
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: call_gemini(messages=[{"content": prompt}])
    )
    
    # Parse the response (expecting JSON with component code)
    try:
        # Try to parse as JSON first
        parsed = json.loads(response)
        if isinstance(parsed, dict):
            # If it's a dict mapping component IDs to code
            components_code = parsed
        else:
            # Fallback: try to extract code blocks
            components_code = extract_components_from_response(response, components)
    except json.JSONDecodeError:
        # If not JSON, try to extract individual components
        components_code = extract_components_from_response(response, components)
    
    # Map to file paths
    files = {}
    for comp_id, code in components_code.items():
        comp_name = to_pascal_case(comp_id)
        file_path = f"{page_folder}/components/{comp_name}.tsx"
        files[file_path] = clean_code(code)
    
    return files


def build_batch_component_prompt(components_spec_list, theme, page_route):
    """Build a prompt to generate all components for a page in one call."""
    theme_info = ""
    if theme:
        theme_info = f"""
Theme Configuration:
- Mode: {theme.get('mode', 'light')}
- Primary Color: {theme.get('primaryColor', 'blue')}
- Radius: {theme.get('radius', 'md')}
- Spacing: {theme.get('spacing', 'comfortable')}
"""
    
    components_json = json.dumps(components_spec_list, indent=2)
    
    # Build component list for the prompt
    component_ids = [comp["id"] for comp in components_spec_list]
    
    prompt = f"""You are an expert Next.js 14+ and React developer. Generate complete, production-ready TypeScript React components.

Generate ALL components for the page route: {page_route}
{theme_info}

Components to generate (with their specs):
{components_json}

CRITICAL REQUIREMENTS:
1. Use Next.js 14+ App Router conventions
2. Use TypeScript with proper types and interfaces
3. Use shadcn/ui components from @/components/ui when appropriate (Button, Card, Input, etc.)
4. Use Tailwind CSS utility classes - be creative and modern
5. Use React Server Components by default, add "use client" directive only when needed (for hooks, interactivity, event handlers)
6. Import paths must use @/ aliases (e.g., @/components/ui/button, @/lib/utils)
7. Use the cn() utility from @/lib/utils for className merging
8. Follow modern React patterns (functional components, proper hooks)
9. Include proper TypeScript interfaces for props
10. Make components responsive and accessible
11. Use the component spec's props, state, and usage guidelines
12. Apply the theme colors and styling preferences

OUTPUT FORMAT - Return a valid JSON object with this exact structure:
{{
  "{component_ids[0] if component_ids else 'component-1'}": "complete tsx code here as string",
  "{component_ids[1] if len(component_ids) > 1 else 'component-2'}": "complete tsx code here as string"
}}

CRITICAL: 
- Return ONLY valid JSON, no markdown, no code blocks, no explanations
- Each value must be the complete TSX component code as a string
- Escape quotes and newlines properly in JSON strings
- Use double quotes for JSON keys and string values
"""
    return prompt


def extract_components_from_response(response, components):
    """
    Extract individual component code from AI response.
    Handles various response formats and falls back gracefully.
    """
    response = response.strip()
    components_code = {}
    
    # Strategy 1: Try to find and parse JSON object
    start_idx = response.find('{')
    end_idx = response.rfind('}') + 1
    
    if start_idx >= 0 and end_idx > start_idx:
        try:
            json_str = response[start_idx:end_idx]
            parsed = json.loads(json_str)
            if isinstance(parsed, dict) and len(parsed) > 0:
                # Validate that we have the expected component IDs
                expected_ids = set(components.keys())
                found_ids = set(parsed.keys())
                if expected_ids.issubset(found_ids) or len(found_ids) > 0:
                    return parsed
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            # Try to fix common JSON issues
            try:
                # Remove markdown code blocks if present
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0]
                elif "```" in json_str:
                    json_str = json_str.split("```")[1].split("```")[0]
                parsed = json.loads(json_str.strip())
                if isinstance(parsed, dict):
                    return parsed
            except:
                pass
    
    # Strategy 2: Try to extract code blocks by component name
    for comp_id in components.keys():
        comp_name = to_pascal_case(comp_id)
        # Look for code blocks with component name
        patterns = [
            f"```tsx\n// {comp_name}",
            f"```tsx\n{comp_name}",
            f"```typescript\n{comp_name}",
            f"export default function {comp_name}",
            f"export function {comp_name}",
            f"const {comp_name} ="
        ]
        
        found = False
        for pattern in patterns:
            if pattern in response:
                # Extract code block
                start = response.find(pattern)
                if start >= 0:
                    # Find the end of the code block
                    if "```" in response[start:]:
                        code_start = response.find("```", start)
                        code_end = response.find("```", code_start + 3)
                        if code_end > code_start:
                            code = response[code_start + 3:code_end].strip()
                            if code.startswith("tsx\n") or code.startswith("typescript\n"):
                                code = code.split("\n", 1)[1]
                            components_code[comp_id] = code
                            found = True
                            break
                    else:
                        # No code block markers, try to extract function
                        end_markers = ["\n\n```", "\n\n##", "\n\n---", "\n\n#"]
                        for marker in end_markers:
                            end = response.find(marker, start)
                            if end > start:
                                code = response[start:end].strip()
                                components_code[comp_id] = code
                                found = True
                                break
                        if found:
                            break
        
        # Fallback: Generate a basic component
        if not found:
            comp_name = to_pascal_case(comp_id)
            spec = components.get(comp_id, {})
            props_list = spec.get("props", [])
            props_interface = ""
            props_params = ""
            if props_list:
                props_interface = f"interface {comp_name}Props {{\n  " + "\n  ".join([f"{prop}: string" for prop in props_list]) + "\n}"
                props_params = f"{{ {', '.join(props_list)} }}: {comp_name}Props"
            
            fallback_code = f"""{props_interface if props_interface else ""}
export default function {comp_name}({props_params if props_params else ""}) {{
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold">{comp_name}</h2>
      <p className="text-muted-foreground">{spec.get('usage', 'Component placeholder')}</p>
    </div>
  )
}}"""
            components_code[comp_id] = fallback_code
    
    return components_code


def assemble_page_with_types(page_route, components):
    """Assemble page.tsx with proper TypeScript types and imports."""
    page_folder = get_page_folder(page_route)
    
    import_lines = []
    jsx_lines = []
    
    for comp_id in components.keys():
        comp_name = to_pascal_case(comp_id)
        # Use @/ alias for imports
        import_path = f"@/{page_folder}/components/{comp_name}"
        import_lines.append(f"import {comp_name} from '{import_path}'")
        jsx_lines.append(f"      <{comp_name} />")
    
    page_code = f"""{chr(10).join(import_lines)}

export default function Page() {{
  return (
    <div className="min-h-screen">
{chr(10).join(jsx_lines)}
    </div>
  )
}}
"""
    return page_code


def get_page_folder(page_route):
    """Get the folder path for a page route."""
    if page_route == "/":
        return "app"
    # Remove leading slash and use as folder name
    route_path = page_route.lstrip("/")
    return f"app/{route_path}"


def to_pascal_case(s):
    """Convert kebab-case or snake_case to PascalCase."""
    # Handle both - and _ separators
    words = s.replace("_", "-").split("-")
    return "".join(word.capitalize() for word in words if word)


def generate_shadcn_components(files):
    """Generate basic shadcn/ui components that are commonly used."""
    # Button component
    files["components/ui/button.tsx"] = """import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
"""
    
    # Card component
    files["components/ui/card.tsx"] = """import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
"""
    
    # Input component
    files["components/ui/input.tsx"] = """import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
"""


def clean_code(code):
    """Clean up generated code by removing markdown code blocks."""
    if not code:
        return ""
    
    code = code.strip()
    
    # Remove markdown code blocks
    if code.startswith("```tsx"):
        code = code[6:]
    elif code.startswith("```typescript"):
        code = code[13:]
    elif code.startswith("```"):
        code = code[3:]
    
    if code.endswith("```"):
        code = code[:-3]
    
    return code.strip()
