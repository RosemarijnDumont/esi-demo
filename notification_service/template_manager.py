
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Any
import os

# Configure Jinja2 environment to load templates from a 'templates' directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

async def render_template(template_name: str, data: Dict[str, Any]) -> str:
    """
    Renders a notification template with the provided data.
    """
    try:
        template = env.get_template(f"{template_name}.html") # Assuming HTML templates
        return template.render(data)
    except Exception as e:
        print(f"Error rendering template {template_name}: {e}")
        raise Exception(f"Template rendering failed: {str(e)}")
