"""
templates.py — Fixed-coordinate diagram templates.

Each template function receives a data dict (from YAML) and an svg list,
draws all symbols and signal lines at hardcoded positions, and returns nothing.

Canvas width x height is defined per template.

Data dict keys vary by template — see YAML schema in each docstring.
"""

from symbols import (
    field_transmitter, dcs_controller, function_block, selector_block,
    valve, signal_line, arrowhead, junction_dot, signal_label,
    range_label_vertical
)


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE LOOP
# ─────────────────────────────────────────────────────────────────────────────
# YAML schema:
#   template: single_loop
#   transmitter: {tag: FT-401}
#   controller:  {tag: FC-401, action: REVERSE ACTION}
#   valve:       {tag: FV-401, failure: AO/AFC}
#
# Layout (left → right):
#   Transmitter(100,120) → Controller(260,120) → Valve(430,120)
#
CANVAS_SINGLE = (560, 240)

def draw_single_loop(data, svg):
    tx = data["transmitter"]
    ct = data["controller"]
    vl = data["valve"]

    # positions
    TX = (100, 120)
    CT = (270, 120)
    VL = (440, 120)

    # transmitter
    field_transmitter(svg, *TX, tx["tag"])

    # signal line TX → CT  (dashed, with arrowhead)
    # TX right edge at (118, 120), CT left edge at (248, 120)
    signal_line(svg, [(TX[0]+18, TX[1]), (CT[0]-22, CT[1])])
    arrowhead(svg, CT[0]-22, CT[1], "right")
    signal_label(svg, (TX[0]+18 + CT[0]-22)//2, TX[1]-5, "PV")

    # controller
    dcs_controller(svg, *CT, ct["tag"], action=ct.get("action", "REVERSE ACTION"))

    # signal line CT → VL
    signal_line(svg, [(CT[0]+22, CT[1]), (VL[0]-14, VL[1])])
    arrowhead(svg, VL[0]-14, VL[1], "right")
    signal_label(svg, (CT[0]+22 + VL[0]-14)//2, CT[1]-5, "OP")

    # valve
    valve(svg, *VL, vl["tag"], vl.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# CASCADE
# ─────────────────────────────────────────────────────────────────────────────
# YAML schema:
#   template: cascade
#   primary_transmitter:   {tag: PT-401}
#   primary_controller:    {tag: PC-401, action: REVERSE ACTION}
#   secondary_transmitter: {tag: FT-401}
#   secondary_controller:  {tag: FC-401, action: REVERSE ACTION}
#   valve:                 {tag: FV-401, failure: AO/AFC}
#
# Layout:
#   Primary TX(100,80) → Primary CT(260,80) --SP--> Secondary CT(420,120)
#                                                         ↑
#   Secondary TX(100,160) → Secondary CT(420,160)
#   Secondary CT → Valve(580,160)
#
CANVAS_CASCADE = (720, 280)

def draw_cascade(data, svg):
    ptx = data["primary_transmitter"]
    pct = data["primary_controller"]
    stx = data["secondary_transmitter"]
    sct = data["secondary_controller"]
    vl  = data["valve"]

    PTX = (100, 90)
    PCT = (270, 90)
    STX = (100, 190)
    SCT = (450, 190)
    VL  = (610, 190)

    # primary transmitter
    field_transmitter(svg, *PTX, ptx["tag"])
    signal_line(svg, [(PTX[0]+18, PTX[1]), (PCT[0]-22, PTX[1])])
    arrowhead(svg, PCT[0]-22, PTX[1], "right")
    signal_label(svg, (PTX[0]+18 + PCT[0]-22)//2, PTX[1]-5, "PV")

    # primary controller
    dcs_controller(svg, *PCT, pct["tag"], action=pct.get("action", "REVERSE ACTION"))

    # SP line: PCT right → drop down → SCT top (SP input)
    # PCT right edge (292, 90) → (370, 90) → (370, 168) → SCT top (450, 168)
    sp_x = 370
    signal_line(svg, [(PCT[0]+22, PCT[1]), (sp_x, PCT[1]), (sp_x, SCT[1]-22), (SCT[0], SCT[1]-22)])
    arrowhead(svg, SCT[0], SCT[1]-22, "down")
    signal_label(svg, sp_x + 8, (PCT[1] + SCT[1])//2, "SP", anchor="left")

    # secondary transmitter
    field_transmitter(svg, *STX, stx["tag"])
    signal_line(svg, [(STX[0]+18, STX[1]), (SCT[0]-22, STX[1])])
    arrowhead(svg, SCT[0]-22, STX[1], "right")
    signal_label(svg, (STX[0]+18 + SCT[0]-22)//2, STX[1]-5, "PV")

    # secondary controller
    dcs_controller(svg, *SCT, sct["tag"], action=sct.get("action", "REVERSE ACTION"))

    # SCT → valve
    signal_line(svg, [(SCT[0]+22, SCT[1]), (VL[0]-14, SCT[1])])
    arrowhead(svg, VL[0]-14, SCT[1], "right")
    signal_label(svg, (SCT[0]+22 + VL[0]-14)//2, SCT[1]-5, "OP")

    valve(svg, *VL, vl["tag"], vl.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# SPLIT RANGE (two controllers, one transmitter — as in Image 1)
# ─────────────────────────────────────────────────────────────────────────────
# YAML schema:
#   template: split_range_dual
#   transmitter:  {tag: PT-001}
#   controller_a: {tag: PC-001A, action: REVERSE ACTION}
#   controller_b: {tag: PC-001B, action: DIRECT ACTION}
#   valve_a:      {tag: PV-001A, failure: AO/AFC}
#   valve_b:      {tag: PV-0001B, failure: AO/AFC}
#
# Layout (Image 1 pattern):
#   TX left → horizontal line splits up to CT_B and down to CT_A
#   Each CT → its own valve to the right
#
CANVAS_SPLIT_DUAL = (620, 380)

def draw_split_range_dual(data, svg):
    tx  = data["transmitter"]
    cta = data["controller_a"]
    ctb = data["controller_b"]
    vla = data["valve_a"]
    vlb = data["valve_b"]

    TX  = (100, 190)   # center vertically
    CTA = (300, 280)   # lower controller (A = REVERSE)
    CTB = (300, 100)   # upper controller (B = DIRECT)
    VLA = (480, 280)
    VLB = (480, 100)

    # transmitter
    field_transmitter(svg, *TX, tx["tag"])

    # TX right → branch point
    branch_x = 190
    signal_line(svg, [(TX[0]+18, TX[1]), (branch_x, TX[1])])
    arrowhead(svg, branch_x, TX[1], "right")

    # branch point junction
    junction_dot(svg, branch_x, TX[1])

    # branch up to CTB
    signal_line(svg, [(branch_x, TX[1]), (branch_x, CTB[1]), (CTB[0]-22, CTB[1])])
    arrowhead(svg, CTB[0]-22, CTB[1], "right")
    signal_label(svg, branch_x - 14, (TX[1] + CTB[1])//2, "PV", anchor="right")

    # branch down to CTA
    signal_line(svg, [(branch_x, TX[1]), (branch_x, CTA[1]), (CTA[0]-22, CTA[1])])
    arrowhead(svg, CTA[0]-22, CTA[1], "right")
    signal_label(svg, branch_x - 14, (TX[1] + CTA[1])//2, "PV", anchor="right")

    # controllers
    dcs_controller(svg, *CTB, ctb["tag"], action=ctb.get("action", "DIRECT ACTION"))
    dcs_controller(svg, *CTA, cta["tag"], action=cta.get("action", "REVERSE ACTION"))

    # CTB → VLB
    signal_line(svg, [(CTB[0]+22, CTB[1]), (VLB[0]-14, CTB[1])])
    arrowhead(svg, VLB[0]-14, CTB[1], "right")
    signal_label(svg, (CTB[0]+22 + VLB[0]-14)//2, CTB[1]-5, "OP")

    # CTA → VLA
    signal_line(svg, [(CTA[0]+22, CTA[1]), (VLA[0]-14, CTA[1])])
    arrowhead(svg, VLA[0]-14, CTA[1], "right")
    signal_label(svg, (CTA[0]+22 + VLA[0]-14)//2, CTA[1]-5, "OP")

    # valves
    valve(svg, *VLB, vlb["tag"], vlb.get("failure", "AO/AFC"))
    valve(svg, *VLA, vla["tag"], vla.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# SPLIT RANGE WITH ARTHC FUNCTION BLOCKS (Image 2 / Image 3 pattern)
# ─────────────────────────────────────────────────────────────────────────────
# YAML schema:
#   template: split_range_arthc
#   transmitter:  {tag: PT-001}
#   controller:   {tag: PC-001, action: DIRECT ACTION}
#   block_a:      {tag: PY-001A, func: ARTHC, range_in: "0%-50%",  range_out: "100%-0%"}
#   block_b:      {tag: PY-001B, func: ARTHC, range_in: "50%-100%", range_out: "0%-100%"}
#   valve_a:      {tag: PV-001A, failure: AO/AFC}
#   valve_b:      {tag: PV-0001B, failure: AO/AFC}
#
# Layout (Image 2):
#   TX → CT → OP line splits → PY_B (upper) and PY_A (lower)
#   Range labels on split lines, output lines to valves
#
CANVAS_SPLIT_ARTHC = (720, 420)

def draw_split_range_arthc(data, svg):
    tx  = data["transmitter"]
    ct  = data["controller"]
    bla = data["block_a"]
    blb = data["block_b"]
    vla = data["valve_a"]
    vlb = data["valve_b"]

    TX  = (80,  210)
    CT  = (230, 210)
    BLB = (430, 110)   # upper block (B)
    BLA = (430, 310)   # lower block (A)
    VLB = (610, 110)
    VLA = (610, 310)

    # transmitter
    field_transmitter(svg, *TX, tx["tag"])
    signal_line(svg, [(TX[0]+18, TX[1]), (CT[0]-22, TX[1])])
    arrowhead(svg, CT[0]-22, TX[1], "right")
    signal_label(svg, (TX[0]+18 + CT[0]-22)//2, TX[1]-5, "PV")

    # controller
    dcs_controller(svg, *CT, ct["tag"], action=ct.get("action", "DIRECT ACTION"))

    # OP line from CT to branch
    branch_x = 330
    signal_line(svg, [(CT[0]+22, CT[1]), (branch_x, CT[1])])
    signal_label(svg, CT[0]+30, CT[1]-5, "OP")
    junction_dot(svg, branch_x, CT[1])

    # branch up to BLB input
    range_in_b = blb.get("range_in", "50%-100%")
    signal_line(svg, [(branch_x, CT[1]), (branch_x, BLB[1]), (BLB[0]-22, BLB[1])])
    arrowhead(svg, BLB[0]-22, BLB[1], "right")
    range_label_vertical(svg, branch_x - 12, BLB[1], CT[1], range_in_b)
    signal_label(svg, BLB[0]-28, BLB[1]-5, "IN", anchor="right")

    # branch down to BLA input
    range_in_a = bla.get("range_in", "0%-50%")
    signal_line(svg, [(branch_x, CT[1]), (branch_x, BLA[1]), (BLA[0]-22, BLA[1])])
    arrowhead(svg, BLA[0]-22, BLA[1], "right")
    range_label_vertical(svg, branch_x - 12, CT[1], BLA[1], range_in_a)
    signal_label(svg, BLA[0]-28, BLA[1]-5, "IN", anchor="right")

    # function blocks
    function_block(svg, *BLB, blb["tag"], func_label=blb.get("func", "ARTHC"))
    function_block(svg, *BLA, bla["tag"], func_label=bla.get("func", "ARTHC"))

    # BLB → VLB
    range_out_b = blb.get("range_out", "0%-100%")
    signal_line(svg, [(BLB[0]+22, BLB[1]), (VLB[0]-14, BLB[1])])
    arrowhead(svg, VLB[0]-14, BLB[1], "right")
    signal_label(svg, BLB[0]+26, BLB[1]-5, "OP")
    signal_label(svg, (BLB[0]+22 + VLB[0]-14)//2, BLB[1]+12, range_out_b)

    # BLA → VLA
    range_out_a = bla.get("range_out", "100%-0%")
    signal_line(svg, [(BLA[0]+22, BLA[1]), (VLA[0]-14, BLA[1])])
    arrowhead(svg, VLA[0]-14, BLA[1], "right")
    signal_label(svg, BLA[0]+26, BLA[1]-5, "OP")
    signal_label(svg, (BLA[0]+22 + VLA[0]-14)//2, BLA[1]+12, range_out_a)

    # valves
    valve(svg, *VLB, vlb["tag"], vlb.get("failure", "AO/AFC"))
    valve(svg, *VLA, vla["tag"], vla.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# HIGH SELECTOR OVERRIDE (Image 4 top portion: PT → PC → PY[>] → valve)
# ─────────────────────────────────────────────────────────────────────────────
# YAML schema:
#   template: high_selector
#   transmitter_1: {tag: PT-001}
#   transmitter_2: {tag: PT-002}
#   controller_1:  {tag: PC-001, action: REVERSE ACTION}
#   selector:      {tag: PY-001, selector: ">"}
#   valve:         {tag: PV-001, failure: AC/AFO}
#
# Layout:
#   TX1 → CT1 (IN1) → PY[>] → valve
#   TX2 ──────────────────── (IN2) →/
#
CANVAS_HIGH_SEL = (700, 300)

def draw_high_selector(data, svg):
    tx1 = data["transmitter_1"]
    tx2 = data["transmitter_2"]
    ct1 = data["controller_1"]
    sel = data["selector"]
    vl  = data["valve"]

    TX1 = (80,  90)
    TX2 = (80,  210)
    CT1 = (240, 90)
    SEL = (430, 90)
    VL  = (590, 90)

    # TX1 → CT1
    field_transmitter(svg, *TX1, tx1["tag"])
    signal_line(svg, [(TX1[0]+18, TX1[1]), (CT1[0]-22, TX1[1])])
    arrowhead(svg, CT1[0]-22, TX1[1], "right")
    signal_label(svg, (TX1[0]+18 + CT1[0]-22)//2, TX1[1]-5, "PV")

    # CT1
    dcs_controller(svg, *CT1, ct1["tag"], action=ct1.get("action", "REVERSE ACTION"))

    # CT1 → SEL IN1
    signal_line(svg, [(CT1[0]+22, CT1[1]), (SEL[0]-22, CT1[1])])
    arrowhead(svg, SEL[0]-22, CT1[1], "right")
    signal_label(svg, CT1[0]+28, CT1[1]-5, "OP")
    signal_label(svg, SEL[0]-28, SEL[1]-5, "IN1", anchor="right")

    # TX2 → SEL IN2 (long horizontal line)
    field_transmitter(svg, *TX2, tx2["tag"])
    # TX2 right → right to x=SEL[0]+22 → up to SEL[1]+8 → left to SEL[0]+22 (IN2 on right side)
    signal_line(svg, [(TX2[0]+18, TX2[1]), (SEL[0]+22+20, TX2[1]), (SEL[0]+22+20, SEL[1]+8), (SEL[0]+22, SEL[1]+8)])
    arrowhead(svg, SEL[0]+22, SEL[1]+8, "left")
    signal_label(svg, SEL[0]+30, SEL[1]+8-5, "IN2", anchor="left")
    signal_label(svg, (TX2[0]+18 + SEL[0]+42)//2, TX2[1]-5, "PV")

    # selector block
    selector_block(svg, *SEL, sel["tag"], selector=sel.get("selector", ">"))

    # SEL → valve
    signal_line(svg, [(SEL[0]+22, SEL[1]), (VL[0]-14, SEL[1])])
    arrowhead(svg, VL[0]-14, SEL[1], "right")
    signal_label(svg, SEL[0]+28, SEL[1]-5, "OP")

    # valve
    valve(svg, *VL, vl["tag"], vl.get("failure", "AC/AFO"))


# ─────────────────────────────────────────────────────────────────────────────
# CASCADE WITH SPLIT-RANGE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
# Use case: Charge heater temperature control — TC (primary) cascades to FC
# (secondary), FC output splits via ARTHC to two fuel valves (main + pilot).
# Also applies to reboiler dual-fuel, cooler dual-stream, etc.
#
# YAML schema:
#   template: cascade_split_range
#   title: "NHT - Charge Heater Temperature Control TC-1101"
#   primary_transmitter:  {tag: TT-1101}
#   primary_controller:   {tag: TC-1101, action: REVERSE ACTION}
#   secondary_transmitter:{tag: FT-1101}
#   secondary_controller: {tag: FC-1101, action: REVERSE ACTION}
#   block_b:  {tag: FY-1101B, func: ARTHC, range_in: "50%-100%", range_out: "0%-100%"}
#   block_a:  {tag: FY-1101A, func: ARTHC, range_in: "0%-50%",  range_out: "100%-0%"}
#   valve_b:  {tag: FV-1101B, failure: AO/AFC}
#   valve_a:  {tag: FV-1101A, failure: AO/AFC}
#
CANVAS_CASCADE_SPLIT = (860, 460)

def draw_cascade_split_range(data, svg):
    ptx = data["primary_transmitter"]
    pct = data["primary_controller"]
    stx = data["secondary_transmitter"]
    sct = data["secondary_controller"]
    bla = data["block_a"]
    blb = data["block_b"]
    vla = data["valve_a"]
    vlb = data["valve_b"]

    PTX = (80,  100)
    PCT = (240, 100)
    STX = (80,  230)
    SCT = (420, 230)
    BLB = (620, 130)
    BLA = (620, 330)
    VLB = (790, 130)
    VLA = (790, 330)

    # primary transmitter → primary controller
    field_transmitter(svg, *PTX, ptx["tag"])
    signal_line(svg, [(PTX[0]+18, PTX[1]), (PCT[0]-22, PTX[1])])
    arrowhead(svg, PCT[0]-22, PTX[1], "right")
    signal_label(svg, (PTX[0]+18 + PCT[0]-22)//2, PTX[1]-5, "PV")
    dcs_controller(svg, *PCT, pct["tag"], action=pct.get("action", "REVERSE ACTION"))

    # SP line: PCT → drop down → SCT top
    sp_x = 330
    signal_line(svg, [(PCT[0]+22, PCT[1]), (sp_x, PCT[1]),
                      (sp_x, SCT[1]-22), (SCT[0], SCT[1]-22)])
    arrowhead(svg, SCT[0], SCT[1]-22, "down")
    signal_label(svg, sp_x + 8, (PCT[1] + SCT[1]-22)//2, "SP", anchor="left")

    # secondary transmitter → secondary controller
    field_transmitter(svg, *STX, stx["tag"])
    signal_line(svg, [(STX[0]+18, STX[1]), (SCT[0]-22, STX[1])])
    arrowhead(svg, SCT[0]-22, STX[1], "right")
    signal_label(svg, (STX[0]+18 + SCT[0]-22)//2, STX[1]-5, "PV")
    dcs_controller(svg, *SCT, sct["tag"], action=sct.get("action", "REVERSE ACTION"))

    # OP branch from SCT
    branch_x = 520
    signal_line(svg, [(SCT[0]+22, SCT[1]), (branch_x, SCT[1])])
    signal_label(svg, SCT[0]+28, SCT[1]-5, "OP")
    junction_dot(svg, branch_x, SCT[1])

    # branch up → BLB
    range_in_b = blb.get("range_in", "50%-100%")
    signal_line(svg, [(branch_x, SCT[1]), (branch_x, BLB[1]), (BLB[0]-22, BLB[1])])
    arrowhead(svg, BLB[0]-22, BLB[1], "right")
    range_label_vertical(svg, branch_x - 12, BLB[1], SCT[1], range_in_b)
    signal_label(svg, BLB[0]-28, BLB[1]-5, "IN", anchor="right")

    # branch down → BLA
    range_in_a = bla.get("range_in", "0%-50%")
    signal_line(svg, [(branch_x, SCT[1]), (branch_x, BLA[1]), (BLA[0]-22, BLA[1])])
    arrowhead(svg, BLA[0]-22, BLA[1], "right")
    range_label_vertical(svg, branch_x - 12, SCT[1], BLA[1], range_in_a)
    signal_label(svg, BLA[0]-28, BLA[1]-5, "IN", anchor="right")

    # function blocks
    function_block(svg, *BLB, blb["tag"], func_label=blb.get("func", "ARTHC"))
    function_block(svg, *BLA, bla["tag"], func_label=bla.get("func", "ARTHC"))

    # BLB → VLB
    signal_line(svg, [(BLB[0]+22, BLB[1]), (VLB[0]-14, BLB[1])])
    arrowhead(svg, VLB[0]-14, BLB[1], "right")
    signal_label(svg, BLB[0]+26, BLB[1]-5, "OP")
    signal_label(svg, (BLB[0]+22+VLB[0]-14)//2, BLB[1]+12, blb.get("range_out", "0%-100%"))

    # BLA → VLA
    signal_line(svg, [(BLA[0]+22, BLA[1]), (VLA[0]-14, BLA[1])])
    arrowhead(svg, VLA[0]-14, BLA[1], "right")
    signal_label(svg, BLA[0]+26, BLA[1]-5, "OP")
    signal_label(svg, (BLA[0]+22+VLA[0]-14)//2, BLA[1]+12, bla.get("range_out", "100%-0%"))

    valve(svg, *VLB, vlb["tag"], vlb.get("failure", "AO/AFC"))
    valve(svg, *VLA, vla["tag"], vla.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# OVERRIDE CONTROL (two controllers + selector → valve)
# ─────────────────────────────────────────────────────────────────────────────
# Use case: Compressor suction pressure control with discharge pressure override.
# Process controller (normal operation) and override/limit controller both feed
# a high or low selector — winner drives the valve directly or via flow cascade.
#
# YAML schema:
#   template: override
#   title: "NHT - Recycle Compressor Pressure Override PC-1401"
#   transmitter_normal:   {tag: PT-1401}
#   controller_normal:    {tag: PC-1401, action: DIRECT ACTION}
#   transmitter_override: {tag: PT-1402}
#   controller_override:  {tag: PC-1402, action: REVERSE ACTION}
#   selector:             {tag: PY-1401, selector: ">"}
#   valve:                {tag: PV-1401, failure: AC/AFO}
#
CANVAS_OVERRIDE = (700, 320)

def draw_override(data, svg):
    txn = data["transmitter_normal"]
    ctn = data["controller_normal"]
    txo = data["transmitter_override"]
    cto = data["controller_override"]
    sel = data["selector"]
    vl  = data["valve"]

    TXN = (80,  90)    # normal (process) transmitter
    CTN = (250, 90)    # normal controller
    TXO = (80,  230)   # override transmitter
    CTO = (250, 230)   # override controller
    SEL = (440, 160)   # selector block, centered between two controllers
    VL  = (600, 160)

    # normal path
    field_transmitter(svg, *TXN, txn["tag"])
    signal_line(svg, [(TXN[0]+18, TXN[1]), (CTN[0]-22, TXN[1])])
    arrowhead(svg, CTN[0]-22, TXN[1], "right")
    signal_label(svg, (TXN[0]+18+CTN[0]-22)//2, TXN[1]-5, "PV")
    dcs_controller(svg, *CTN, ctn["tag"], action=ctn.get("action", "DIRECT ACTION"))

    # override path
    field_transmitter(svg, *TXO, txo["tag"])
    signal_line(svg, [(TXO[0]+18, TXO[1]), (CTO[0]-22, TXO[1])])
    arrowhead(svg, CTO[0]-22, TXO[1], "right")
    signal_label(svg, (TXO[0]+18+CTO[0]-22)//2, TXO[1]-5, "PV")
    dcs_controller(svg, *CTO, cto["tag"], action=cto.get("action", "REVERSE ACTION"))

    # CTN OP → route to SEL IN1 (top input)
    mid_x = 355
    signal_line(svg, [(CTN[0]+22, CTN[1]), (mid_x, CTN[1]),
                      (mid_x, SEL[1]-10), (SEL[0]-22, SEL[1]-10)])
    arrowhead(svg, SEL[0]-22, SEL[1]-10, "right")
    signal_label(svg, CTN[0]+28, CTN[1]-5, "OP")
    signal_label(svg, SEL[0]-28, SEL[1]-14, "IN1", anchor="right")

    # CTO OP → route to SEL IN2 (bottom input)
    signal_line(svg, [(CTO[0]+22, CTO[1]), (mid_x, CTO[1]),
                      (mid_x, SEL[1]+10), (SEL[0]-22, SEL[1]+10)])
    arrowhead(svg, SEL[0]-22, SEL[1]+10, "right")
    signal_label(svg, CTO[0]+28, CTO[1]-5, "OP")
    signal_label(svg, SEL[0]-28, SEL[1]+14, "IN2", anchor="right")

    # selector
    selector_block(svg, *SEL, sel["tag"], selector=sel.get("selector", ">"))

    # SEL → valve
    signal_line(svg, [(SEL[0]+22, SEL[1]), (VL[0]-14, SEL[1])])
    arrowhead(svg, VL[0]-14, SEL[1], "right")
    signal_label(svg, SEL[0]+28, SEL[1]-5, "OP")

    valve(svg, *VL, vl["tag"], vl.get("failure", "AC/AFO"))


# ─────────────────────────────────────────────────────────────────────────────
# RATIO CONTROL
# ─────────────────────────────────────────────────────────────────────────────
# Use case: H2/HC ratio control in NHT reactor, fuel/air ratio for burners,
# or any loop where the setpoint of one flow controller tracks a fraction of
# another (wild) flow.
#
# Scheme: Wild flow (FT_wild) is measured and multiplied by ratio K inside
# FY (ratio computation block). FY output becomes SP of the ratio flow
# controller (FC). Controlled flow (FT_controlled) feeds FC as PV.
# FC drives the control valve.
#
# YAML schema:
#   template: ratio_control
#   title: "NHT - H2/HC Ratio Control FFC-1201"
#   transmitter_wild:       {tag: FT-1201}
#   ratio_block:            {tag: FY-1201, func: "RATIO"}
#   transmitter_controlled: {tag: FT-1202}
#   controller:             {tag: FFC-1201, action: REVERSE ACTION}
#   valve:                  {tag: FV-1201, failure: AO/AFC}
#
CANVAS_RATIO = (700, 320)

def draw_ratio_control(data, svg):
    txw = data["transmitter_wild"]
    ryb = data["ratio_block"]
    txc = data["transmitter_controlled"]
    ct  = data["controller"]
    vl  = data["valve"]

    TXW = (80,  90)    # wild flow transmitter
    RYB = (250, 90)    # ratio computation block
    TXC = (80,  230)   # controlled flow transmitter
    CT  = (450, 160)   # ratio flow controller
    VL  = (610, 160)

    # wild flow transmitter → ratio block
    field_transmitter(svg, *TXW, txw["tag"])
    signal_line(svg, [(TXW[0]+18, TXW[1]), (RYB[0]-22, TXW[1])])
    arrowhead(svg, RYB[0]-22, TXW[1], "right")
    signal_label(svg, (TXW[0]+18+RYB[0]-22)//2, TXW[1]-5, "PV")

    # ratio block (operator-set ratio K enters from top as SP)
    function_block(svg, *RYB, ryb["tag"], func_label=ryb.get("func", "RATIO"))
    # ratio setpoint input from top (operator)
    signal_line(svg, [(RYB[0], RYB[1]-22), (RYB[0], RYB[1]-40)])
    arrowhead(svg, RYB[0], RYB[1]-22, "down")
    signal_label(svg, RYB[0]+4, RYB[1]-44, "K (ratio SP)", anchor="left")

    # ratio block OP → route down → FC SP
    sp_drop_x = 360
    signal_line(svg, [(RYB[0]+22, RYB[1]), (sp_drop_x, RYB[1]),
                      (sp_drop_x, CT[1]-22), (CT[0], CT[1]-22)])
    arrowhead(svg, CT[0], CT[1]-22, "down")
    signal_label(svg, sp_drop_x+4, (RYB[1]+CT[1]-22)//2, "SP", anchor="left")

    # controlled flow transmitter → FC PV
    field_transmitter(svg, *TXC, txc["tag"])
    signal_line(svg, [(TXC[0]+18, TXC[1]), (CT[0]-22, TXC[1])])
    arrowhead(svg, CT[0]-22, TXC[1], "right")
    signal_label(svg, (TXC[0]+18+CT[0]-22)//2, TXC[1]-5, "PV")

    # FC PV comes in from left (controlled flow)
    # need to route TXC → up to CT[1] level → into CT left
    signal_line(svg, [(CT[0]-22, TXC[1]), (CT[0]-22, CT[1])])
    arrowhead(svg, CT[0]-22, CT[1], "right")

    # controller
    dcs_controller(svg, *CT, ct["tag"], action=ct.get("action", "REVERSE ACTION"))

    # FC → valve
    signal_line(svg, [(CT[0]+22, CT[1]), (VL[0]-14, CT[1])])
    arrowhead(svg, VL[0]-14, CT[1], "right")
    signal_label(svg, CT[0]+28, CT[1]-5, "OP")

    valve(svg, *VL, vl["tag"], vl.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# OVERRIDE CASCADE (selector output feeds a cascade flow controller)
# ─────────────────────────────────────────────────────────────────────────────
# Use case: Compressor suction pressure with anti-surge — two pressure
# controllers feed a selector, selector output is SP of a flow (recycle)
# controller that drives the recycle valve.
#
# YAML schema:
#   template: override_cascade
#   title: "NHT - Compressor Anti-Surge Override PC-1401/FC-1401"
#   transmitter_normal:   {tag: PT-1401}
#   controller_normal:    {tag: PC-1401, action: DIRECT ACTION}
#   transmitter_override: {tag: PT-1402}
#   controller_override:  {tag: PC-1402, action: REVERSE ACTION}
#   selector:             {tag: PY-1401, selector: ">"}
#   transmitter_flow:     {tag: FT-1401}
#   controller_flow:      {tag: FC-1401, action: REVERSE ACTION}
#   valve:                {tag: FV-1401, failure: AC/AFO}
#
CANVAS_OVERRIDE_CASCADE = (860, 360)

def draw_override_cascade(data, svg):
    txn = data["transmitter_normal"]
    ctn = data["controller_normal"]
    txo = data["transmitter_override"]
    cto = data["controller_override"]
    sel = data["selector"]
    txf = data["transmitter_flow"]
    ctf = data["controller_flow"]
    vl  = data["valve"]

    TXN = (80,  80)
    CTN = (240, 80)
    TXO = (80,  200)
    CTO = (240, 200)
    SEL = (420, 140)
    TXF = (80,  300)
    CTF = (600, 140)
    VL  = (760, 140)

    # normal pressure path
    field_transmitter(svg, *TXN, txn["tag"])
    signal_line(svg, [(TXN[0]+18, TXN[1]), (CTN[0]-22, TXN[1])])
    arrowhead(svg, CTN[0]-22, TXN[1], "right")
    signal_label(svg, (TXN[0]+18+CTN[0]-22)//2, TXN[1]-5, "PV")
    dcs_controller(svg, *CTN, ctn["tag"], action=ctn.get("action", "DIRECT ACTION"))

    # override pressure path
    field_transmitter(svg, *TXO, txo["tag"])
    signal_line(svg, [(TXO[0]+18, TXO[1]), (CTO[0]-22, TXO[1])])
    arrowhead(svg, CTO[0]-22, TXO[1], "right")
    signal_label(svg, (TXO[0]+18+CTO[0]-22)//2, TXO[1]-5, "PV")
    dcs_controller(svg, *CTO, cto["tag"], action=cto.get("action", "REVERSE ACTION"))

    # CTN OP → SEL IN1
    mid_x = 335
    signal_line(svg, [(CTN[0]+22, CTN[1]), (mid_x, CTN[1]),
                      (mid_x, SEL[1]-10), (SEL[0]-22, SEL[1]-10)])
    arrowhead(svg, SEL[0]-22, SEL[1]-10, "right")
    signal_label(svg, CTN[0]+28, CTN[1]-5, "OP")
    signal_label(svg, SEL[0]-28, SEL[1]-14, "IN1", anchor="right")

    # CTO OP → SEL IN2
    signal_line(svg, [(CTO[0]+22, CTO[1]), (mid_x, CTO[1]),
                      (mid_x, SEL[1]+10), (SEL[0]-22, SEL[1]+10)])
    arrowhead(svg, SEL[0]-22, SEL[1]+10, "right")
    signal_label(svg, CTO[0]+28, CTO[1]-5, "OP")
    signal_label(svg, SEL[0]-28, SEL[1]+14, "IN2", anchor="right")

    # selector
    selector_block(svg, *SEL, sel["tag"], selector=sel.get("selector", ">"))

    # SEL OP → CTF SP (top)
    signal_line(svg, [(SEL[0]+22, SEL[1]), (CTF[0], SEL[1]), (CTF[0], CTF[1]-22)])
    arrowhead(svg, CTF[0], CTF[1]-22, "down")
    signal_label(svg, (SEL[0]+22+CTF[0])//2, SEL[1]-5, "SP")

    # flow transmitter → CTF PV (left)
    field_transmitter(svg, *TXF, txf["tag"])
    signal_line(svg, [(TXF[0]+18, TXF[1]), (CTF[0]-22, TXF[1]),
                      (CTF[0]-22, CTF[1])])
    arrowhead(svg, CTF[0]-22, CTF[1], "right")
    signal_label(svg, (TXF[0]+18+CTF[0]-22)//2, TXF[1]-5, "PV")

    # flow controller
    dcs_controller(svg, *CTF, ctf["tag"], action=ctf.get("action", "REVERSE ACTION"))

    # CTF → valve
    signal_line(svg, [(CTF[0]+22, CTF[1]), (VL[0]-14, CTF[1])])
    arrowhead(svg, VL[0]-14, CTF[1], "right")
    signal_label(svg, CTF[0]+28, CTF[1]-5, "OP")

    valve(svg, *VL, vl["tag"], vl.get("failure", "AC/AFO"))


# ─────────────────────────────────────────────────────────────────────────────
# THREE-ELEMENT LEVEL CONTROL
# ─────────────────────────────────────────────────────────────────────────────
# Use case: Drum level control where level (LT), steam/outlet flow (FT_out),
# and feedwater/inlet flow (FT_in) are combined. LT drives LC, LC output is
# trimmed by the flow differential via a summing block (LY), LY output is SP
# to FC which controls the feed valve.
# Common in: knockout drums, stripper feed, heater coil protection.
#
# YAML schema:
#   template: three_element
#   title: "NHT - Stripper Feed Drum Level Control LC-1701"
#   transmitter_level:  {tag: LT-1701}
#   controller_level:   {tag: LC-1701, action: REVERSE ACTION}
#   transmitter_out:    {tag: FT-1701}
#   transmitter_in:     {tag: FT-1702}
#   summer_block:       {tag: LY-1701, func: "ARTH"}
#   controller_flow:    {tag: FC-1701, action: REVERSE ACTION}
#   valve:              {tag: LV-1701, failure: AO/AFC}
#
CANVAS_THREE_ELEMENT = (860, 380)

def draw_three_element(data, svg):
    txl = data["transmitter_level"]
    ctl = data["controller_level"]
    txo = data["transmitter_out"]
    txi = data["transmitter_in"]
    smb = data["summer_block"]
    ctf = data["controller_flow"]
    vl  = data["valve"]

    TXL = (80,  100)
    CTL = (240, 100)
    TXO = (80,  230)
    TXI = (80,  320)
    SMB = (430, 175)   # summer/arithmetic block
    CTF = (610, 175)
    VL  = (770, 175)

    # level transmitter → level controller
    field_transmitter(svg, *TXL, txl["tag"])
    signal_line(svg, [(TXL[0]+18, TXL[1]), (CTL[0]-22, TXL[1])])
    arrowhead(svg, CTL[0]-22, TXL[1], "right")
    signal_label(svg, (TXL[0]+18+CTL[0]-22)//2, TXL[1]-5, "PV")
    dcs_controller(svg, *CTL, ctl["tag"], action=ctl.get("action", "REVERSE ACTION"))

    # LC OP → summer IN1 (top)
    signal_line(svg, [(CTL[0]+22, CTL[1]), (SMB[0], CTL[1]), (SMB[0], SMB[1]-22)])
    arrowhead(svg, SMB[0], SMB[1]-22, "down")
    signal_label(svg, SMB[0]+4, (CTL[1]+SMB[1]-22)//2, "IN1", anchor="left")

    # outlet flow transmitter → summer IN2 (left)
    field_transmitter(svg, *TXO, txo["tag"])
    signal_line(svg, [(TXO[0]+18, TXO[1]), (SMB[0]-22, TXO[1])])
    arrowhead(svg, SMB[0]-22, TXO[1], "right")
    signal_label(svg, (TXO[0]+18+SMB[0]-22)//2, TXO[1]-5, "PV")

    # inlet flow transmitter → summer IN3 (bottom)
    field_transmitter(svg, *TXI, txi["tag"])
    signal_line(svg, [(TXI[0]+18, TXI[1]), (SMB[0], TXI[1]), (SMB[0], SMB[1]+22)])
    arrowhead(svg, SMB[0], SMB[1]+22, "up")
    signal_label(svg, TXI[0]+22, TXI[1]-5, "PV")
    signal_label(svg, SMB[0]+4, (TXI[1]+SMB[1]+22)//2, "IN3", anchor="left")

    # route TXO into summer left edge — summer left is SMB[0]-22
    # the TXO horizontal line already goes to SMB[0]-22 at TXO[1] y=230
    # need it to enter SMB at y=175 (center). Route: (SMB[0]-22, 230) up to (SMB[0]-22, 175)
    signal_line(svg, [(SMB[0]-22, TXO[1]), (SMB[0]-22, SMB[1])])
    arrowhead(svg, SMB[0]-22, SMB[1], "right")
    signal_label(svg, SMB[0]-28, (TXO[1]+SMB[1])//2, "IN2", anchor="right")

    # summer block
    function_block(svg, *SMB, smb["tag"], func_label=smb.get("func", "ARTH"))

    # summer OP → FC SP (top input)
    signal_line(svg, [(SMB[0]+22, SMB[1]), (CTF[0], SMB[1]), (CTF[0], CTF[1]-22)])
    arrowhead(svg, CTF[0], CTF[1]-22, "down")
    signal_label(svg, (SMB[0]+22+CTF[0])//2, SMB[1]-5, "SP")

    # no separate PV transmitter for FC — it receives from FT_in already piped in
    # show FC with PV coming from IN connection already routed
    dcs_controller(svg, *CTF, ctf["tag"], action=ctf.get("action", "REVERSE ACTION"))

    # FC → valve
    signal_line(svg, [(CTF[0]+22, CTF[1]), (VL[0]-14, CTF[1])])
    arrowhead(svg, VL[0]-14, CTF[1], "right")
    signal_label(svg, CTF[0]+28, CTF[1]-5, "OP")

    valve(svg, *VL, vl["tag"], vl.get("failure", "AO/AFC"))


# ─────────────────────────────────────────────────────────────────────────────
# DUAL LOOP AROUND VESSEL (level + pressure)
# ─────────────────────────────────────────────────────────────────────────────
# Use case: Separator / drum narrative figure — independent level outlet loop
# and pressure (vapor) loop drawn around one equipment tag.
#
# YAML schema:
#   template: dual_loop_vessel
#   title: "NHT - Separator 400-D-402 Level & Pressure Control"
#   vessel: {tag: "400-D-402", name: "SEPARATOR"}
#   level_transmitter:  {tag: LT-005}
#   level_controller:   {tag: LIC-005, action: DIRECT ACTION}
#   level_valve:        {tag: LV-005, failure: AO/AFC}
#   pressure_transmitter:{tag: PT-015}
#   pressure_controller: {tag: PIC-015, action: DIRECT ACTION}
#   pressure_valve:      {tag: PV-015, failure: AO/AFC}
#   local_gauge:         {tag: PG-029}          # optional
#   relief:              {tag: "PR", set: "27.5 kg/cm2g"}  # optional
#   feed_label:          "from products trim condenser"
#   gas_out_label:       "to recycle compressor suction"
#   liquid_out_label:    "to stripper feed"
#
CANVAS_DUAL_VESSEL = (900, 480)

def draw_dual_loop_vessel(data, svg):
    from symbols import FONT, FONT_SIZE_TAG, FONT_SIZE_LABEL, LINE_COLOR, STROKE_W

    ves = data["vessel"]
    ltx = data["level_transmitter"]
    lct = data["level_controller"]
    lvl = data["level_valve"]
    ptx = data["pressure_transmitter"]
    pct = data["pressure_controller"]
    pvl = data["pressure_valve"]
    pg  = data.get("local_gauge")
    pr  = data.get("relief")

    feed_lbl   = data.get("feed_label", "feed in (off-sheet)")
    gas_lbl    = data.get("gas_out_label", "gas out")
    liq_lbl    = data.get("liquid_out_label", "liquid out")

    # vessel box
    VX, VY = 310, 130
    VW, VH = 180, 200
    VCX = VX + VW // 2
    VCY = VY + VH // 2

    svg.append(
        f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" '
        f'fill="white" stroke="{LINE_COLOR}" stroke-width="{STROKE_W + 0.5}"/>'
    )
    svg.append(
        f'<text x="{VCX}" y="{VCY - 10}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_TAG}" font-weight="bold">'
        f'{ves["tag"]}</text>'
    )
    svg.append(
        f'<text x="{VCX}" y="{VCY + 8}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">'
        f'{ves.get("name", "VESSEL")}</text>'
    )

    # feed in (left process line)
    signal_line(svg, [(VX - 70, VCY), (VX, VCY)], dashed=False)
    arrowhead(svg, VX, VCY, "right")
    signal_label(svg, VX - 35, VCY - 8, feed_lbl)

    # gas out (top process line)
    signal_line(svg, [(VCX, VY), (VCX, VY - 40)], dashed=False)
    arrowhead(svg, VCX, VY - 40, "up")
    signal_label(svg, VCX + 6, VY - 34, gas_lbl, anchor="left")

    # liquid out stub (bottom-right of vessel → level valve path)
    liq_y = VY + VH
    signal_line(svg, [(VCX + 40, liq_y), (VCX + 40, liq_y + 30)], dashed=False)

    # ── Pressure loop (left / vapor) ──────────────────────────────────────
    PT = (100, 100)
    PC = (100, 200)
    PV = (100, 300)

    field_transmitter(svg, *PT, ptx["tag"])
    # process tap implied from vessel vapor → PT (horizontal process hint)
    signal_line(svg, [(VX, VY + 30), (PT[0] + 18 + 12, VY + 30), (PT[0] + 18 + 12, PT[1])], dashed=False)

    signal_line(svg, [(PT[0], PT[1] + 18), (PC[0], PC[1] - 22)])
    arrowhead(svg, PC[0], PC[1] - 22, "down")
    signal_label(svg, PT[0] + 10, (PT[1] + PC[1]) // 2, "PV", anchor="left")

    dcs_controller(svg, *PC, pct["tag"], action=pct.get("action", "DIRECT ACTION"))

    signal_line(svg, [(PC[0], PC[1] + 22), (PV[0], PV[1] - 26)])
    arrowhead(svg, PV[0], PV[1] - 26, "down")
    signal_label(svg, PC[0] + 10, (PC[1] + PV[1]) // 2, "OP", anchor="left")

    valve(svg, *PV, pvl["tag"], pvl.get("failure", "AO/AFC"))
    # PV on gas path: valve → up to gas header near vessel top
    signal_line(svg, [(PV[0] + 14, PV[1]), (180, PV[1]), (180, VY - 20), (VCX - 20, VY - 20)], dashed=False)
    arrowhead(svg, VCX - 20, VY - 20, "right")
    signal_label(svg, 200, VY - 28, "PV on gas out")

    # local gauge (optional) — right side of vessel vapor space
    if pg:
        PG = (VX + VW + 50, VY + 40)
        field_transmitter(svg, *PG, pg["tag"])
        signal_line(svg, [(VX + VW, PG[1]), (PG[0] - 18 - 12, PG[1])], dashed=False)

    # relief annotation (optional)
    if pr:
        pr_tag = pr.get("tag", "PR")
        pr_set = pr.get("set", "")
        svg.append(
            f'<text x="{VX - 8}" y="{VY + VH - 20}" text-anchor="end" '
            f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}" font-weight="bold">'
            f'{pr_tag}</text>'
        )
        svg.append(
            f'<text x="{VX - 8}" y="{VY + VH - 8}" text-anchor="end" '
            f'font-family="{FONT}" font-size="{FONT_SIZE_LABEL}">'
            f'set {pr_set}</text>'
        )
        signal_line(svg, [(VX - 4, VY + VH - 24), (VX, VY + VH - 24)], dashed=False)

    # ── Level loop (right / hydrocarbon liquid) ───────────────────────────
    LT = (560, 280)
    LC = (670, 280)
    LV = (780, 280)

    # process connection vessel → LT
    signal_line(svg, [(VX + VW, VCY + 40), (LT[0] - 18 - 12, VCY + 40), (LT[0] - 18 - 12, LT[1])], dashed=False)

    field_transmitter(svg, *LT, ltx["tag"])
    signal_line(svg, [(LT[0] + 18, LT[1]), (LC[0] - 22, LC[1])])
    arrowhead(svg, LC[0] - 22, LC[1], "right")
    signal_label(svg, (LT[0] + 18 + LC[0] - 22) // 2, LT[1] - 5, "PV")

    dcs_controller(svg, *LC, lct["tag"], action=lct.get("action", "DIRECT ACTION"))
    signal_line(svg, [(LC[0] + 22, LC[1]), (LV[0] - 14, LV[1])])
    arrowhead(svg, LV[0] - 14, LV[1], "right")
    signal_label(svg, (LC[0] + 22 + LV[0] - 14) // 2, LC[1] - 5, "OP")

    valve(svg, *LV, lvl["tag"], lvl.get("failure", "AO/AFC"))
    signal_label(svg, LV[0], LV[1] + 40, liq_lbl)


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATES = {
    "single_loop":          (CANVAS_SINGLE,          draw_single_loop),
    "cascade":              (CANVAS_CASCADE,          draw_cascade),
    "split_range_dual":     (CANVAS_SPLIT_DUAL,       draw_split_range_dual),
    "split_range_arthc":    (CANVAS_SPLIT_ARTHC,      draw_split_range_arthc),
    "high_selector":        (CANVAS_HIGH_SEL,         draw_high_selector),
    "cascade_split_range":  (CANVAS_CASCADE_SPLIT,    draw_cascade_split_range),
    "override":             (CANVAS_OVERRIDE,         draw_override),
    "override_cascade":     (CANVAS_OVERRIDE_CASCADE, draw_override_cascade),
    "ratio_control":        (CANVAS_RATIO,            draw_ratio_control),
    "three_element":        (CANVAS_THREE_ELEMENT,    draw_three_element),
    "dual_loop_vessel":     (CANVAS_DUAL_VESSEL,      draw_dual_loop_vessel),
}
