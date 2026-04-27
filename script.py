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

slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Third Normal Form (3NF) — What Is It?")

add_rect(slide, 0.4, 1.3, 12.5, 1.5, MID_BLUE)
add_text_box(slide, "Definition", 0.55, 1.33, 4.0, 0.4,
             font_size=15, bold=True, color=YELLOW)
defn = ("A relation is in 3NF if and only if:\n"
        "  1.  It is already in 2NF, AND\n"
        "  2.  Every non-key attribute is NON-TRANSITIVELY dependent on the primary key.")
add_text_box(slide, defn, 0.55, 1.72, 12.2, 1.0, font_size=14, color=WHITE)

add_text_box(slide, "What is a Transitive Dependency?",
             0.4, 2.95, 12.5, 0.38, font_size=15, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 3.33, 12.5, 0.9, RGBColor(0x10, 0x25, 0x40))
trans = ("  If  A → B  and  B → C,  then  A → C  is a TRANSITIVE dependency.\n"
         "  C is transitively dependent on A through B.")
add_text_box(slide, trans, 0.55, 3.36, 12.2, 0.85, font_size=14, color=LIGHT_GRAY)

add_rect(slide, 0.4, 4.35, 12.5, 0.95, RGBColor(0x14, 0x3D, 0x20))
add_text_box(slide,
             "🔑  Mnemonic:  \"Every non-key attribute must tell us a fact about\n"
             "     the KEY,  the WHOLE KEY,  and  NOTHING BUT THE KEY.\"",
             0.55, 4.38, 12.2, 0.9,
             font_size=15, bold=True, color=GREEN)

slide.notes_slide.notes_text_frame.text = (
    "The phrase 'nothing but the key' is a classic mnemonic for all three normal forms: "
    "1NF=the key, 2NF=the whole key, 3NF=nothing but the key. "
    "Transitive dependency is the specific enemy of 3NF. A non-key attribute that "
    "determines another non-key attribute creates an indirect, problematic dependency chain "
    "causing update anomalies."
)

slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "3NF — Identifying and Resolving Transitive Dependencies")

add_text_box(slide, "Problematic Table (Violates 3NF):",
             0.4, 1.32, 7.0, 0.35, font_size=13, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 1.67, 12.5, 1.1, RGBColor(0x10, 0x25, 0x40))
tbl = ("  StudentID  |  StudentName  |  DeptID  |  DeptName\n"
       "  ──────────────────────────────────────────────────────\n"
       "    S001      |    Alice      |   D01    |  Computer Science\n"
       "    S002      |    Bob        |   D02    |  Mathematics")
add_text_box(slide, tbl, 0.55, 1.7, 12.2, 1.0, font_size=12, color=LIGHT_GRAY)

# FD chain
add_text_box(slide, "Functional Dependency Chain:",
             0.4, 2.87, 6.0, 0.35, font_size=13, bold=True, color=ACCENT_BLUE)
fds = [
    ("  StudentID  →  DeptID          ✅  direct", 13, False, WHITE),
    ("  DeptID     →  DeptName        ✅  direct", 13, False, WHITE),
    ("  StudentID  →  DeptName        ❌  TRANSITIVE DEPENDENCY!", 13, True, YELLOW),
]
add_multiline(slide, fds, 0.4, 3.22, 8.5, 1.0)

# Anomalies
add_rect(slide, 8.9, 2.87, 4.0, 1.55, RGBColor(0x40, 0x10, 0x10))
add_text_box(slide, "Anomalies Caused:", 9.0, 2.9, 3.8, 0.35,
             font_size=13, bold=True, color=RED_SOFT)
anom = [
    ("  ⚠  Update Anomaly", 12, False, WHITE),
    ("  ⚠  Deletion Anomaly", 12, False, WHITE),
    ("  ⚠  Insertion Anomaly", 12, False, WHITE),
]
add_multiline(slide, anom, 9.0, 3.25, 3.8, 1.1)

# Solution
add_text_box(slide, "✅  Solution — Decompose into 2 tables:",
             0.4, 4.3, 8.0, 0.38, font_size=13, bold=True, color=GREEN)
add_rect(slide, 0.4, 4.68, 5.8, 0.95, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "Student Table:  StudentID | StudentName | DeptID",
             0.55, 4.72, 5.6, 0.35, font_size=12, color=WHITE)
add_rect(slide, 7.1, 4.68, 5.8, 0.95, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "Department Table:  DeptID | DeptName",
             7.25, 4.72, 5.6, 0.35, font_size=12, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "Walk through each anomaly carefully. Use the deletion anomaly as the most "
    "striking example — losing ALL dept info because the last student was deleted "
    "is clearly a design flaw. After decomposition, both tables are independently "
    "maintainable and DeptName lives in exactly one place."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 5 — BCNF DEFINITION
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Boyce-Codd Normal Form (BCNF) — A Stronger 3NF")

add_rect(slide, 0.4, 1.32, 12.5, 1.3, MID_BLUE)
add_text_box(slide, "Definition", 0.55, 1.35, 4.0, 0.38,
             font_size=15, bold=True, color=YELLOW)
add_text_box(slide,
             "A relation is in BCNF if and only if for every functional dependency X → Y,\n"
             "X must be a SUPERKEY (i.e., X uniquely identifies every tuple in the relation).",
             0.55, 1.73, 12.2, 0.85, font_size=14, color=WHITE)

add_text_box(slide, "When Does 3NF ≠ BCNF?",
             0.4, 2.75, 8.0, 0.38, font_size=15, bold=True, color=ACCENT_BLUE)
pts = [
    "  •  When a table has MULTIPLE OVERLAPPING CANDIDATE KEYS",
    "  •  A non-superkey attribute determines part of a candidate key",
    "  •  3NF allows this if the dependent is a PRIME attribute; BCNF does NOT",
]
add_multiline(slide, [(t, 14, False, WHITE) for t in pts], 0.4, 3.13, 12.5, 1.0)

# Comparison table
add_text_box(slide, "Key Distinction:", 0.4, 4.22, 5.0, 0.35,
             font_size=14, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 4.57, 12.5, 0.35, MID_BLUE)
hdr = "  Feature                                           |  3NF       |  BCNF"
add_text_box(slide, hdr, 0.5, 4.57, 12.3, 0.35,
             font_size=12, bold=True, color=YELLOW)
rows = [
    "  Allows FD where determinant is NOT a superkey?   |  Sometimes |  NEVER",
    "  Removes partial dependencies?                    |  ✅         |  ✅",
    "  Removes transitive dependencies?                 |  ✅         |  ✅",
    "  Always dependency-preserving?                    |  ✅         |  ❌",
]
for i, r in enumerate(rows):
    bg = RGBColor(0x10, 0x25, 0x40) if i % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    add_rect(slide, 0.4, 4.92 + i * 0.32, 12.5, 0.32, bg)
    add_text_box(slide, r, 0.5, 4.93 + i * 0.32, 12.3, 0.3,
                 font_size=11, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "Students often ask: if 3NF removes transitive dependencies, what's left for BCNF? "
    "The answer lies in prime attributes — attributes that are part of a candidate key. "
    "3NF still permits an FD where a prime attribute depends on a non-superkey. BCNF "
    "closes this loophole. In BCNF, the left side of EVERY FD must be a superkey."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 6 — BCNF EXAMPLE
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "BCNF — Spotting the Difference from 3NF")

add_text_box(slide,
             "Scenario: A university assigns professors to courses. Each section has one professor.",
             0.4, 1.32, 12.5, 0.38, font_size=13, color=LIGHT_GRAY)

add_text_box(slide, "Table: Enrollment", 0.4, 1.75, 4.0, 0.35,
             font_size=14, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 2.1, 6.5, 1.1, RGBColor(0x10, 0x25, 0x40))
tbl = ("  StudentID  |  Course    |  Professor\n"
       "  ─────────────────────────────────────────\n"
       "    S001      |  DBMS      |  Dr. Smith\n"
       "    S001      |  Networks  |  Dr. Lee\n"
       "    S002      |  DBMS      |  Dr. Smith")
add_text_box(slide, tbl, 0.55, 2.13, 6.2, 1.0, font_size=12, color=WHITE)

add_text_box(slide, "Functional Dependencies:", 7.3, 1.75, 5.5, 0.35,
             font_size=14, bold=True, color=ACCENT_BLUE)
fds = [
    ("  {StudentID, Course}    →  Professor   (composite PK)", 12, False, WHITE),
    ("  {StudentID, Professor} →  Course      (candidate key)", 12, False, WHITE),
    ("  Professor              →  Course      ⚠ BCNF Violation!", 12, True, YELLOW),
]
add_multiline(slide, fds, 7.3, 2.13, 5.7, 1.1)

add_rect(slide, 0.4, 3.3, 12.5, 0.75, RGBColor(0x40, 0x28, 0x00))
add_text_box(slide,
             "⚠  Professor → Course holds but Professor is NOT a superkey.\n"
             "   It IS in 3NF (Professor is prime) but FAILS BCNF.",
             0.55, 3.33, 12.2, 0.7, font_size=13, bold=True, color=YELLOW)

add_text_box(slide, "✅  Solution — Decompose:",
             0.4, 4.15, 5.0, 0.35, font_size=14, bold=True, color=GREEN)
add_rect(slide, 0.4, 4.5, 5.8, 1.1, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "ProfessorCourse Table:\n  Professor | Course",
             0.55, 4.53, 5.6, 0.65, font_size=12, color=WHITE)
add_rect(slide, 7.1, 4.5, 5.8, 1.1, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "StudentProfessor Table:\n  StudentID | Professor",
             7.25, 4.53, 5.6, 0.65, font_size=12, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "This example perfectly illustrates why BCNF exists. The original table IS in 3NF — "
    "Professor is a prime attribute. But BCNF flags it because Professor alone is not a "
    "superkey. Important caveat: BCNF decomposition is not always dependency-preserving. "
    "In some cases you must choose between BCNF and preserving all FDs."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 7 — 3NF vs BCNF COMPARISON
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "3NF vs BCNF — When to Use Which?")

headers = ["Criteria", "3NF", "BCNF"]
rows_data = [
    ("Removes partial dependencies",         "✅", "✅"),
    ("Removes transitive dependencies",      "✅", "✅"),
    ("Removes anomalies from prime attr FDs","❌", "✅"),
    ("Always lossless decomposition",        "✅", "✅"),
    ("Always dependency-preserving",         "✅", "❌  (sometimes)"),
    ("Strictness Level",                     "Moderate", "Higher"),
    ("Practical use in industry",            "Very common", "When needed"),
]

col_w = [7.0, 2.4, 2.8]
col_x = [0.4, 7.55, 10.1]

# Header row
for ci, (cx, cw, h) in enumerate(zip(col_x, col_w, headers)):
    add_rect(slide, cx, 1.32, cw, 0.42, MID_BLUE)
    add_text_box(slide, h, cx + 0.08, 1.33, cw - 0.1, 0.4,
                 font_size=14, bold=True, color=YELLOW)

for ri, row in enumerate(rows_data):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 1.74 + ri * 0.38
    for ci, (cx, cw, cell) in enumerate(zip(col_x, col_w, row)):
        add_rect(slide, cx, y, cw, 0.38, bg)
        col = GREEN if cell == "✅" else (RED_SOFT if cell == "❌" else WHITE)
        add_text_box(slide, "  " + cell, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.34, font_size=12, color=col)

add_rect(slide, 0.4, 4.7, 12.5, 0.75, RGBColor(0x0D, 0x30, 0x1A))
tips = ("  💡  Rule of Thumb:\n"
        "  • No overlapping candidate keys → 3NF = BCNF\n"
        "  • Overlapping keys + BCNF breaks dependency preservation → prefer 3NF")
add_text_box(slide, tips, 0.55, 4.72, 12.2, 0.72, font_size=12, color=LIGHT_GRAY)

slide.notes_slide.notes_text_frame.text = (
    "In most real-world relational databases, achieving 3NF is sufficient. BCNF is "
    "pursued when complete redundancy elimination is critical. The fact that BCNF may "
    "not preserve all FDs is significant — you'd rather have slight redundancy than "
    "lose the ability to enforce a business rule through an FD."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 8 — 4NF
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Fourth Normal Form (4NF) — Eliminating Multi-Valued Dependencies")

add_rect(slide, 0.4, 1.32, 12.5, 1.1, MID_BLUE)
add_text_box(slide, "Prerequisite: Must be in BCNF", 0.55, 1.35, 6.0, 0.35,
             font_size=13, bold=True, color=YELLOW)
add_text_box(slide,
             "Multi-Valued Dependency (MVD): One attribute independently determines "
             "multiple values of another. Notation:  A →→ B\n"
             "4NF Definition: A relation is in 4NF if it is in BCNF and contains NO "
             "non-trivial MVDs unless the determinant is a superkey.",
             0.55, 1.68, 12.2, 0.72, font_size=13, color=WHITE)

add_text_box(slide, "Example — Violates 4NF:", 0.4, 2.52, 5.0, 0.35,
             font_size=14, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 2.87, 7.5, 1.3, RGBColor(0x10, 0x25, 0x40))
tbl = ("  Employee  |  Skill    |  Language\n"
       "  ───────────────────────────────────────\n"
       "  Alice      |  Java     |  English\n"
       "  Alice      |  Java     |  French\n"
       "  Alice      |  Python   |  English\n"
       "  Alice      |  Python   |  French")
add_text_box(slide, tbl, 0.55, 2.9, 7.2, 1.2, font_size=12, color=WHITE)
add_text_box(slide,
             "  Employee →→ Skill  (independently)\n"
             "  Employee →→ Language  (independently)\n"
             "  Skills & Languages are unrelated → spurious rows!",
             8.1, 2.9, 4.8, 1.1, font_size=13, color=YELLOW)

add_text_box(slide, "✅  Solution — Decompose into 2 tables:",
             0.4, 4.27, 7.0, 0.35, font_size=14, bold=True, color=GREEN)
add_rect(slide, 0.4, 4.62, 5.5, 0.85, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "EmployeeSkill:\n  Employee | Skill",
             0.55, 4.65, 5.3, 0.6, font_size=12, color=WHITE)
add_rect(slide, 7.4, 4.62, 5.5, 0.85, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "EmployeeLanguage:\n  Employee | Language",
             7.55, 4.65, 5.3, 0.6, font_size=12, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "Multi-valued dependencies are harder to spot because the issue isn't about one "
    "attribute determining another — it's about two attributes being independently "
    "determined by the same key and mistakenly combined. The classic sign is needing a "
    "Cartesian product of values to represent all combinations. 4NF is less common in "
    "production but important for theoretical completeness."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 9 — 5NF
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "B. Normal Forms (Part 2)")
slide_title_bar(slide, "Fifth Normal Form (5NF) — Eliminating Join Dependencies")

add_rect(slide, 0.4, 1.32, 12.5, 1.45, MID_BLUE)
add_text_box(slide, "Prerequisite: Must be in 4NF | Also called: PJNF (Project-Join NF)",
             0.55, 1.35, 12.2, 0.38, font_size=13, bold=True, color=YELLOW)
add_text_box(slide,
             "Join Dependency (JD): A table has a join dependency if it can be LOSSLESSLY "
             "decomposed into 3 or more tables, where joining them back reconstructs the original.\n"
             "5NF Definition: A relation is in 5NF if every join dependency is implied by "
             "the candidate keys.",
             0.55, 1.73, 12.2, 1.02, font_size=13, color=WHITE)

add_text_box(slide, "Classic Example — Supplier / Part / Project:",
             0.4, 2.87, 8.0, 0.38, font_size=14, bold=True, color=ACCENT_BLUE)
pts = [
    "  •  A supplier can supply certain parts",
    "  •  Certain parts are used in certain projects",
    "  •  Certain suppliers work on certain projects",
    "  •  The combination {Supplier, Part, Project} only holds when ALL three are independently true",
    "  •  Decompose into 3 binary tables; rejoining must reproduce the exact original",
]
add_multiline(slide, [(t, 13, False, WHITE) for t in pts], 0.4, 3.25, 12.5, 1.5)

add_rect(slide, 0.4, 4.85, 12.5, 0.85, RGBColor(0x0D, 0x25, 0x40))
add_text_box(slide,
             "  When to Apply 5NF:\n"
             "  •  Extremely rare in practice   •  Complex many-to-many-to-many relationships\n"
             "  •  Important for academic completeness and advanced data modeling",
             0.55, 4.88, 12.2, 0.8, font_size=12, color=LIGHT_GRAY)

slide.notes_slide.notes_text_frame.text = (
    "5NF is largely theoretical. You will rarely encounter a case where a DBA explicitly "
    "applies 5NF, but understanding it rounds out the conceptual picture of normalization. "
    "The key insight: 5NF deals with relationships that only make sense in triplicate — "
    "no two-way pairing fully captures the constraint."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 10 — NORMALIZATION LADDER
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
#  SLIDE 11 — DETERMINANTS & DEPENDENTS
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "C. Functional Dependencies")
slide_title_bar(slide, "Functional Dependencies — Determinants and Dependent Attributes")

add_rect(slide, 0.4, 1.32, 12.5, 0.85, MID_BLUE)
add_text_box(slide,
             "FD X → Y means: for every valid tuple, if two tuples share the same value of X, "
             "they MUST have the same value of Y.   (\"X functionally determines Y\")",
             0.55, 1.35, 12.2, 0.82, font_size=14, color=WHITE)

terms = [
    ("Determinant",   "Attribute(s) on the LEFT side of the FD",  "StudentID  in  StudentID → StudentName"),
    ("Dependent",     "Attribute(s) on the RIGHT side of the FD", "StudentName  in  StudentID → StudentName"),
    ("Trivial FD",    "Dependent is a SUBSET of the determinant",  "{A, B} → A"),
    ("Non-trivial FD","Dependent is NOT a subset of determinant",  "StudentID → GPA"),
    ("Full FD",       "Dependent relies on the ENTIRE determinant","Critical for 2NF compliance"),
    ("Partial FD",    "Dependent relies on PART of the determinant","Violates 2NF"),
]

add_rect(slide, 0.4, 2.25, 2.7, 0.38, MID_BLUE)
add_rect(slide, 3.15, 2.25, 4.5, 0.38, MID_BLUE)
add_rect(slide, 7.7, 2.25, 5.2, 0.38, MID_BLUE)
for ci, h in enumerate(["Term", "Definition", "Example"]):
    cx = [0.4, 3.15, 7.7][ci]
    cw = [2.7, 4.5, 5.2][ci]
    add_text_box(slide, h, cx + 0.1, 2.26, cw - 0.1, 0.36,
                 font_size=13, bold=True, color=YELLOW)

for ri, (term, defn, ex) in enumerate(terms):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 2.63 + ri * 0.38
    for cx, cw, txt in [(0.4, 2.7, term), (3.15, 4.5, defn), (7.7, 5.2, ex)]:
        add_rect(slide, cx, y, cw, 0.38, bg)
        add_text_box(slide, "  " + txt, cx + 0.05, y + 0.03,
                     cw - 0.1, 0.34, font_size=11, color=WHITE)

slide.notes_slide.notes_text_frame.text = (
    "Many students confuse determinants with primary keys. Stress that a determinant "
    "can be ANY attribute or set — it doesn't have to be the PK. A non-key attribute "
    "can be a determinant (e.g., Email → PhoneNumber), and that's what causes transitive "
    "dependency issues in 3NF. Partial FDs are the specific issue targeted by 2NF."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 12 — IDENTIFYING FDs IN TABLES
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "C. Functional Dependencies")
slide_title_bar(slide, "How to Identify Functional Dependencies — Step-by-Step")

steps = [
    ("Step 1", "List all attributes in the table"),
    ("Step 2", "Identify the primary key (or composite key)"),
    ("Step 3", "For each non-key attribute ask: 'What uniquely determines this value?'"),
    ("Step 4", "Write out all discovered functional dependencies"),
    ("Step 5", "Check for partial FDs (violates 2NF) and transitive FDs (violates 3NF)"),
]
for i, (s, d) in enumerate(steps):
    add_rect(slide, 0.4, 1.32 + i * 0.4, 1.5, 0.38, MID_BLUE)
    add_text_box(slide, s, 0.45, 1.33 + i * 0.4, 1.4, 0.36,
                 font_size=12, bold=True, color=YELLOW)
    add_rect(slide, 1.95, 1.32 + i * 0.4, 11.0, 0.38,
             RGBColor(0x10, 0x25, 0x40) if i % 2 == 0 else RGBColor(0x14, 0x2D, 0x50))
    add_text_box(slide, "  " + d, 2.05, 1.33 + i * 0.4, 10.8, 0.36,
                 font_size=12, color=WHITE)

add_text_box(slide, "Practical Example — Employee Project Table:",
             0.4, 3.38, 8.0, 0.35, font_size=13, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 3.73, 12.5, 0.65, RGBColor(0x10, 0x25, 0x40))
tbl = "  EmpID | ProjID | EmpName | ProjName | HoursWorked | Dept | DeptManager"
add_text_box(slide, tbl, 0.55, 3.76, 12.2, 0.5, font_size=11, color=LIGHT_GRAY)

fds_found = [
    ("{EmpID, ProjID}  →  HoursWorked",  "✅  Full FD on composite PK",        WHITE,  GREEN),
    ("EmpID           →  EmpName",       "⚠  Partial FD (only EmpID needed)",  WHITE,  YELLOW),
    ("ProjID          →  ProjName",      "⚠  Partial FD (only ProjID needed)", WHITE,  YELLOW),
    ("EmpID           →  Dept",          "⚠  Partial FD",                      WHITE,  YELLOW),
    ("Dept            →  DeptManager",   "⚠  Transitive FD (through Dept)",    WHITE,  RED_SOFT),
]
for i, (fd, note, c1, c2) in enumerate(fds_found):
    y = 4.43 + i * 0.37
    add_rect(slide, 0.4, y, 5.5, 0.35, RGBColor(0x10, 0x25, 0x40))
    add_text_box(slide, "  " + fd, 0.5, y + 0.02, 5.3, 0.32, font_size=11, color=c1)
    add_rect(slide, 5.95, y, 7.0, 0.35, RGBColor(0x10, 0x25, 0x40))
    add_text_box(slide, "  " + note, 6.05, y + 0.02, 6.8, 0.32,
                 font_size=11, color=c2)

slide.notes_slide.notes_text_frame.text = (
    "This example is a gold mine for FD identification. Walk through each FD and "
    "have students identify whether it is full, partial, or transitive. This single "
    "table violates both 2NF and 3NF. Ask students: how many separate tables will "
    "we need after full normalization?"
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 13 — STEPS IN THE NORMALIZATION PROCESS
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "D. Normalization Process")
slide_title_bar(slide, "The Normalization Process — End-to-End Framework")

flow = [
    ("RAW / UNNORMALIZED DATA (UNF)", ACCENT_BLUE),
    ("Step 1 → Apply 1NF  :  Remove repeating groups → atomic values", MID_BLUE),
    ("Step 2 → Apply 2NF  :  Remove partial dependencies", MID_BLUE),
    ("Step 3 → Apply 3NF  :  Remove transitive dependencies", MID_BLUE),
    ("Step 4 → Apply BCNF :  Ensure every determinant is a superkey", MID_BLUE),
    ("Step 5 → Apply 4NF  :  Remove multi-valued dependencies", MID_BLUE),
    ("Step 6 → Apply 5NF  :  Remove join dependencies", MID_BLUE),
    ("FULLY NORMALIZED DATABASE ✅", GREEN),
]

arrow_x = 6.5
box_left = 0.5
box_w    = 12.3
box_h    = 0.52
start_y  = 1.3

for i, (label, color) in enumerate(flow):
    y = start_y + i * (box_h + 0.05)
    add_rect(slide, box_left, y, box_w, box_h, color)
    bold = (i == 0 or i == len(flow) - 1)
    add_text_box(slide, "   " + label, box_left + 0.1, y + 0.06,
                 box_w - 0.15, box_h - 0.1,
                 font_size=14, bold=bold, color=WHITE)
    if i < len(flow) - 1:
        add_text_box(slide, "▼", arrow_x, y + box_h - 0.05,
                     0.4, 0.28, font_size=13, color=LIGHT_GRAY,
                     align=PP_ALIGN.CENTER)

add_text_box(slide,
             "Principles:  Lossless decomposition  •  Preserve functional dependencies  "
             "•  Work bottom-up (1NF → 5NF)",
             0.4, 7.05, 12.5, 0.3, font_size=11,
             color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

slide.notes_slide.notes_text_frame.text = (
    "Present this as a workflow students can apply methodically. Normalization is "
    "iterative — after each step, re-examine what remains. In practice, most designers "
    "target 3NF or BCNF and stop there. The twin goals of lossless decomposition and "
    "dependency preservation should always be kept in mind."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 14 — UNF → NORMALIZED (FULL WORKED EXAMPLE)
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "D. Normalization Process")
slide_title_bar(slide, "From Raw Data to Normalized Tables — Full Worked Example")

add_text_box(slide, "Unnormalized Table (UNF):",
             0.4, 1.3, 5.0, 0.32, font_size=12, bold=True, color=ACCENT_BLUE)
add_rect(slide, 0.4, 1.62, 12.5, 0.7, RGBColor(0x10, 0x25, 0x40))
add_text_box(slide,
             "  OrderID | CustomerName | CustomerCity | Products (multi-valued)       | Salesperson | SalesRegion\n"
             "  O001    | Juan Dela Cruz | Manila     | Laptop x2, Mouse x3          | Ana Reyes   | Luzon",
             0.5, 1.65, 12.3, 0.65, font_size=10, color=WHITE)

add_text_box(slide, "→ After 1NF  (atomic values, composite PK: {OrderID, ProductName}):",
             0.4, 2.38, 12.5, 0.32, font_size=12, bold=True, color=YELLOW)
add_rect(slide, 0.4, 2.7, 12.5, 0.65, RGBColor(0x10, 0x25, 0x40))
add_text_box(slide,
             "  OrderID | CustomerName   | CustomerCity | ProductName | Qty | Salesperson | SalesRegion",
             0.5, 2.73, 12.3, 0.58, font_size=10, color=WHITE)

add_text_box(slide, "→ After 2NF  (remove partial deps → split into Orders + OrderItems):",
             0.4, 3.42, 12.5, 0.32, font_size=12, bold=True, color=YELLOW)
add_rect(slide, 0.4, 3.74, 5.8, 0.65, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide,
             "  Orders:\n  OrderID | CustomerName | CustomerCity | Salesperson | SalesRegion",
             0.5, 3.77, 5.6, 0.58, font_size=10, color=WHITE)
add_rect(slide, 7.1, 3.74, 5.8, 0.65, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide,
             "  OrderItems:\n  OrderID | ProductName | Qty",
             7.2, 3.77, 5.6, 0.58, font_size=10, color=WHITE)

add_text_box(slide,
             "→ After 3NF  (remove transitive: Salesperson → SalesRegion → separate Salesperson table):",
             0.4, 4.46, 12.5, 0.32, font_size=12, bold=True, color=YELLOW)

tables_3nf = [
    ("Orders",      "OrderID | CustomerName | CustomerCity | SalespersonID"),
    ("Salesperson", "SalespersonID | SalespersonName | SalesRegion"),
    ("OrderItems",  "OrderID | ProductName | Qty"),
]
for i, (tname, tcols) in enumerate(tables_3nf):
    x = 0.4 + i * 4.3
    add_rect(slide, x, 4.82, 4.0, 0.72, RGBColor(0x0D, 0x30, 0x1A))
    add_text_box(slide, tname, x + 0.1, 4.84, 3.8, 0.28,
                 font_size=11, bold=True, color=GREEN)
    add_text_box(slide, tcols, x + 0.1, 5.1, 3.8, 0.4, font_size=9, color=WHITE)

add_rect(slide, 0.4, 5.6, 12.5, 0.5, RGBColor(0x0D, 0x25, 0x40))
add_text_box(slide,
             "  ✅  Result: 3 clean, independent, fully normalized tables — "
             "no redundancy, no anomalies!",
             0.55, 5.63, 12.2, 0.45, font_size=13, bold=True, color=GREEN)

slide.notes_slide.notes_text_frame.text = (
    "Walk through each transformation deliberately. After UNF → 1NF point out the "
    "new composite PK. After 1NF → 2NF show which attributes escape to their own table. "
    "After 2NF → 3NF show the salesperson-to-region transitive chain. Optionally draw "
    "an ERD on the board showing relationships between resulting tables."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 15 — DECOMPOSITION TECHNIQUES
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "D. Normalization Process")
slide_title_bar(slide, "Decomposition Techniques in Normalization")

add_rect(slide, 0.4, 1.32, 12.5, 0.68, MID_BLUE)
add_text_box(slide,
             "Decomposition: Breaking relation R into R1, R2, …, Rn such that "
             "NO information is lost and business rules are maintained.",
             0.55, 1.34, 12.2, 0.65, font_size=14, color=WHITE)

# Left panel — Lossless
add_rect(slide, 0.4, 2.1, 5.9, 2.8, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "✅ 1. Lossless-Join Decomposition",
             0.5, 2.13, 5.7, 0.38, font_size=14, bold=True, color=GREEN)
lossless = [
    "Natural joining all decomposed tables",
    "returns EXACTLY the original table.",
    "No spurious (extra/incorrect) tuples.",
    "",
    "Test (for R → R1, R2):",
    "Lossless if:",
    "  R1 ∩ R2 → R1   OR",
    "  R1 ∩ R2 → R2",
    "(common attribute is a key in ≥1 table)",
]
add_multiline(slide, [(t, 12, False, WHITE) for t in lossless],
              0.5, 2.52, 5.7, 2.3)

# Right panel — Dependency Preserving
add_rect(slide, 7.0, 2.1, 5.9, 2.8, RGBColor(0x0D, 0x20, 0x38))
add_text_box(slide, "✅ 2. Dependency-Preserving Decomposition",
             7.1, 2.13, 5.7, 0.38, font_size=14, bold=True, color=ACCENT_BLUE)
dep_pres = [
    "All original FDs can be ENFORCED",
    "using only the decomposed tables",
    "(without needing to JOIN them first).",
    "",
    "Ensures integrity constraints",
    "can be checked efficiently.",
    "",
    "If lost: must use application-level",
    "logic to enforce the business rule.",
]
add_multiline(slide, [(t, 12, False, WHITE) for t in dep_pres],
              7.1, 2.52, 5.7, 2.3)

# Trade-off table
add_text_box(slide, "⚠  Trade-off:", 0.4, 5.0, 3.5, 0.35,
             font_size=14, bold=True, color=YELLOW)
headers_t = ["Property", "3NF", "BCNF"]
row_data_t = [
    ("Lossless Decomposition",      "✅ Always", "✅ Always"),
    ("Dependency Preservation",     "✅ Always", "❌ Not always"),
]
col_widths_t = [5.5, 3.0, 3.0]
col_xs_t = [0.4, 6.05, 9.2]
add_rect(slide, 0.4, 5.35, 11.8, 0.35, MID_BLUE)
for ci, (cx, cw, h) in enumerate(zip(col_xs_t, col_widths_t, headers_t)):
    add_text_box(slide, h, cx + 0.05, 5.36, cw, 0.33,
                 font_size=12, bold=True, color=YELLOW)
for ri, row in enumerate(row_data_t):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 5.7 + ri * 0.35
    for cx, cw, cell in zip(col_xs_t, col_widths_t, row):
        add_rect(slide, cx, y, cw, 0.35, bg)
        col = GREEN if "✅" in cell else (RED_SOFT if "❌" in cell else WHITE)
        add_text_box(slide, "  " + cell, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.31, font_size=11, color=col)

slide.notes_slide.notes_text_frame.text = (
    "Decomposition is the mechanical action of normalization. The lossless join property "
    "is non-negotiable — if decomposition creates false rows upon joining, it is wrong. "
    "Dependency preservation is a quality goal — losing a dependency means the database "
    "can no longer enforce that business rule via a simple constraint. This trade-off is "
    "at the heart of the 3NF vs BCNF debate."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 16 — PITFALLS & BEST PRACTICES
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "D. Normalization Process")
slide_title_bar(slide, "Common Mistakes and Best Practices in Normalization")

# Pitfalls
add_rect(slide, 0.4, 1.32, 6.0, 0.38, RGBColor(0x60, 0x10, 0x10))
add_text_box(slide, "❌  Common Pitfalls", 0.5, 1.34, 5.8, 0.34,
             font_size=14, bold=True, color=RED_SOFT)

pitfalls = [
    ("Over-normalizing",               "Too many joins slow down queries; hurts performance"),
    ("Under-normalizing",              "Data redundancy leads to update/insert/delete anomalies"),
    ("Ignoring composite keys",        "Missing partial dependencies — common 2NF error"),
    ("Stopping at 3NF prematurely",    "Overlapping candidate keys may still cause issues"),
    ("Breaking lossless join property","Decomposed tables cannot be rejoined without losing data"),
]
for i, (mistake, reason) in enumerate(pitfalls):
    bg = RGBColor(0x30, 0x10, 0x10) if i % 2 == 0 else RGBColor(0x38, 0x14, 0x14)
    y = 1.72 + i * 0.36
    add_rect(slide, 0.4, y, 2.5, 0.35, bg)
    add_text_box(slide, "  " + mistake, 0.45, y + 0.02, 2.4, 0.32,
                 font_size=10, bold=True, color=YELLOW)
    add_rect(slide, 2.95, y, 3.5, 0.35, bg)
    add_text_box(slide, "  " + reason, 3.0, y + 0.02, 3.4, 0.32,
                 font_size=10, color=WHITE)

# Best Practices
add_rect(slide, 7.0, 1.32, 6.0, 0.38, RGBColor(0x0D, 0x30, 0x1A))
add_text_box(slide, "✅  Best Practices", 7.1, 1.34, 5.8, 0.34,
             font_size=14, bold=True, color=GREEN)

bps = [
    "Always start from UNF and work upward systematically",
    "Document ALL functional dependencies before starting",
    "Verify lossless join at every decomposition step",
    "Aim for 3NF as baseline in production systems (OLTP)",
    "Apply BCNF+ only when redundancy elimination outweighs cost",
    "Use ER diagrams alongside normalized schemas for clarity",
    "Consider INTENTIONAL denormalization for read-heavy systems",
]
for i, bp in enumerate(bps):
    bg = RGBColor(0x0D, 0x30, 0x1A) if i % 2 == 0 else RGBColor(0x10, 0x38, 0x20)
    y = 1.72 + i * 0.36
    add_rect(slide, 7.0, y, 6.0, 0.35, bg)
    add_text_box(slide, "  •  " + bp, 7.05, y + 0.02, 5.9, 0.32,
                 font_size=10, color=WHITE)

add_rect(slide, 0.4, 4.25, 12.5, 0.62, RGBColor(0x14, 0x2D, 0x50))
add_text_box(slide,
             "  💡  Normalization is a TOOL, not a goal. A perfectly normalized schema "
             "requiring 10 joins\n"
             "       may be worse in practice than a deliberately denormalized one. "
             "Design with purpose!",
             0.55, 4.27, 12.2, 0.6, font_size=12, bold=True, color=ACCENT_BLUE)

slide.notes_slide.notes_text_frame.text = (
    "This slide brings theory into practical wisdom. Over-normalization is a real-world "
    "problem. Normalization is a tool, not a goal in itself. Denormalization is a "
    "deliberate, documented design decision — the opposite of sloppy design. Normalization "
    "gives you the clean foundation; then you optimize from there."
)


# ═══════════════════════════════════════════════════════════════
#  SLIDE 17 — SUMMARY & KEY TAKEAWAYS
# ═══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
slide_chrome(slide, "Summary")
slide_title_bar(slide, "Summary — What You've Learned Today")

summary_data = [
    ("1NF",  "Atomic values, no repeating groups",          "—"),
    ("2NF",  "Full dependency on whole PK",                 "Partial"),
    ("3NF",  "No non-key → non-key dependency",             "Transitive"),
    ("BCNF", "Every determinant is a superkey",             "Non-superkey FDs"),
    ("4NF",  "No multi-valued dependencies",                "MVDs"),
    ("5NF",  "No join dependencies beyond candidate keys",  "Join Dependencies"),
]
cols_s = ["Normal Form", "Key Rule", "Dependency Removed"]
col_ws_s = [2.0, 5.8, 4.4]
col_xs_s = [0.4, 2.55, 8.5]

add_rect(slide, 0.4, 1.32, 12.5, 0.4, MID_BLUE)
for cx, cw, h in zip(col_xs_s, col_ws_s, cols_s):
    add_text_box(slide, h, cx + 0.08, 1.33, cw - 0.1, 0.38,
                 font_size=13, bold=True, color=YELLOW)

nf_colors = [
    RGBColor(0xE7, 0x4C, 0x3C), RGBColor(0xF3, 0x9C, 0x12),
    RGBColor(0x27, 0xAE, 0x60), ACCENT_BLUE,
    RGBColor(0x16, 0x7A, 0xC6), RGBColor(0x8E, 0x44, 0xAD),
]
for ri, (row, nfc) in enumerate(zip(summary_data, nf_colors)):
    bg = RGBColor(0x10, 0x25, 0x40) if ri % 2 == 0 else RGBColor(0x14, 0x2D, 0x50)
    y = 1.72 + ri * 0.38
    for ci, (cx, cw, cell) in enumerate(zip(col_xs_s, col_ws_s, row)):
        add_rect(slide, cx, y, cw, 0.37, bg)
        col = nfc if ci == 0 else WHITE
        bold = ci == 0
        add_text_box(slide, "  " + cell, cx + 0.05, y + 0.02,
                     cw - 0.1, 0.33, font_size=12, bold=bold, color=col)

add_rect(slide, 0.4, 4.02, 12.5, 0.08, ACCENT_BLUE)
add_text_box(slide, "Core Principles:", 0.4, 4.15, 5.0, 0.35,
             font_size=14, bold=True, color=WHITE)
principles = [
    "🔑  Determinants must be superkeys (BCNF and above)",
    "🔑  Decomposition must ALWAYS be lossless",
    "🔑  Strive to preserve all functional dependencies",
    "🔑  Normalization = eliminating redundancy + preventing anomalies",
    "🔑  In practice, 3NF or BCNF is the target for most OLTP systems",
]
add_multiline(slide, [(p, 13, False, WHITE) for p in principles],
              0.4, 4.5, 12.5, 2.0)

add_rect(slide, 0.4, 6.6, 12.5, 0.5, MID_BLUE)
add_text_box(slide,
             "\"Normalization is the foundation of good relational database design — "
             "every scalable, maintainable system relies on it.\"",
             0.55, 6.62, 12.2, 0.46,
             font_size=13, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)

slide.notes_slide.notes_text_frame.text = (
    "Use this slide as a wrap-up. Ask students to close notes and recall: what does "
    "each NF eliminate? Reiterate that normalization is cumulative — each level builds "
    "on the last. Preview next topics: denormalization, indexing strategies, or physical "
    "database design."
)


# ═══════════════════════════════════════════════════════════════
#  SAVE
# ═══════════════════════════════════════════════════════════════
output_file = "Advand_Normalization_Concepts.pptx"
prs.save(output_file)
print(f"✅  Presentation saved as:  {output_file}")
print(f"    Total slides: {len(prs.slides)}  (1 title + 17 content slides)")
