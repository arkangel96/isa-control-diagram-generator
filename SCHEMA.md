# Control Diagram Generator — YAML Schema Reference

## Usage

```
python draw.py input.yaml output.svg
```

Optional PNG conversion (requires cairosvg):
```
python -c "import cairosvg; cairosvg.svg2png(url='output.svg', write_to='output.png', scale=2)"
```

---

## Template: single_loop

One transmitter → one controller → one valve.

```yaml
template: single_loop
title: "NHT - Feed Flow Control FC-401"

transmitter:
  tag: FT-401

controller:
  tag: FC-401
  action: REVERSE ACTION       # or DIRECT ACTION

valve:
  tag: FV-401
  failure: AO/AFC              # AO/AFC, AC/AFO, AO/AFO, AC/AFC
```

---

## Template: cascade

Primary controller sets SP of secondary controller, secondary drives valve.

```yaml
template: cascade
title: "NHT - Stripper Level Cascade LC/FC"

primary_transmitter:
  tag: LT-1701

primary_controller:
  tag: LC-1701
  action: REVERSE ACTION

secondary_transmitter:
  tag: FT-1702

secondary_controller:
  tag: FC-1702
  action: REVERSE ACTION

valve:
  tag: FV-1702
  failure: AO/AFC
```

---

## Template: split_range_dual

One transmitter → two independent controllers (Image 1 style) → two valves.
Use when each controller has its own control action (one DIRECT, one REVERSE).

```yaml
template: split_range_dual
title: "NHT - Pressure Split-Range PC-001A/B"

transmitter:
  tag: PT-001

controller_b:
  tag: PC-001B
  action: DIRECT ACTION        # upper controller

controller_a:
  tag: PC-001A
  action: REVERSE ACTION       # lower controller

valve_b:
  tag: PV-001B
  failure: AO/AFC

valve_a:
  tag: PV-001A
  failure: AO/AFC
```

---

## Template: split_range_arthc

One transmitter → one controller → OP splits via ARTHC/AUTO-MAN function blocks → two valves.
Use for split-range with range scaling (Image 2/3 style).

```yaml
template: split_range_arthc
title: "NHT - Separator Pressure Split-Range PC-1301"

transmitter:
  tag: PT-1301

controller:
  tag: PC-1301
  action: DIRECT ACTION

block_b:                       # upper function block
  tag: PY-1301B
  func: ARTHC                  # or AUTO/MAN, ARTH
  range_in: "50%-100%"
  range_out: "0%-100%"

block_a:                       # lower function block
  tag: PY-1301A
  func: ARTHC
  range_in: "0%-50%"
  range_out: "100%-0%"

valve_b:
  tag: PV-1301B
  failure: AO/AFC

valve_a:
  tag: PV-1301A
  failure: AO/AFC
```

---

## Template: high_selector

Two transmitters, one controller with high-select override.

```yaml
template: high_selector
title: "NHT - Compressor Pressure Override"

transmitter_1:
  tag: PT-001

transmitter_2:
  tag: PT-002

controller_1:
  tag: PC-001
  action: REVERSE ACTION

selector:
  tag: PY-001
  selector: ">"                # ">" for high select, "<" for low select

valve:
  tag: PV-001
  failure: AC/AFO
```

---

## Failure Mode Codes

| Code   | Meaning                              |
|--------|--------------------------------------|
| AO/AFC | Air to Open / Air Fail Closed        |
| AC/AFO | Air to Close / Air Fail Open         |
| AO/AFO | Air to Open / Air Fail Open          |
| AC/AFC | Air to Close / Air Fail Closed       |

## Controller Action

- **REVERSE ACTION**: PV increases → Output decreases (e.g., flow control, level control discharging)
- **DIRECT ACTION**: PV increases → Output increases (e.g., pressure control venting, temperature control cooling)
