from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy


DARK_BLUE   = RGBColor(0x0D, 0x1B, 0x2A)   # background / title bg
MID_BLUE    = RGBColor(0x1B, 0x48, 0x8B)   # accent bar
ACCENT_BLUE = RGBColor(0x26, 0x8B, 0xD2)   # highlights
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xEC, 0xEF, 0xF4)
YELLOW      = RGBColor(0xFF, 0xD1, 0x66)
GREEN       = RGBColor(0x2E, 0xCC, 0x71)
RED_SOFT    = RGBColor(0xE7, 0x4C, 0x3C)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # completely blank layout


def add_rect(slide, left, top, width, height, fill_color, transparency=0):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    shape.line.fill.background()
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = fill_color
    return shape


def add_text_box(slide, text, left, top, width, height,
                 font_size=18, bold=False, color=WHITE,
                 align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size   = Pt(font_size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_multiline(slide, lines, left, top, width, height,
                  base_size=14, color=WHITE, bold_first=False):
    """Add multiple paragraphs inside one text box."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        if isinstance(line, tuple):
            run.text, size, bold, col = line
            run.font.size  = Pt(size)
            run.font.bold  = bold
            run.font.color.rgb = col
        else:
            run.text = line
            run.font.size  = Pt(base_size)
            run.font.bold  = bold_first and first
            run.font.color.rgb = color
    return txBox


def slide_chrome(slide, section_tag=""):
    """Draw the common background + top bar + bottom bar."""
    # Full background
    add_rect(slide, 0, 0, 13.33, 7.5, DARK_BLUE)
    # Top accent bar
    add_rect(slide, 0, 0, 13.33, 0.12, ACCENT_BLUE)
    # Bottom bar
    add_rect(slide, 0, 7.25, 13.33, 0.25, MID_BLUE)
    # Section tag bottom-right
    if section_tag:
        add_text_box(slide, section_tag, 10.5, 7.22, 2.7, 0.28,
                     font_size=9, color=LIGHT_GRAY, align=PP_ALIGN.RIGHT)


def slide_title_bar(slide, title_text, subtitle_text=""):
    """Blue title rectangle near top."""
    add_rect(slide, 0.4, 0.18, 12.53, 0.95, MID_BLUE)
    add_text_box(slide, title_text, 0.55, 0.2, 12.2, 0.9,
                 font_size=28, bold=True, color=WHITE)
    if subtitle_text:
        add_text_box(slide, subtitle_text, 0.55, 1.1, 12.2, 0.4,
                     font_size=15, color=ACCENT_BLUE, bold=False)

slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(slide, 0, 0,  13.33, 0.15, ACCENT_BLUE)
add_rect(slide, 0, 7.35, 13.33, 0.15, ACCENT_BLUE)
# Centre decorative box
add_rect(slide, 1.5, 1.5, 10.33, 4.5, MID_BLUE)
add_rect(slide, 1.55, 1.55, 10.23, 0.08, ACCENT_BLUE)

add_text_box(slide, "Advanced Normalization Concepts",
             1.7, 1.7, 9.9, 1.2,
             font_size=38, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text_box(slide, "Deepening Understanding of Normalization Rules",
             1.7, 2.85, 9.9, 0.6,
             font_size=20, bold=False, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)

add_rect(slide, 3.5, 3.55, 6.33, 0.05, ACCENT_BLUE)

add_text_box(slide, "Advanced System Design and Implementation",
             1.7, 3.7, 9.9, 0.5,
             font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide, "April 2026",
             1.7, 4.25, 9.9, 0.4,
             font_size=14, color=YELLOW, align=PP_ALIGN.CENTER)

slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "Overview")
slide_title_bar(slide, "What We'll Cover Today")

topics = [
    "  📌  Quick Recap: 1NF and 2NF",
    "",
    "  📌  B. Normal Forms (Part 2)",
    "         •  Third Normal Form (3NF)",
    "         •  Boyce-Codd Normal Form (BCNF)",
    "         •  Overview of 4NF and 5NF",
    "",
    "  📌  C. Functional Dependencies (Continuation)",
    "         •  Determinants and Dependent Attributes",
    "         •  Identifying Functional Dependencies in Tables",
    "",
    "  📌  D. Steps in the Normalization Process",
    "         •  Converting Unnormalized Data to Normalized Tables",
    "         •  Decomposition Techniques",
]
lines = []
for t in topics:
    lines.append((t, 15, "📌" in t, WHITE))
add_multiline(slide, lines, 0.6, 1.3, 12.1, 5.8, base_size=15)

# Notes
notes_slide = slide.notes_slide
notes_slide.notes_text_frame.text = (
    "Begin by briefly orienting students to where they are in the course. "
    "Emphasize that today's lecture builds directly on 1NF and 2NF. "
    "Remind students that normalization directly prevents data anomalies in "
    "real-world databases. Encourage them to think of each normal form as a "
    "progressively stricter rule that removes a specific type of redundancy."
)


slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "Recap")
slide_title_bar(slide, "Where We Left Off — 1NF and 2NF")

# 1NF box
add_rect(slide, 0.4, 1.35, 5.9, 2.1, MID_BLUE)
add_text_box(slide, "First Normal Form (1NF)", 0.5, 1.38, 5.7, 0.45,
             font_size=16, bold=True, color=YELLOW)
nf1 = [
    "  •  All attributes contain atomic (indivisible) values",
    "  •  No repeating groups or arrays",
    "  •  Each record is unique",
]
add_multiline(slide, [(t, 13, False, WHITE) for t in nf1],
              0.5, 1.82, 5.7, 1.6)

# 2NF box
add_rect(slide, 6.9, 1.35, 5.9, 2.1, MID_BLUE)
add_text_box(slide, "Second Normal Form (2NF)", 7.0, 1.38, 5.7, 0.45,
             font_size=16, bold=True, color=YELLOW)
nf2 = [
    "  •  Must already be in 1NF",
    "  •  Every non-key attribute must be FULLY",
    "      functionally dependent on the entire PK",
    "  •  Eliminates partial dependencies",
]
add_multiline(slide, [(t, 13, False, WHITE) for t in nf2],
              7.0, 1.82, 5.7, 1.6)

# Example
add_text_box(slide, "Example of Partial Dependency (Violates 2NF):",
             0.4, 3.6, 12.5, 0.38, font_size=13, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 3.98, 12.5, 1.6, RGBColor(0x10, 0x25, 0x40))
tbl_text = (
    "  OrderID  |  ProductID  |  ProductName  |  Quantity\n"
    "  ─────────────────────────────────────────────────────\n"
    "    101     |    P01      |    Laptop     |     2\n"
    "    101     |    P02      |    Mouse      |     5\n\n"
    "  ⚠  ProductName depends only on ProductID → partial dependency!"
)
add_text_box(slide, tbl_text, 0.55, 4.02, 12.2, 1.5,
             font_size=12, color=LIGHT_GRAY)

slide.notes_slide.notes_text_frame.text = (
    "This slide is a bridge. Spend only 3-4 minutes here. "
    "Remind students that 1NF removes multi-valued cells and 2NF removes "
    "partial dependencies. Lead into: even after 2NF, transitive dependencies "
    "can still exist — which is exactly what 3NF addresses."
)

# ═══════════════════════════════════════════════════════════════
#  SLIDE 4 — 3NF (DEFINITION + EXAMPLE)
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Third Normal Form (3NF) — Definition & Transitive Dependencies")


add_rect(slide, 0.4, 1.32, 12.5, 0.95, MID_BLUE)
add_text_box(slide, "Definition", 0.55, 1.35, 4.0, 0.32,
             font_size=14, bold=True, color=YELLOW)
defn = ("In 3NF: (1) Must be in 2NF, AND (2) Every non-key attribute is NON-TRANSITIVELY "
        "dependent on the PK.\n"
        "Mnemonic: '...the KEY, the WHOLE KEY, and NOTHING BUT THE KEY.'")
add_text_box(slide, defn, 0.55, 1.67, 12.2, 0.58, font_size=13, color=WHITE)

add_text_box(slide,
             "Transitive Dependency: If  A → B  and  B → C,  then  A → C  is TRANSITIVE.",
             0.4, 2.32, 12.5, 0.32, font_size=13, bold=True, color=ACCENT_BLUE)

add_text_box(slide, "Violating Table:", 0.4, 2.68, 5.0, 0.3,
             font_size=12, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 2.98, 12.5, 0.75, RGBColor(0x10, 0x25, 0x40))
tbl = ("  StudentID  |  StudentName  |  DeptID  |  DeptName\n"
       "  ──────────────────────────────────────────────────────\n"
       "    S001      |    Alice      |   D01    |  Computer Science")
add_text_box(slide, tbl, 0.55, 3.0, 12.2, 0.7, font_size=11, color=LIGHT_GRAY)

fds = [
    ("  StudentID  →  DeptID          ✅  direct", 12, False, WHITE),
    ("  DeptID     →  DeptName        ✅  direct", 12, False, WHITE),
    ("  StudentID  →  DeptName        ❌  TRANSITIVE DEPENDENCY!", 12, True, YELLOW),
]
add_multiline(slide, fds, 0.4, 3.82, 8.5, 0.85)

add_rect(slide, 8.9, 3.82, 4.0, 0.85, RGBColor(0x40, 0x10, 0x10))
add_text_box(slide, "Anomalies:", 9.0, 3.84, 3.8, 0.28,
             font_size=12, bold=True, color=RED_SOFT)
add_multiline(slide, [
    ("  ⚠  Update Anomaly", 11, False, WHITE),
    ("  ⚠  Deletion Anomaly", 11, False, WHITE),
    ("  ⚠  Insertion Anomaly", 11, False, WHITE),
], 9.0, 4.12, 3.8, 0.52)

add_text_box(slide, "✅  Solution — Decompose into 2 tables:",
             0.4, 4.76, 8.0, 0.3, font_size=12, bold=True, color=GREEN)
add_rect(slide, 0.4, 5.08, 5.8, 0.58, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "Student Table:  StudentID | StudentName | DeptID",
             0.55, 5.1, 5.6, 0.5, font_size=11, color=WHITE)
add_rect(slide, 7.1, 5.08, 5.8, 0.58, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "Department Table:  DeptID | DeptName",
             7.25, 5.1, 5.6, 0.5, font_size=11, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "The 'nothing but the key' mnemonic covers all three normal forms: "
    "1NF=the key, 2NF=the whole key, 3NF=nothing but the key. "
    "Walk through each anomaly — losing ALL dept info because the last student was deleted "
    "is the most striking example. After decomposition, DeptName lives in exactly one place."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 5 — BCNF (DEFINITION + EXAMPLE + COMPARISON)
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Boyce-Codd Normal Form (BCNF) — A Stronger 3NF")

add_rect(slide, 0.4, 1.32, 12.5, 0.72, MID_BLUE)
add_text_box(slide,
             "BCNF: For every FD  X → Y,  X must be a SUPERKEY.  "
             "BCNF closes the 3NF loophole where a prime attribute depends on a non-superkey.",
             0.55, 1.34, 12.2, 0.68, font_size=13, color=WHITE)

add_text_box(slide, "Example — Enrollment Table:",
             0.4, 2.1, 6.0, 0.3, font_size=13, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 2.4, 6.2, 0.85, RGBColor(0x10, 0x25, 0x40))
tbl = ("  StudentID  |  Course    |  Professor\n"
       "  ─────────────────────────────────────────\n"
       "    S001      |  DBMS      |  Dr. Smith")
add_text_box(slide, tbl, 0.55, 2.42, 6.0, 0.8, font_size=11, color=WHITE)

add_text_box(slide, "Functional Dependencies:",
             6.85, 2.1, 5.8, 0.3, font_size=13, bold=True, color=ACCENT_BLUE)
fds = [
    ("  {StudentID, Course} →  Professor  (composite PK)", 11, False, WHITE),
    ("  {StudentID, Prof}   →  Course     (candidate key)", 11, False, WHITE),
    ("  Professor           →  Course     ⚠ BCNF Violation!", 11, True, YELLOW),
]
add_multiline(slide, fds, 6.85, 2.4, 5.8, 0.85)

add_rect(slide, 0.4, 3.32, 12.5, 0.55, RGBColor(0x40, 0x28, 0x00))
add_text_box(slide,
             "⚠  Professor → Course holds but Professor is NOT a superkey. "
             "It IS in 3NF (Professor is prime) but FAILS BCNF.",
             0.55, 3.35, 12.2, 0.5, font_size=12, bold=True, color=YELLOW)

add_text_box(slide,
             "✅  Decompose:  ProfessorCourse (Professor | Course)  +  "
             "StudentProfessor (StudentID | Professor)",
             0.4, 3.95, 12.5, 0.3, font_size=12, bold=True, color=GREEN)

# Comparison table
add_text_box(slide, "3NF vs BCNF:", 0.4, 4.32, 4.0, 0.3,
             font_size=13, bold=True, color=ACCENT_BLUE)
headers_c = ["Criteria", "3NF", "BCNF"]
col_ws_c = [6.5, 2.7, 2.7]
col_xs_c = [0.4, 7.05, 9.9]
add_rect(slide, 0.4, 4.62, 12.5, 0.35, MID_BLUE)
for cx, cw, h in zip(col_xs_c, col_ws_c, headers_c):
    add_text_box(slide, h, cx + 0.05, 4.63, cw, 0.33,
                 font_size=12, bold=True, color=YELLOW)
rows_c = [
    ("Removes partial & transitive dependencies",  "✅", "✅"),
    ("Removes anomalies from prime attr FDs",       "❌", "✅"),
    ("Always dependency-preserving",                "✅", "❌  (sometimes)"),
    ("Use when",                                    "Standard OLTP", "Max redundancy elimination"),
]
for ri, row in enumerate(rows_c):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 4.97 + ri * 0.33
    for cx, cw, cell in zip(col_xs_c, col_ws_c, row):
        add_rect(slide, cx, y, cw, 0.33, bg)
        col = GREEN if cell == "✅" else (RED_SOFT if cell.startswith("❌") else WHITE)
        add_text_box(slide, "  " + cell, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.29, font_size=11, color=col)

slide.notes_slide.notes_text_frame.text = (
    "Students often ask: if 3NF removes transitive dependencies, what's left for BCNF? "
    "Answer: prime attributes. 3NF still permits an FD where a prime attribute depends on "
    "a non-superkey. BCNF closes this loophole. Important caveat: BCNF decomposition is "
    "not always dependency-preserving — in some cases you must choose between BCNF and "
    "preserving all FDs."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 6 — 4NF & 5NF OVERVIEW
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Higher Normal Forms — 4NF and 5NF")

add_rect(slide, 0.4, 1.32, 12.5, 0.38, MID_BLUE)
add_text_box(slide, "Fourth Normal Form (4NF) — Eliminating Multi-Valued Dependencies",
             0.55, 1.34, 12.2, 0.34, font_size=15, bold=True, color=YELLOW)
add_text_box(slide,
             "Prerequisite: BCNF   |   MVD Notation: A →→ B  (A independently determines "
             "multiple B values)\n"
             "4NF: Relation is in 4NF if in BCNF and contains NO non-trivial MVDs unless "
             "the determinant is a superkey.",
             0.55, 1.72, 12.2, 0.6, font_size=12, color=WHITE)

add_text_box(slide, "Example — Violates 4NF:", 0.4, 2.38, 5.0, 0.3,
             font_size=13, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 2.68, 6.8, 1.05, RGBColor(0x10, 0x25, 0x40))
tbl4 = ("  Employee  |  Skill    |  Language\n"
        "  ───────────────────────────────────────\n"
        "  Alice      |  Java     |  English\n"
        "  Alice      |  Python   |  French")
add_text_box(slide, tbl4, 0.55, 2.7, 6.6, 1.0, font_size=11, color=WHITE)
add_text_box(slide,
             "  Employee →→ Skill   (independently)\n"
             "  Employee →→ Language (independently)\n"
             "  → Cartesian product = spurious rows!",
             7.4, 2.7, 5.1, 0.9, font_size=12, color=YELLOW)

add_text_box(slide,
             "✅  Decompose:  EmployeeSkill (Employee | Skill)  +  "
             "EmployeeLanguage (Employee | Language)",
             0.4, 3.8, 12.5, 0.3, font_size=12, bold=True, color=GREEN)

add_rect(slide, 0, 4.2, 13.33, 0.06, ACCENT_BLUE)

add_rect(slide, 0.4, 4.32, 12.5, 0.38, MID_BLUE)
add_text_box(slide, "Fifth Normal Form (5NF / PJNF) — Eliminating Join Dependencies",
             0.55, 4.34, 12.2, 0.34, font_size=15, bold=True, color=YELLOW)
add_text_box(slide,
             "Prerequisite: 4NF   |   Join Dependency (JD): Table can be losslessly "
             "decomposed into 3+ tables, and joining them back reconstructs the original.\n"
             "5NF: Relation is in 5NF if every join dependency is implied by the candidate keys.",
             0.55, 4.72, 12.2, 0.6, font_size=12, color=WHITE)

add_text_box(slide, "Classic Example — Supplier / Part / Project:",
             0.4, 5.38, 8.0, 0.3, font_size=13, bold=True, color=ACCENT_BLUE)
pts5 = [
    "  •  A supplier supplies certain parts, and those parts are used in certain projects",
    "  •  The combination {Supplier, Part, Project} holds only when all three pairwise "
    "relationships independently hold",
    "  •  Decompose into 3 binary tables; rejoining must reproduce the exact original",
]
add_multiline(slide, [(t, 12, False, WHITE) for t in pts5], 0.4, 5.68, 12.5, 0.9)

add_rect(slide, 0.4, 6.65, 12.5, 0.38, RGBColor(0x0D, 0x25, 0x40))
add_text_box(slide,
             "  When to Apply: 4NF — uncommon but relevant;  "
             "5NF — largely theoretical, important for academic completeness and advanced modeling.",
             0.55, 6.67, 12.2, 0.34, font_size=11, color=LIGHT_GRAY)

slide.notes_slide.notes_text_frame.text = (
    "Multi-valued dependencies are harder to spot — the issue is two attributes being "
    "independently determined by the same key and mistakenly combined. The classic sign "
    "is needing a Cartesian product of values to represent all combinations. 4NF is less "
    "common in production but important for theoretical completeness. 5NF is largely "
    "theoretical — key insight: it deals with relationships that only make sense in triplicate."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 7 — NORMALIZATION LADDER
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms — Summary")
slide_title_bar(slide, "The Normalization Ladder — Visual Summary")

nf_data = [
    ("5NF",  "No join dependencies beyond candidate keys",      RGBColor(0x8E, 0x44, 0xAD)),
    ("4NF",  "No non-trivial multi-valued dependencies",        RGBColor(0x16, 0x7A, 0xC6)),
    ("BCNF", "Every determinant must be a superkey",            ACCENT_BLUE),
    ("3NF",  "No transitive dependencies",                      RGBColor(0x27, 0xAE, 0x60)),
    ("2NF",  "No partial dependencies",                         RGBColor(0xF3, 0x9C, 0x12)),
    ("1NF",  "Atomic values, no repeating groups",              RGBColor(0xE7, 0x4C, 0x3C)),
]

box_left  = 1.2
box_width = 10.9
box_h     = 0.72
start_y   = 1.35
gap       = 0.08

for i, (label, desc, color) in enumerate(nf_data):
    y = start_y + i * (box_h + gap)
    indent = i * 0.18
    add_rect(slide, box_left + indent, y, box_width - indent * 2, box_h, color)
    add_text_box(slide, label, box_left + indent + 0.15, y + 0.1,
                 1.4, box_h - 0.12, font_size=20, bold=True, color=WHITE)
    add_text_box(slide, desc, box_left + indent + 1.7, y + 0.1,
                 box_width - indent * 2 - 1.8, box_h - 0.12,
                 font_size=14, color=WHITE)
    if i < len(nf_data) - 1:
        add_text_box(slide, "⊃", 6.3, y + box_h - 0.05, 0.5, 0.35,
                     font_size=14, bold=True, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide, "Every higher NF includes ALL requirements of the forms below it.",
             0.5, 6.9, 12.3, 0.35,
             font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

slide.notes_slide.notes_text_frame.text = (
    "This ladder diagram is one of the most important visual aids in normalization. "
    "Use it to reinforce that each normal form includes all requirements of lower forms. "
    "A table in BCNF is also in 3NF, 2NF, and 1NF. The converse is not true. "
    "This hierarchy helps students quickly determine which form a table is in by "
    "checking conditions from bottom to top."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 8 — FUNCTIONAL DEPENDENCIES (CONCEPTS + IDENTIFICATION)
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "C. Functional Dependencies")
slide_title_bar(slide, "Functional Dependencies — Concepts and Identification")

add_rect(slide, 0.4, 1.32, 12.5, 0.5, MID_BLUE)
add_text_box(slide,
             "FD  X → Y: For every valid tuple, if two tuples share the same X, "
             "they MUST have the same Y.  (\"X functionally determines Y\")",
             0.55, 1.34, 12.2, 0.46, font_size=13, color=WHITE)

# Left: Terms table
terms = [
    ("Determinant",   "Left side of FD",               "StudentID in StudentID → Name"),
    ("Dependent",     "Right side of FD",              "Name in StudentID → Name"),
    ("Trivial FD",    "Dependent ⊆ determinant",       "{A,B} → A"),
    ("Full FD",       "Relies on ENTIRE determinant",  "Critical for 2NF"),
    ("Partial FD",    "Relies on PART of determinant", "Violates 2NF"),
    ("Transitive FD", "A → B → C chain",               "Violates 3NF"),
]
col_xs_t = [0.4, 2.6, 6.1]
col_ws_t = [2.15, 3.45, 3.6]
add_rect(slide, 0.4, 1.9, 9.75, 0.32, MID_BLUE)
for ci, h in enumerate(["Term", "Definition", "Example"]):
    cx, cw = col_xs_t[ci], col_ws_t[ci]
    add_text_box(slide, h, cx + 0.05, 1.91, cw, 0.3,
                 font_size=12, bold=True, color=YELLOW)
for ri, (term, defn, ex) in enumerate(terms):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 2.22 + ri * 0.32
    for cx, cw, txt in zip(col_xs_t, col_ws_t, [term, defn, ex]):
        add_rect(slide, cx, y, cw, 0.32, bg)
        add_text_box(slide, "  " + txt, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.28, font_size=10, color=WHITE)

# Right: How to Identify FDs (5 steps)
add_text_box(slide, "How to Identify FDs:", 9.9, 1.88, 3.1, 0.3,
             font_size=12, bold=True, color=ACCENT_BLUE)
steps_text = [
    ("Step 1: List all attributes in the table", 10, False, WHITE),
    ("Step 2: Identify the primary / composite key", 10, False, WHITE),
    ("Step 3: For each non-key attr: 'What uniquely determines this?'", 10, False, WHITE),
    ("Step 4: Write out all discovered FDs", 10, False, WHITE),
    ("Step 5: Check for partial FDs (→2NF) and transitive FDs (→3NF)", 10, False, YELLOW),
]
add_multiline(slide, steps_text, 9.9, 2.22, 3.1, 2.1)

# Bottom: Practical example
add_text_box(slide, "Practical Example — Employee Project Table:",
             0.4, 4.26, 8.0, 0.3, font_size=12, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 4.56, 12.5, 0.42, RGBColor(0x10, 0x25, 0x40))
add_text_box(slide,
             "  EmpID | ProjID | EmpName | ProjName | HoursWorked | Dept | DeptManager",
             0.55, 4.58, 12.2, 0.38, font_size=11, color=LIGHT_GRAY)
fds_found = [
    ("{EmpID, ProjID}  →  HoursWorked",  "✅  Full FD on composite PK",        WHITE,  GREEN),
    ("EmpID           →  EmpName",       "⚠  Partial FD (only EmpID needed)",  WHITE,  YELLOW),
    ("ProjID          →  ProjName",      "⚠  Partial FD (only ProjID needed)", WHITE,  YELLOW),
    ("Dept            →  DeptManager",   "⚠  Transitive FD (through Dept)",    WHITE,  RED_SOFT),
]
for i, (fd, note, c1, c2) in enumerate(fds_found):
    y = 5.03 + i * 0.32
    add_rect(slide, 0.4, y, 5.5, 0.3, RGBColor(0x10, 0x25, 0x40))
    add_text_box(slide, "  " + fd, 0.5, y + 0.01, 5.3, 0.28, font_size=10, color=c1)
    add_rect(slide, 5.95, y, 7.0, 0.3, RGBColor(0x10, 0x25, 0x40))
    add_text_box(slide, "  " + note, 6.05, y + 0.01, 6.8, 0.28, font_size=10, color=c2)

slide.notes_slide.notes_text_frame.text = (
    "Many students confuse determinants with primary keys. Stress that a determinant "
    "can be ANY attribute or set — it doesn't have to be the PK. A non-key attribute "
    "can be a determinant (e.g., Email → Phone), and that's what causes transitive "
    "dependency issues in 3NF. Walk through each FD in the Employee Project table and "
    "have students identify whether it is full, partial, or transitive."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 9 — NORMALIZATION PROCESS & DECOMPOSITION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "D. Normalization Process")
slide_title_bar(slide, "The Normalization Process — Framework & Decomposition")

# Left: compact flow diagram
flow = [
    ("RAW / UNNORMALIZED DATA (UNF)", ACCENT_BLUE),
    ("Step 1 → 1NF  :  Remove repeating groups → atomic values", MID_BLUE),
    ("Step 2 → 2NF  :  Remove partial dependencies", MID_BLUE),
    ("Step 3 → 3NF  :  Remove transitive dependencies", MID_BLUE),
    ("Step 4 → BCNF :  Every determinant is a superkey", MID_BLUE),
    ("Step 5 → 4NF  :  Remove multi-valued dependencies", MID_BLUE),
    ("Step 6 → 5NF  :  Remove join dependencies", MID_BLUE),
    ("FULLY NORMALIZED DATABASE ✅", GREEN),
]
box_left_f = 0.4
box_w_f    = 7.2
box_h_f    = 0.46
start_y_f  = 1.32
for i, (label, color) in enumerate(flow):
    y = start_y_f + i * (box_h_f + 0.04)
    add_rect(slide, box_left_f, y, box_w_f, box_h_f, color)
    bold = (i == 0 or i == len(flow) - 1)
    add_text_box(slide, "   " + label, box_left_f + 0.08, y + 0.05,
                 box_w_f - 0.12, box_h_f - 0.08,
                 font_size=12, bold=bold, color=WHITE)
    if i < len(flow) - 1:
        add_text_box(slide, "▼", box_left_f + box_w_f / 2 - 0.2, y + box_h_f - 0.04,
                     0.4, 0.24, font_size=11, color=LIGHT_GRAY,
                     align=PP_ALIGN.CENTER)

# Right: Decomposition principles
add_rect(slide, 8.0, 1.32, 5.1, 0.34, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "✅ Lossless-Join Decomposition",
             8.1, 1.34, 4.9, 0.3, font_size=13, bold=True, color=GREEN)
lossless = [
    "Joining all decomposed tables returns",
    "EXACTLY the original (no spurious tuples).",
    "Test: R1 ∩ R2 → R1  OR  R1 ∩ R2 → R2",
    "(common attr is a key in ≥1 table)",
]
add_multiline(slide, [(t, 11, False, WHITE) for t in lossless],
              8.0, 1.68, 5.1, 1.1)

add_rect(slide, 8.0, 2.84, 5.1, 0.34, RGBColor(0x0D, 0x20, 0x38))
add_text_box(slide, "✅ Dependency-Preserving Decomposition",
             8.1, 2.86, 4.9, 0.3, font_size=13, bold=True, color=ACCENT_BLUE)
dep_p = [
    "All original FDs can be enforced using",
    "only the decomposed tables (no JOIN needed).",
    "If lost: must use application-level logic",
    "to enforce the business rule.",
]
add_multiline(slide, [(t, 11, False, WHITE) for t in dep_p],
              8.0, 3.2, 5.1, 1.1)

add_rect(slide, 8.0, 4.36, 5.1, 0.32, MID_BLUE)
add_text_box(slide, "Trade-off: 3NF vs BCNF",
             8.1, 4.37, 4.9, 0.3, font_size=12, bold=True, color=YELLOW)
tradeoff_hdr = ["Property", "3NF", "BCNF"]
tradeoff_rows = [
    ("Lossless",              "✅ Always", "✅ Always"),
    ("Dependency-preserving", "✅ Always", "❌ Not always"),
]
col_xs_tr = [8.0, 10.35, 11.75]
col_ws_tr = [2.3, 1.4, 1.4]
add_rect(slide, 8.0, 4.68, 5.1, 0.3, MID_BLUE)
for cx, cw, h in zip(col_xs_tr, col_ws_tr, tradeoff_hdr):
    add_text_box(slide, h, cx + 0.05, 4.69, cw - 0.1, 0.28,
                 font_size=10, bold=True, color=YELLOW)
for ri, row in enumerate(tradeoff_rows):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 4.98 + ri * 0.3
    for cx, cw, cell in zip(col_xs_tr, col_ws_tr, row):
        add_rect(slide, cx, y, cw, 0.3, bg)
        col = GREEN if "✅" in cell else (RED_SOFT if "❌" in cell else WHITE)
        add_text_box(slide, cell, cx + 0.05, y + 0.01, cw - 0.1, 0.28,
                     font_size=10, color=col)

add_rect(slide, 8.0, 5.62, 5.1, 0.75, RGBColor(0x14, 0x2D, 0x50))
add_text_box(slide,
             "  Principles:\n"
             "  • Work bottom-up (1NF → 5NF)\n"
             "  • Lossless decomposition is NON-NEGOTIABLE\n"
             "  • Most systems target 3NF or BCNF",
             8.1, 5.64, 4.9, 0.7, font_size=10, color=LIGHT_GRAY)

slide.notes_slide.notes_text_frame.text = (
    "Present this as a workflow students can apply methodically. Normalization is "
    "iterative — after each step, re-examine what remains. In practice, most designers "
    "target 3NF or BCNF and stop there. Lossless join is non-negotiable — if decomposition "
    "creates false rows upon joining, it is wrong. Dependency preservation is a quality "
    "goal — losing a dependency means the database can no longer enforce that business rule."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 10 — SUMMARY & BEST PRACTICES
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "Summary")
slide_title_bar(slide, "Summary — Key Takeaways & Best Practices")

summary_data = [
    ("1NF",  "Atomic values, no repeating groups",         "—"),
    ("2NF",  "Full dependency on whole PK",                "Partial"),
    ("3NF",  "No non-key → non-key dependency",            "Transitive"),
    ("BCNF", "Every determinant is a superkey",            "Non-superkey FDs"),
    ("4NF",  "No multi-valued dependencies",               "MVDs"),
    ("5NF",  "No join dependencies beyond candidate keys", "Join Dependencies"),
]
cols_s = ["NF", "Key Rule", "Removes"]
col_ws_s = [1.0, 5.5, 2.5]
col_xs_s = [0.4, 1.55, 7.2]

add_rect(slide, 0.4, 1.32, 9.35, 0.35, MID_BLUE)
for cx, cw, h in zip(col_xs_s, col_ws_s, cols_s):
    add_text_box(slide, h, cx + 0.05, 1.33, cw - 0.1, 0.33,
                 font_size=12, bold=True, color=YELLOW)

nf_colors = [
    RGBColor(0xE7, 0x4C, 0x3C), RGBColor(0xF3, 0x9C, 0x12),
    RGBColor(0x27, 0xAE, 0x60), ACCENT_BLUE,
    RGBColor(0x16, 0x7A, 0xC6), RGBColor(0x8E, 0x44, 0xAD),
]
for ri, (row, nfc) in enumerate(zip(summary_data, nf_colors)):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 1.67 + ri * 0.32
    for ci, (cx, cw, cell) in enumerate(zip(col_xs_s, col_ws_s, row)):
        add_rect(slide, cx, y, cw, 0.32, bg)
        col = nfc if ci == 0 else WHITE
        bold = ci == 0
        add_text_box(slide, "  " + cell, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.28, font_size=11, bold=bold, color=col)

# Core principles (right of summary table)
add_rect(slide, 9.9, 1.32, 3.0, 0.35, MID_BLUE)
add_text_box(slide, "Core Principles", 9.95, 1.33, 2.9, 0.33,
             font_size=12, bold=True, color=YELLOW)
principles = [
    "🔑  Determinants must be superkeys (BCNF+)",
    "🔑  Decomposition must ALWAYS be lossless",
    "🔑  Strive to preserve all FDs",
    "🔑  Normalization = eliminating redundancy",
    "🔑  Target 3NF or BCNF for most OLTP systems",
]
add_multiline(slide, [(p, 10, False, WHITE) for p in principles],
              9.9, 1.67, 3.0, 1.6)

# Best practices vs Pitfalls
add_rect(slide, 0.4, 3.72, 12.5, 0.35, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "✅  Best Practices", 0.5, 3.74, 6.0, 0.31,
             font_size=13, bold=True, color=GREEN)
add_text_box(slide, "❌  Common Pitfalls", 6.75, 3.74, 6.0, 0.31,
             font_size=13, bold=True, color=RED_SOFT)

bps = [
    "Start from UNF and work upward systematically",
    "Document ALL FDs before starting",
    "Verify lossless join at every decomposition step",
    "Aim for 3NF as baseline in production systems (OLTP)",
    "Consider INTENTIONAL denormalization for read-heavy systems",
]
for i, bp in enumerate(bps):
    y = 4.1 + i * 0.3
    bg = RGBColor(0x0D, 0x30, 0x1A) if i % 2 == 0 else RGBColor(0x10, 0x38, 0x20)
    add_rect(slide, 0.4, y, 6.1, 0.28, bg)
    add_text_box(slide, "  •  " + bp, 0.45, y + 0.01, 6.0, 0.26, font_size=9, color=WHITE)

pitfalls = [
    ("Over-normalizing",            "Too many joins slow down queries"),
    ("Under-normalizing",           "Leads to update/insert/delete anomalies"),
    ("Ignoring composite keys",     "Missing partial deps — 2NF error"),
    ("Stopping at 3NF prematurely", "Overlapping candidate keys still cause issues"),
    ("Breaking lossless join",      "Decomposed tables cannot be rejoined correctly"),
]
for i, (mistake, reason) in enumerate(pitfalls):
    y = 4.1 + i * 0.3
    bg = RGBColor(0x30, 0x10, 0x10) if i % 2 == 0 else RGBColor(0x38, 0x14, 0x14)
    add_rect(slide, 6.75, y, 2.35, 0.28, bg)
    add_text_box(slide, "  " + mistake, 6.8, y + 0.01, 2.25, 0.26,
                 font_size=9, bold=True, color=YELLOW)
    add_rect(slide, 9.15, y, 3.65, 0.28, bg)
    add_text_box(slide, "  " + reason, 9.2, y + 0.01, 3.55, 0.26,
                 font_size=9, color=WHITE)

add_rect(slide, 0.4, 5.65, 12.5, 0.52, RGBColor(0x14, 0x2D, 0x50))
add_text_box(slide,
             "  💡  Normalization is a TOOL, not a goal. Design with purpose!\n"
             "  \"Normalization is the foundation of good relational database design — "
             "every scalable, maintainable system relies on it.\"",
             0.55, 5.67, 12.2, 0.5, font_size=11, bold=True, color=ACCENT_BLUE)

slide.notes_slide.notes_text_frame.text = (
    "Use this slide as a wrap-up. Ask students to close notes and recall: what does "
    "each NF eliminate? Reiterate that normalization is cumulative — each level builds "
    "on the last. Over-normalization is a real-world problem. Denormalization is a "
    "deliberate, documented design decision — the opposite of sloppy design. "
    "Preview next topics: denormalization, indexing strategies, or physical database design."
)


# ═══════════════════════════════════════════════════════════════
#  SAVE
# ═══════════════════════════════════════════════════════════════
output_file = "Advand_Normalization_Concepts.pptx"
prs.save(output_file)
print(f"✅  Presentation saved as:  {output_file}")
print(f"    Total slides: {len(prs.slides)}  (1 title + 9 content slides)")
