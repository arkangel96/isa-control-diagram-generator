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
    # Zone labels (FIELD / DCS / FIELD) — added at bottom-left of diagram
    zone_y = canvas_h - MARGIN - 18           # y of DCS/FIELD separator line
    zone_x1 = MARGIN // 2                      # left edge of border
    zone_x2 = canvas_w - MARGIN // 2           # right edge of border

    lines.append(
        f'<line x1="{zone_x1}" y1="{zone_y}" x2="{zone_x2}" y2="{zone_y}" '
        f'stroke="#555555" stroke-width="0.7" stroke-dasharray="5,3"/>')
    lines.append(
        f'<text x="{zone_x1 + 4}" y="{zone_y - 4}" '
        f'font-family="{TITLE_FONT}" font-size="9" fill="#444">DCS</text>')
    lines.append(
        f'<text x="{zone_x1 + 4}" y="{zone_y + 13}" '
        f'font-family="{TITLE_FONT}" font-size="9" fill="#444">FIELD</text>')
    # upper zone separator (FIELD transmitters above DCS controllers)
    upper_y = MARGIN + 18
    lines.append(
        f'<line x1="{zone_x1}" y1="{upper_y}" x2="{zone_x2}" y2="{upper_y}" '
        f'stroke="#555555" stroke-width="0.7" stroke-dasharray="5,3"/>')
    lines.append(
        f'<text x="{zone_x1 + 4}" y="{upper_y - 4}" '
        f'font-family="{TITLE_FONT}" font-size="9" fill="#444">FIELD</text>')
    lines.append(
        f'<text x="{zone_x1 + 4}" y="{upper_y + 13}" '
        f'font-family="{TITLE_FONT}" font-size="9" fill="#444">DCS</text>')



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
