# build.py
import markdown
import yaml
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PythonThemedSiteBuilder:
    """
    A simple static site generator for academic websites.
    Converts Markdown to HTML with a Python-inspired theme.
    """
    
    def __init__(self, content_dir="content", output_dir="docs", 
                 template_dir="templates", static_dir="static"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)
        self.static_dir = Path(static_dir)
        
        # Markdown extensions for academic content
        self.md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'attr_list',
        ])
        
        # Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def clean_output(self):
        """Remove previous build."""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
    
    def copy_static_files(self):
        """Copy static assets (CSS, images, etc.)."""
        static_output = self.output_dir / "static"
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, static_output)
            print(f"  Copied static files to {static_output}")
    
    def parse_markdown(self, filepath: Path) -> dict:
        """Parse a markdown file and return content + metadata."""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Manually parse YAML front matter for reliable multiline support
        meta = {}
        content = text
        
        if text.startswith('---'):
            # Find the closing ---
            end_index = text.find('---', 3)
            
            if end_index != -1:
                yaml_content = text[3:end_index].strip()
                content = text[end_index + 3:].strip()
                
                try:
                    meta = yaml.safe_load(yaml_content) or {}
                except yaml.YAMLError as e:
                    print(f"    Warning: YAML parsing error: {e}")
                    meta = {}
        
        # Convert markdown content to HTML
        self.md.reset()
        html_content = self.md.convert(content)

        return {
            'content': html_content,
            'meta': meta,
            'toc': getattr(self.md, 'toc', '')
        }
    
    def render_page(self, parsed_content: dict, template_name="base.html") -> str:
        """Render parsed content using Jinja2 template."""
        template = self.env.get_template(template_name)
        return template.render(
            content=parsed_content['content'],
            meta=parsed_content['meta'],
            toc=parsed_content['toc'],
            nav_items=self.get_nav_items()
        )
    
    def get_nav_items(self) -> list:
        """Generate navigation items from content files."""
        nav_order = ['index', 'research', 'publications', 'teaching', 'misc']
        nav_items = []
        
        for name in nav_order:
            filepath = self.content_dir / f"{name}.md"
            if filepath.exists():
                parsed = self.parse_markdown(filepath)
                title = parsed['meta'].get('title', name.capitalize())
                href = 'index.html' if name == 'index' else f'{name}.html'
                nav_items.append({'title': title, 'href': href})
        
        return nav_items
    
    def build(self):
        """Build the entire site."""
        print("🐍 Building Python-themed academic website...")
        print("=" * 50)
        
        self.clean_output()
        self.copy_static_files()
        
        # Process all markdown files
        for md_file in self.content_dir.glob("*.md"):
            print(f"  Processing {md_file.name}...")
            
            parsed = self.parse_markdown(md_file)
            html = self.render_page(parsed)
            
            output_file = self.output_dir / f"{md_file.stem}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"    → Generated {output_file.name}")
        
        print("=" * 50)
        print("✅ Build complete! Output in 'docs/' directory")


if __name__ == "__main__":
    builder = PythonThemedSiteBuilder()
    builder.build()