"""
symbols.py — ISA 5.1 SVG drawing primitives
All coordinates are absolute (x, y). No layout logic here.
"""

FONT = "Arial, Helvetica, sans-serif"
FONT_SIZE_TAG = 9
FONT_SIZE_LABEL = 8
FONT_SIZE_RANGE = 7
LINE_COLOR = "#000000"
STROKE_W = 1.0
DASH = "4,3"


def _g(content):
    return content


def field_transmitter(svg, cx, cy, tag, show_tap=True):
    """
    Plain circle with process tap line at bottom.
    Represents a field-mounted transmitter (PT, TT, FT, LT, etc.)
    Diameter = 36px
    """
    r = 18
    lines = []
    lines.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    if show_tap:
        # horizontal process tap line on left
        lines.append(
            f'<line x1="{cx - r - 12}" y1="{cy}" x2="{cx - r}" y2="{cy}" '
            f'stroke="{LINE_COLOR}" stroke-width="{STROKE_W + 0.5}"/>'
        )
        # small vertical nub (process connection)
        lines.append(
            f'<line x1="{cx - r - 12}" y1="{cy - 5}" x2="{cx - r - 12}" y2="{cy + 5}" '
            f'stroke="{LINE_COLOR}" stroke-width="{STROKE_W + 0.5}"/>'
        )
    # tag text — two lines: letters then numbers
    letters = ''.join(c for c in tag if c.isalpha() or c == '-').split('-')[0] if '-' in tag else ''.join(c for c in tag if c.isalpha())
    numbers = tag[len(letters):].lstrip('-')
    lines.append(
        f'<text x="{cx}" y="{cy - 3}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">{letters}</text>'
    )
    lines.append(
        f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}">{numbers}</text>'
    )
    svg.extend(lines)


def dcs_controller(svg, cx, cy, tag, action=None):
    """
    Circle inside square with double horizontal line at bottom.
    ISA: shared display, operator-accessible (DCS controller/indicator).
    Box = 44x44, circle r=16.
    action: "DIRECT ACTION" or "REVERSE ACTION" — drawn above the box.
    """
    half = 22
    r = 16
    lines = []

    # action label above box
    if action:
        lines.append(
            f'<text x="{cx}" y="{cy - half - 8}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">{action.split()[0]}</text>'
        )
        lines.append(
            f'<text x="{cx}" y="{cy - half - 0}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">{action.split()[1] if len(action.split()) > 1 else ""}</text>'
        )

    # outer square
    lines.append(
        f'<rect x="{cx - half}" y="{cy - half}" width="{half*2}" height="{half*2}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # inner circle
    lines.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # double horizontal line at bottom of square (shared display marker)
    y_line1 = cy + half - 5
    y_line2 = cy + half - 2
    lines.append(
        f'<line x1="{cx - half}" y1="{y_line1}" x2="{cx + half}" y2="{y_line1}" '
        f'stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    lines.append(
        f'<line x1="{cx - half}" y1="{y_line2}" x2="{cx + half}" y2="{y_line2}" '
        f'stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # tag text
    letters = ''.join(c for c in tag if c.isalpha() or c == '-').split('-')[0] if '-' in tag else ''.join(c for c in tag if c.isalpha())
    numbers = tag[len(letters):].lstrip('-')
    lines.append(
        f'<text x="{cx}" y="{cy - 3}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">{letters}</text>'
    )
    lines.append(
        f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}">{numbers}</text>'
    )
    svg.extend(lines)


def function_block(svg, cx, cy, tag, func_label=None):
    """
    Circle inside square (no double line at bottom).
    Used for PY, TY, JY, TDI, JC function blocks.
    func_label: e.g. "ARTHC", "AUTO/MAN", "ARTH" — drawn above box.
    Box = 44x44, circle r=16.
    """
    half = 22
    r = 16
    lines = []

    if func_label:
        lines.append(
            f'<text x="{cx}" y="{cy - half - 4}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">{func_label}</text>'
        )

    lines.append(
        f'<rect x="{cx - half}" y="{cy - half}" width="{half*2}" height="{half*2}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    lines.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # tag text
    letters = ''.join(c for c in tag if c.isalpha() or c == '-').split('-')[0] if '-' in tag else ''.join(c for c in tag if c.isalpha())
    numbers = tag[len(letters):].lstrip('-')
    lines.append(
        f'<text x="{cx}" y="{cy - 3}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">{letters}</text>'
    )
    lines.append(
        f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}">{numbers}</text>'
    )
    svg.extend(lines)


def selector_block(svg, cx, cy, tag, selector=">"):
    """
    High/Low selector function block.
    Circle-in-square with selector symbol (> or <) in top-right corner.
    """
    half = 22
    r = 16
    lines = []
    lines.append(
        f'<rect x="{cx - half}" y="{cy - half}" width="{half*2}" height="{half*2}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    lines.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # selector symbol top-right
    lines.append(
        f'<text x="{cx + half - 4}" y="{cy - half + 9}" text-anchor="end" '
        f'font-family="{FONT}" font-size="10" font-weight="bold">{selector}</text>'
    )
    # tag
    letters = ''.join(c for c in tag if c.isalpha() or c == '-').split('-')[0] if '-' in tag else ''.join(c for c in tag if c.isalpha())
    numbers = tag[len(letters):].lstrip('-')
    lines.append(
        f'<text x="{cx}" y="{cy - 3}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">{letters}</text>'
    )
    lines.append(
        f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}">{numbers}</text>'
    )
    svg.extend(lines)


def valve(svg, cx, cy, tag, failure_mode):
    """
    Bow-tie valve body (two filled triangles meeting at a point),
    actuator dot on top, tag + failure mode below.
    Total height ~32px, width ~28px.
    """
    hw = 14   # half-width
    hh = 12   # half-height
    lines = []
    # left triangle (points right to center)
    lines.append(
        f'<polygon points="{cx - hw},{cy - hh} {cx},{cy} {cx - hw},{cy + hh}" '
        f'fill="black" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # right triangle (points left to center)
    lines.append(
        f'<polygon points="{cx + hw},{cy - hh} {cx},{cy} {cx + hw},{cy + hh}" '
        f'fill="black" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # actuator circle on top
    lines.append(
        f'<circle cx="{cx}" cy="{cy - hh - 5}" r="4" '
        f'fill="black" stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # stem line from actuator to body top
    lines.append(
        f'<line x1="{cx}" y1="{cy - hh - 1}" x2="{cx}" y2="{cy - hh}" '
        f'stroke="{LINE_COLOR}" stroke-width="{STROKE_W}"/>'
    )
    # tag below
    lines.append(
        f'<text x="{cx}" y="{cy + hh + 12}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">{tag}</text>'
    )
    lines.append(
        f'<text x="{cx}" y="{cy + hh + 22}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">{failure_mode}</text>'
    )
    svg.extend(lines)


def signal_line(svg, points, dashed=True):
    """
    Polyline signal path. points = list of (x, y) tuples.
    All segments must be orthogonal (horizontal or vertical only).
    """
    pts = " ".join(f"{x},{y}" for x, y in points)
    dash_attr = f'stroke-dasharray="{DASH}"' if dashed else ""
    svg.append(
        f'<polyline points="{pts}" fill="none" stroke="{LINE_COLOR}" '
        f'stroke-width="{STROKE_W}" {dash_attr}/>'
    )


def arrowhead(svg, x, y, direction="right"):
    """
    Filled triangle arrowhead.
    direction: "right", "left", "down", "up"
    """
    sz = 5
    if direction == "right":
        pts = f"{x},{y} {x - sz},{y - sz//2} {x - sz},{y + sz//2}"
    elif direction == "left":
        pts = f"{x},{y} {x + sz},{y - sz//2} {x + sz},{y + sz//2}"
    elif direction == "down":
        pts = f"{x},{y} {x - sz//2},{y - sz} {x + sz//2},{y - sz}"
    elif direction == "up":
        pts = f"{x},{y} {x - sz//2},{y + sz} {x + sz//2},{y + sz}"
    else:
        pts = f"{x},{y} {x - sz},{y - sz//2} {x - sz},{y + sz//2}"
    svg.append(f'<polygon points="{pts}" fill="{LINE_COLOR}"/>')


def junction_dot(svg, x, y):
    """Small filled circle at signal junction/branch point."""
    svg.append(
        f'<circle cx="{x}" cy="{y}" r="3" fill="{LINE_COLOR}"/>'
    )


def signal_label(svg, x, y, text, anchor="middle"):
    """Small label on a signal line (PV, OP, SP, IN, range, etc.)"""
    svg.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">{text}</text>'
    )


def range_label_vertical(svg, x, y1, y2, text):
    """Vertical range label alongside a vertical signal line."""
    mid_y = (y1 + y2) // 2
    svg.append(
        f'<text x="{x}" y="{mid_y}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_RANGE}" '
        f'transform="rotate(-90,{x},{mid_y})">{text}</text>'
    )
