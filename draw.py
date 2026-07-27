"""
draw.py — ISA Functional Control Diagram Generator
Usage: python draw.py input.yaml output.svg

Reads a YAML file describing a control loop, selects the matching template,
stamps all ISA symbols at fixed coordinates, and writes a clean SVG file.

No AI, no internet, no external dependencies beyond PyYAML.
Install: pip install pyyaml
"""

import sys
import os
import yaml
from templates import TEMPLATES


TITLE_FONT = "Arial, Helvetica, sans-serif"
BORDER_COLOR = "#000000"
MARGIN = 40  # border margin


def xml_escape(text):
    """Escape characters that break SVG/XML parsers (& < > ")."""
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_svg(canvas_w, canvas_h, draw_fn, data, title=None):
    """
    Build complete SVG document string.
    draw_fn populates a list of SVG element strings.
    """
    svg_elements = []

    # call template drawing function — populates svg_elements list
    draw_fn(data, svg_elements)

    # assemble full SVG
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{canvas_w}" height="{canvas_h}" '
                 f'viewBox="0 0 {canvas_w} {canvas_h}">')

    # white background
    lines.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="white"/>')

    # outer border
    lines.append(
        f'<rect x="{MARGIN//2}" y="{MARGIN//2}" '
        f'width="{canvas_w - MARGIN}" height="{canvas_h - MARGIN}" '
        f'fill="none" stroke="{BORDER_COLOR}" stroke-width="1"/>'
    )

    # title block at bottom
    if title:
        title_y = canvas_h - MARGIN//2 + 4
        lines.append(
            f'<text x="{canvas_w//2}" y="{title_y - 6}" '
            f'text-anchor="middle" font-family="{TITLE_FONT}" '
            f'font-size="9" font-weight="bold">{xml_escape(title)}</text>'
        )

    # diagram elements
    lines.extend(svg_elements)

    lines.append('</svg>')
    return "\n".join(lines)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(data):
    if "template" not in data:
        raise ValueError("YAML missing required key: 'template'")
    if data["template"] not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(
            f"Unknown template '{data['template']}'. "
            f"Available: {available}"
        )


def main():
    if len(sys.argv) < 3:
        print("Usage: python draw.py input.yaml output.svg")
        print()
        print("Available templates:")
        for name in TEMPLATES:
            print(f"  {name}")
        sys.exit(1)

    yaml_path = sys.argv[1]
    svg_path  = sys.argv[2]

    if not os.path.isfile(yaml_path):
        print(f"Error: file not found: {yaml_path}")
        sys.exit(1)

    data = load_yaml(yaml_path)
    validate(data)

    template_name = data["template"]
    canvas, draw_fn = TEMPLATES[template_name]
    canvas_w, canvas_h = canvas

    title = data.get("title", None)

    svg_content = build_svg(canvas_w, canvas_h, draw_fn, data, title=title)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Done: {svg_path}  ({canvas_w}x{canvas_h}px, template={template_name})")


if __name__ == "__main__":
    main()
