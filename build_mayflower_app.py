"""
Regenerate the Mayflower Specialty AI Liability Supplemental Application PDF.
Uses ReportLab Platypus for layout fidelity to the original.
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, HRFlowable, Flowable, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Polygon, Line
from reportlab.graphics import renderPDF
import os

# ---------------------------------------------------------------------------
# Register custom fonts
# ---------------------------------------------------------------------------
# Register Libre Baskerville Regular for "MAYFLOWER" text
pdfmetrics.registerFont(TTFont('LibreBaskerville-Regular',
                               os.path.join(os.path.dirname(__file__), "assets", "LibreBaskerville-Regular.ttf")))

# Register Montserrat Light for "SPECIALTY" text
pdfmetrics.registerFont(TTFont('Montserrat-Light',
                               os.path.join(os.path.dirname(__file__), "assets", "Montserrat-Light.ttf")))

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#0F3556")          # headers / chrome
NAVY_DARK = colors.HexColor("#0A2840")     # logo
SECTION_HEADER_BG = colors.HexColor("#004D6B")  # section header background - darker teal/navy
ACCENT = colors.HexColor("#1F5F8B")        # subtitle / question numbers / sail
TEAL = colors.HexColor("#2E8FB5")          # field labels
RULE = colors.HexColor("#9FB6C8")          # thin underlines on fields
NOTICE_BG = colors.HexColor("#E8EEF3")     # notice box bg
NOTICE_BORDER = colors.HexColor("#B8C8D6")
LIGHT_FIELD_BG = colors.HexColor("#E8F0F8")  # multi-line answer boxes
TABLE_HEAD_BG = colors.HexColor("#E8EEF3")

PAGE_W, PAGE_H = LETTER
LEFT_MARGIN = 0.6 * inch
RIGHT_MARGIN = 0.6 * inch
TOP_MARGIN = 1.15 * inch   # space for header band
BOTTOM_MARGIN = 0.9 * inch  # space for footer

CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

NORMAL = ParagraphStyle(
    "Normal", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9, leading=11.5, textColor=colors.black,
)

NOTICE = ParagraphStyle(
    "Notice", parent=NORMAL, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#3a4a58"),
)

INSTR = ParagraphStyle(  # body text between section header and first question
    "Instr", parent=NORMAL, fontSize=8.5, leading=11, textColor=colors.HexColor("#2a3a48"),
)

INSTR_ITAL = ParagraphStyle(
    "InstrItal", parent=INSTR, fontName="Helvetica-Oblique", textColor=colors.HexColor("#5a6470"),
)

INTRO_BOLD = ParagraphStyle(
    "IntroBold", parent=NORMAL, fontName="Helvetica-Bold", fontSize=9.5, leading=12,
)

QUESTION = ParagraphStyle(
    "Question", parent=NORMAL, fontName="Helvetica-Bold", fontSize=9, leading=12,
    spaceBefore=4, spaceAfter=2,
)

QHELP = ParagraphStyle(
    "QHelp", parent=NORMAL, fontName="Helvetica-Oblique", fontSize=8, leading=10,
    textColor=colors.HexColor("#5a6470"), spaceAfter=2,
)

OPTION = ParagraphStyle(
    "Option", parent=NORMAL, fontSize=8.7, leading=11,
)

FIELD_LABEL = ParagraphStyle(
    "FieldLabel", parent=NORMAL, fontSize=7.6, leading=9.5, textColor=TEAL,
)

WARRANTY_BODY = ParagraphStyle(
    "WarrantyBody", parent=NORMAL, fontSize=8.7, leading=11.5, spaceAfter=5,
)

WARRANTY_LIST = ParagraphStyle(
    "WarrantyList", parent=NORMAL, fontSize=8.7, leading=11.5, leftIndent=14, spaceAfter=3,
)

WARRANTY_BOLD = ParagraphStyle(
    "WarrantyBold", parent=NORMAL, fontName="Helvetica-Bold", fontSize=8.7, leading=11.5,
    spaceBefore=6, spaceAfter=8,
)

FRAUD_TITLE = ParagraphStyle(
    "FraudTitle", parent=NORMAL, fontName="Helvetica-Bold", fontSize=8, leading=10,
    spaceBefore=4, spaceAfter=1,
)

FRAUD_BODY = ParagraphStyle(
    "FraudBody", parent=NORMAL, fontSize=7.3, leading=9, textColor=colors.HexColor("#222222"),
    spaceAfter=2,
)

END_APP = ParagraphStyle(
    "EndApp", parent=NORMAL, fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
    textColor=colors.HexColor("#5a6470"), spaceBefore=8,
)

# ---------------------------------------------------------------------------
# Custom flowables
# ---------------------------------------------------------------------------

class SectionHeader(Flowable):
    """Navy bar with section number + title in white."""
    def __init__(self, text, width=CONTENT_W, height=18):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height
        self._spaceBefore = 8
        self._spaceAfter = 4

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(SECTION_HEADER_BG)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 11)
        c.drawString(8, self.height/2 - 3.6, self.text)


class CheckBox(Flowable):
    """A square checkbox."""
    def __init__(self, size=8.5):
        super().__init__()
        self.size = size
        self.width = size
        self.height = size

    def wrap(self, aw, ah):
        return (self.size, self.size)

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#506070"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.white)
        c.rect(0, 0, self.size, self.size, stroke=1, fill=1)


class YesNoBoxes(Flowable):
    """Inline Yes [] No [] used at the right edge of question rows."""
    def __init__(self, width=70, height=10):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFont("Helvetica", 8.7)
        c.setFillColor(colors.black)
        # Yes
        c.drawString(0, 1, "Yes")
        c.setStrokeColor(colors.HexColor("#506070"))
        c.setLineWidth(0.6)
        c.rect(18, 0.5, 8.5, 8.5, stroke=1, fill=0)
        # No
        c.drawString(34, 1, "No")
        c.rect(50, 0.5, 8.5, 8.5, stroke=1, fill=0)


class FieldRow(Flowable):
    """A labeled blank field: small teal label sitting above an underline rule."""
    def __init__(self, label, width):
        super().__init__()
        self.label = label
        self.width = width
        self.height = 27

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFont("Helvetica", 8.7)
        c.drawString(0, self.height - 8, self.label)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(0, 2, self.width, 2)


class SignatureFieldRow(Flowable):
    """A labeled blank field for signatures with more spacing between label and underline."""
    def __init__(self, label, width):
        super().__init__()
        self.label = label
        self.width = width
        self.height = 36  # Increased to accommodate 28 points of spacing

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFont("Helvetica", 8.7)
        c.drawString(0, self.height - 8, self.label)  # Label at 28 from bottom
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(0, 2, self.width, 2)  # Line at 2, giving 26 points of space


class AnswerBox(Flowable):
    """A multi-line light-grey answer area."""
    def __init__(self, width, lines=2):
        super().__init__()
        self.width = width
        self.lines = lines
        self.line_h = 11
        self.height = lines * self.line_h + 4

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(LIGHT_FIELD_BG)
        c.setStrokeColor(LIGHT_FIELD_BG)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setStrokeColor(colors.white)
        c.setLineWidth(0.7)
        for i in range(1, self.lines):
            y = i * self.line_h + 2
            c.line(0, y, self.width, y)


# ---------------------------------------------------------------------------
# Helpers to build option rows (checkbox + bold label + italic helper)
# ---------------------------------------------------------------------------

def opt_para(label, helper=None):
    """Returns a Paragraph with bold label and optional italic helper."""
    if helper:
        text = f'<font name="Helvetica-Bold">{label}</font> <font color="#5a6470"><i>{helper}</i></font>'
    else:
        text = f'<font name="Helvetica-Bold">{label}</font>' if label[0].isupper() and len(label.split()) <= 4 else label
        # Many options are plain (not bold). Use plain text here:
        text = label
    return Paragraph(text, OPTION)


def bold_opt_para(label, helper=None):
    """Bold option label + optional italic helper text inline."""
    if helper:
        text = f'<font name="Helvetica-Bold">{label}</font> <font color="#5a6470"><i>{helper}</i></font>'
    else:
        text = f'<font name="Helvetica-Bold">{label}</font>'
    return Paragraph(text, OPTION)


def plain_opt_para(label, helper=None):
    """Plain (not bold) option label + optional helper."""
    if helper:
        text = f'{label} <font color="#5a6470"><i>{helper}</i></font>'
    else:
        text = label
    return Paragraph(text, OPTION)


def options_grid(items, cols=2, col_widths=None, bold=False):
    """
    Build a Table of checkbox options.
    items: list of either str (label) or tuple (label, helper)
    """
    rows = []
    cur = []
    for it in items:
        if isinstance(it, tuple):
            label, helper = it
        else:
            label, helper = it, None
        para = bold_opt_para(label, helper) if bold else plain_opt_para(label, helper)
        cur.append(CheckBox())
        cur.append(para)
        if len(cur) == cols * 2:
            rows.append(cur)
            cur = []
    if cur:
        # pad
        while len(cur) < cols * 2:
            cur.append("")
            cur.append("")
        rows.append(cur)

    if col_widths is None:
        # equal columns
        col_w = CONTENT_W / cols
        widths = []
        for _ in range(cols):
            widths.extend([14, col_w - 14])
    else:
        widths = col_widths

    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def question(num, text, helper=None, yes_no=False):
    """A question label like '1.  How many ...' optionally with italic helper line and/or right-aligned Yes/No boxes."""
    qtext = f'<b>{num}.</b> {text}'
    if not yes_no:
        flow = [Paragraph(qtext, QUESTION)]
        if helper:
            flow.append(Paragraph(helper, QHELP))
        return flow
    # With Yes/No on the right
    yn = YesNoBoxes()
    t = Table(
        [[Paragraph(qtext, QUESTION), yn]],
        colWidths=[CONTENT_W - 70, 70],
        hAlign="LEFT",
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    flow = [t]
    if helper:
        flow.append(Paragraph(helper, QHELP))
    return flow


def fields_row(items):
    """A row of FieldRow objects sized by relative weights.
    items: list of (label, weight) tuples.
    """
    total = sum(w for _, w in items)
    widths = [(CONTENT_W * (w / total)) - 6 for _, w in items]
    # adjust last to fill
    used = sum(widths) + 6 * (len(items) - 1)
    widths[-1] += (CONTENT_W - used) - 6 * 0
    cells = [FieldRow(lbl, w) for (lbl, _), w in zip(items, items)]
    # Recompute using widths above:
    cells = []
    for (label, _), w in zip(items, [(CONTENT_W * (wt / total)) - 6 for _, wt in items]):
        cells.append(FieldRow(label, w))
    col_widths = [(CONTENT_W * (w / total)) - 0 for _, w in items]
    # Use approximate: subtract small inter-cell padding inside cells (we use 0 padding, set widths exact)
    col_widths = [(CONTENT_W * (w / total)) for _, w in items]
    # Rebuild cells with the exact col widths minus a tiny right padding
    cells = [FieldRow(label, cw - 6) for (label, _), cw in zip(items, col_widths)]
    t = Table([cells], colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def notice_box(text):
    """Light blue-grey notice box with a thin border and inset text."""
    p = Paragraph(text, NOTICE)
    t = Table([[p]], colWidths=[CONTENT_W - 0])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NOTICE_BG),
        ("BOX", (0, 0), (-1, -1), 0.4, NOTICE_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


# ---------------------------------------------------------------------------
# Page chrome: header (logo + title), footer
# ---------------------------------------------------------------------------

def draw_logo(c, x, y):
    """Draw the Mayflower sail-on-wave logo mark using the logo image file, then the wordmark."""
    # Get the path to the logo image file
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "Mayflower_LI_Badge_Logomark_RB251031-01.png")

    # Draw the logo image
    # The logo mark is 50x50 points for better visibility
    c.drawImage(logo_path, x, y, width=50, height=50, preserveAspectRatio=True, mask='auto')

    # Wordmark - using custom fonts (Libre Baskerville Regular and Montserrat Light)
    c.setFont("LibreBaskerville-Regular", 16)
    c.setFillColor(NAVY_DARK)
    c.drawString(x + 54, y + 21, "MAYFLOWER")
    c.setFont("Montserrat-Light", 9)
    c.setFillColor(NAVY_DARK)
    c.drawString(x + 54, y + 9, "SPECIALTY")


def page_header_footer(canvas, doc):
    canvas.saveState()
    # --- Header ---
    # Logo at top-left - positioned closer to left edge
    draw_logo(canvas, LEFT_MARGIN - 5, PAGE_H - 0.6 * inch - 19)
    # Right-side title
    canvas.setFont("Helvetica-Bold", 13)
    canvas.setFillColor(NAVY)
    title = "AI Liability Supplemental Application"
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, PAGE_H - 0.55 * inch, title)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(ACCENT)
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, PAGE_H - 0.55 * inch - 13, "Claims Made and Reported Coverage")
    # Header underline (two-tone)
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.0)
    canvas.line(LEFT_MARGIN, PAGE_H - 0.95 * inch, PAGE_W - RIGHT_MARGIN, PAGE_H - 0.95 * inch)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.4)
    canvas.line(LEFT_MARGIN, PAGE_H - 0.95 * inch - 2.5, PAGE_W - RIGHT_MARGIN, PAGE_H - 0.95 * inch - 2.5)

    # --- Footer ---
    footer_y = 0.55 * inch
    canvas.setStrokeColor(colors.HexColor("#cdd5dc"))
    canvas.setLineWidth(0.4)
    canvas.line(LEFT_MARGIN, footer_y + 18, PAGE_W - RIGHT_MARGIN, footer_y + 18)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#4a5560"))
    canvas.drawString(LEFT_MARGIN, footer_y + 5, "© 2026 Mayflower Specialty, Ltd. All rights reserved. Unauthorized reproduction, adaptation, or distribution is prohibited.")
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, footer_y + 5, f"CONFIDENTIAL  |  Page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Story (content) construction
# ---------------------------------------------------------------------------

story = []

# ============================================================
# PAGE 1 — Title block + Section I (Applicant Information)
# ============================================================

story.append(notice_box(
    "PROPRIETARY AND CONFIDENTIAL. This Application and all questions, frameworks, and scoring criteria contained herein are the intellectual property of Mayflower Specialty, Ltd., protected by applicable copyright law. This form is licensed solely for use by the named Applicant to obtain coverage from Mayflower Specialty, Ltd. Any reproduction, adaptation, distribution, or use of this form or any portion thereof, including for developing competing insurance products or underwriting tools, is strictly prohibited without written consent of Mayflower Specialty, Ltd."
))
story.append(Spacer(1, 6))

story.append(notice_box(
    "NOTICE: This is an application for a Claims Made and Reported policy. The policy applied for covers only those Claims first made against an Insured during "
    "the Policy Period or any applicable Extended Reporting Period. Defense costs reduce and may exhaust the Limit of Liability and are subject to the Retention. "
    "Please read the policy carefully."
))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "This Supplemental Application must be completed in conjunction with the applicable ACORD application(s) for Directors and "
    "Officers Liability, Employment Practices Liability, and Professional Liability. All questions must be answered. All information and "
    "submitted materials shall be held in confidence.", INSTR
))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>The Applicant is applying for the following AI-specific coverage module(s):</b>", INTRO_BOLD))
story.append(Spacer(1, 3))
story.append(options_grid([
    "AI Directors and Officers Liability (AI-D&amp;O)",
    "AI Employment Practices Liability (AI-EPL)",
    "AI Professional Liability (AI-E&amp;O)",
    "AI DIC Excess",
], cols=2))
story.append(Spacer(1, 8))

# --- Section I header ---
story.append(SectionHeader("I.  APPLICANT INFORMATION"))
story.append(Spacer(1, 4))

# Field rows
story.append(FieldRow("1. Named Insured (full legal name, including all subsidiaries for which coverage is requested)", CONTENT_W))
story.append(Spacer(1, 4))
story.append(fields_row([("2. DBA (if any)", 1), ("3. State of Incorporation / Formation", 1)]))
story.append(Spacer(1, 4))
story.append(FieldRow("4. Principal Office Address", CONTENT_W))
story.append(Spacer(1, 4))
story.append(fields_row([("5. City", 2), ("State", 1), ("Zip", 1)]))
story.append(Spacer(1, 4))
story.append(fields_row([("6. Phone", 1), ("Email", 1), ("Website", 1)]))
story.append(Spacer(1, 4))
story.append(fields_row([("7. Industry / Sector", 2), ("8. NAICS Code", 1), ("9. Year Founded", 1)]))
story.append(Spacer(1, 4))
story.append(fields_row([("10. Annual Revenue (USD)", 1), ("11. Total Employees", 1), ("12. Number of Locations", 1)]))
story.append(Spacer(1, 4))

story.append(fields_row([("13. Requested Policy Period", 1), ("14. Requested Aggregate Limit", 1)]))
story.append(Spacer(1, 4))

story.append(fields_row([("15. Contact Name and Title", 1), ("16. Contact Email and Phone", 1)]))
story.append(Spacer(1, 4))

# 17. Ownership Structure
story.append(Paragraph("<b>17.</b>  Ownership Structure", QUESTION))
story.append(options_grid([
    "Privately Held", "Publicly Held", "Not-for-Profit", "Other",
], cols=4))
story.append(Spacer(1, 6))


# 18. Business Type
story.append(Paragraph("<b>18.</b>  Business Type", QUESTION))
story.append(options_grid([
    "Corporation", "LLC", "Partnership", "Sole Proprietorship",
], cols=4))
story.append(Spacer(1, 6))

# 19. Geographic Scope
story.append(Paragraph("<b>19.</b>  Geographic Scope of AI Operations", QUESTION))
story.append(options_grid([
    "US Only", "US and EU / UK", "Global",
], cols=3))

# ============================================================
# PAGE 2 — Section II (AI Systems Overview)  questions 1–5b
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("II.  AI SYSTEMS OVERVIEW"))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "<i>This section describes the nature, scope, and deployment architecture of the Applicant's AI systems. All questions refer to the state of the AI "
    "program as of the application date.</i>", INSTR_ITAL
))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "How many distinct AI or machine-learning systems does the Applicant currently deploy in production?",
                      helper="Count each system that is serving predictions, generations, or decisions to a production workload. Exclude research, shadow, or canary "
                             "deployments that do not influence any external or binding decision. Count a fine-tuned variant as a distinct system."))
story.append(options_grid([
    ("0", "pre-deployment"), ("1 to 2", None), ("3 to 5", None),
    ("6 to 10", None), ("11 to 25", None), ("26+", "attach inventory"),
], cols=3, bold=True))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "Provide a schedule of each production AI system with the following information.",
                      helper="A spreadsheet attachment satisfies this question. The schedule must cover every system counted in Question 1 and will be "
                             "incorporated by reference into the policy."))
story.append(Paragraph(
    "<b>(a)</b> system name or identifier  <b>(b)</b> business function served  <b>(c)</b> technology type (NLP, computer vision, tabular ML, generative LLM, "
    "foundation model, reinforcement learning, recommender, other)  <b>(d)</b> build type (in-house, third-party vendor, commercial off-the-shelf, "
    "open-source, fine-tuned from foundation model)  <b>(e)</b> integration depth per Question 3  <b>(f)</b> decision materiality per Question 4  <b>(g)</b> date "
    "first placed into production  <b>(h)</b> date of most recent material change.", INSTR
))
story.append(Spacer(1, 2))
story.append(AnswerBox(CONTENT_W, lines=3))
story.append(Spacer(1, 8))

# Q3
story.extend(question(3, "Highest level of AI integration depth across all deployed systems.",
                      helper="Report the maximum, not the average. If any single system meets the Fully Autonomous definition, classify as Fully Autonomous."))
story.append(options_grid([
    ("Assistive", "recommendations only; human makes every decision"),
], cols=1, bold=True))
story.append(options_grid([
    ("Semi-Autonomous", "AI acts within parameters; human oversight on exceptions"),
], cols=1, bold=True))
story.append(options_grid([
    ("Fully Autonomous", "AI makes binding decisions without human review"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Highest materiality of decisions influenced or made by any AI system.",
                      helper="Materiality is measured by the consequence to the affected third party if the system makes an incorrect decision."))
story.append(options_grid([
    ("Low", "internal optimization only; no direct third-party impact"),
], cols=1, bold=True))
story.append(options_grid([
    ("Medium", "customer-facing recommendations; human approval required before action"),
], cols=1, bold=True))
story.append(options_grid([
    ("High", "binding decisions affecting rights, employment, credit, insurance, healthcare, housing, or safety"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "Generative AI use in any customer-facing, employee-facing, or decision-support application."))
story.append(options_grid([
    ("No", "generative AI not used"),
    ("Yes, internal only", "employees only, not customer-facing"),
    ("Yes, customer-facing", "generative output reaches external parties"),
    ("Yes, decision-support", "generative output influences a binding decision"),
], cols=2, bold=True))
story.append(Spacer(1, 4))

# Q5a
story.append(Paragraph("<b>5a.</b>  If yes, list foundation models and hosting arrangement.", QUESTION))
story.append(Paragraph("<i>List each foundation model by name and version, and indicate commercial API, hyperscaler private deployment, or self-hosted open weights.</i>", QHELP))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q5b
story.append(Paragraph("<b>5b.</b>  Guardrails applied to generative AI in production.", QUESTION))
story.append(options_grid([
    "Input validation and prompt filtering",
    "Output content moderation (toxicity, PII, legal flags)",
    "Retrieval-augmented generation with grounded source citation",
    "Hallucination detection or factuality scoring",
    "Rate limiting and per-user quotas",
    "Logging of prompts and completions with retention policy",
    "Red-team testing within the last 12 months",
    "Human review required before customer-visible output",
    "None of the above",
], cols=2))

story.append(PageBreak())

# ============================================================
# PAGE 3 — Section II questions 6–9
# ============================================================

# Q6
story.extend(question(6, "Reliance on third-party AI components, APIs, or foundation models.",
                      helper="Select the option that describes the most critical third-party dependency. Critical means a failure or breach of the component would materially "
                             "impair the Applicant's service."))
story.append(options_grid([
    ("None", "no third-party AI components in production"),
], cols=1, bold=True))
story.append(options_grid([
    ("Minor", "non-critical enrichment only"),
], cols=1, bold=True))
story.append(options_grid([
    ("Critical, supported vendor", "commercial vendor with SLA and security attestations"),
], cols=1, bold=True))
story.append(options_grid([
    ("Critical, unsupported or open-source", "no vendor SLA; community support only"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q6a
story.append(Paragraph("<b>6a.</b>  For each critical third-party AI component, confirm the Applicant has.", QUESTION))
story.append(options_grid([
    "A written contract with uptime and support terms",
    "A security attestation (SOC 2 Type II, ISO 27001, or equivalent) on file",
    "A data-processing agreement covering all data shared with the vendor",
    "Indemnification for IP infringement arising from model output",
    "Indemnification for bias, defamation, or harm arising from model output",
    "A documented fallback plan if the component becomes unavailable",
], cols=2))
story.append(Spacer(1, 6))

# Q7 (Yes/No on the right)
story.extend(question(7, "Does any AI system operate fully autonomously without real-time human intervention capability?",
                      helper="Intervention capability means a designated human can halt, reverse, or modify an AI decision before its effect becomes "
                             "binding on a third party.",
                      yes_no=True))
story.append(Spacer(1, 4))

# Q7a
story.append(Paragraph("<b>7a.</b>  If yes, describe each such system, its function, automated safeguards, and the kill-switch or circuit-breaker procedure.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=3))
story.append(Spacer(1, 6))

# Q8
story.extend(question(8, "Agentic AI deployments.",
                      helper="An agent is an AI system that plans multi-step actions, invokes external tools or APIs, and operates across sessions without per-step human "
                             "approval. Report agents separately from single-turn chatbots or retrieval systems."))
story.append(options_grid([
    ("No agents in production", None),
    ("Yes, read-only agents", "browse, search, summarize"),
    ("Yes, write-capable agents", "send email, commit code, make bookings, transact"),
    ("Yes, agents with financial authority", "place orders, move funds, execute trades"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q8a
story.append(Paragraph("<b>8a.</b>  If write-capable or financially authorized agents are in production, describe transaction limits, approval gates, and audit-log retention.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q9
story.extend(question(9, "Is any AI system used in any of the following? Select all that apply."))
story.append(options_grid([
    "Autonomous weapons or military targeting",
    "Social scoring or mass surveillance",
    "Predictive policing or criminal sentencing",
    "Biometric identification in public spaces",
    "Real-time emotion inference in workplace or education",
    "Deepfake generation without disclosure",
    "None of the above",
], cols=2))
story.append(Spacer(1, 6))

story.append(notice_box(
    "Applications involving autonomous weapons, social scoring, mass surveillance, biometric identification in public spaces, real-time "
    "emotion inference in workplace or educational settings, or undisclosed deepfake generation are outside Mayflower Specialty's "
    "underwriting appetite. Predictive policing and criminal sentencing applications are considered only under bespoke terms."
))

# ============================================================
# PAGE 4 — Section III (Governance) questions 1–7
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("III.  AI GOVERNANCE"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Controls over the policies, committees, accountabilities, and procedures that govern the Applicant's AI program.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "Has the Applicant adopted a formal AI governance framework?"))
story.append(options_grid([
    ("Yes, fully implemented", "across all production AI systems"),
], cols=1))
story.append(options_grid([
    ("Partially implemented", "implemented for some systems or in progress"),
], cols=1))
story.append(options_grid([
    ("No", "no formal framework"),
], cols=1))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "If a framework is adopted, which? Select all that apply."))
story.append(options_grid([
    "NIST AI Risk Management Framework (AI RMF 1.0)",
    "ISO / IEC 42001",
    "ISO / IEC 23894",
    "OECD AI Principles",
    "IEEE 7000 Series",
    "EU AI Act internal compliance program",
    "Colorado AI Act internal compliance program",
    "Internal or proprietary framework",
    "Other",
], cols=2))
story.append(Spacer(1, 2))
story.append(FieldRow("If Other, specify", CONTENT_W - 30))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "Dedicated AI oversight body.",
                      helper="A body that has not met in the past 12 months should be reported as Ad-hoc regardless of its charter."))
story.append(options_grid([
    ("Yes", "dedicated AI committee with written charter"),
    ("Integrated in ERM", "AI oversight embedded in enterprise risk"),
    ("Ad-hoc", "no standing body; AI issues addressed as they arise"),
    ("No", "no oversight structure"),
], cols=2, bold=True))
story.append(Spacer(1, 4))

# Q3a
story.append(Paragraph("<b>3a.</b>  If Yes or Integrated in ERM, describe composition (roles, not names), reporting line, meeting frequency, and most recent meeting date.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Board or C-suite reporting on AI risk and governance."))
story.append(options_grid([
    ("Yes, monthly", None),
    ("Yes, quarterly", None),
    ("Occasional", "annual or ad hoc"),
    ("No", "not reported to board or C-suite"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "Documented AI ethics or responsible-AI policy."))
story.append(options_grid([
    ("Yes", "adopted and in effect"),
], cols=1, bold=True))
story.append(options_grid([
    ("In development", "drafted, not yet adopted"),
], cols=1, bold=True))
story.append(options_grid([
    ("No", "no such policy"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q6
story.extend(question(6, "Documented AI development and deployment standards.",
                      helper="Standards should cover model selection, data sourcing, training and validation protocols, pre-deployment review, production change control, and decommissioning."))
story.append(options_grid([
    ("Yes", "comprehensive written standards covering all six areas"),
    ("Partial", "some areas documented, others informal"),
    ("Informal", "ad hoc; not written"),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q7
story.extend(question(7, "AI model documentation practices.",
                      helper="Applies to each production system in the inventory at Question II.2."))
story.append(options_grid([
    ("Comprehensive", "model cards, data sheets, risk assessments for every system"),
], cols=1, bold=True))
story.append(options_grid([
    ("Partial", "documentation for some systems or some dimensions"),
], cols=1, bold=True))
story.append(options_grid([
    ("None", "no formal documentation"),
], cols=1, bold=True))

story.append(PageBreak())

# ============================================================
# PAGE 5 — Section III questions 8–14
# ============================================================

# Q8
story.extend(question(8, "Explainability or interpretability capabilities (XAI).",
                      helper="Report the capability that applies to the highest-materiality system."))
story.append(options_grid([
    ("Yes, global and local explanations", "e.g., SHAP, LIME, counterfactuals"),
    ("Yes, local explanations only", None),
    ("In development", None),
    ("No", "black-box only"),
], cols=2, bold=True))
story.append(Spacer(1, 2))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q9
story.extend(question(9, "Highest level of human oversight applied across production AI systems."))
story.append(options_grid([
    ("Human-in-Control", "approval required for every AI decision"),
    ("Human-in-the-Loop", "human reviews every decision before external effect"),
    ("Human-on-the-Loop", "human monitors with intervention ability"),
    ("None", "fully autonomous"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q10
story.extend(question(10, "Formal vendor management program for third-party AI components.",
                      helper="Program should include pre-contract security and bias review, contractual AI-specific addenda, and periodic reassessment."))
story.append(options_grid([
    ("Yes", "formal program meeting all three criteria"),
    ("Partial", "one or two criteria met"),
    ("Informal", "no documented program"),
    ("N/A", "no third-party AI in production"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q11
story.extend(question(11, "Formal change management process for AI model updates.",
                      helper="Applies to any change that materially affects model behavior: retraining, architecture changes, data source changes, prompt template changes for LLM systems."))
story.append(options_grid([
    ("Yes, formal", "documented approval, testing, staged rollout, rollback plan"),
    ("Partial", "some controls; no rollback plan"),
    ("Informal", "ad hoc review"),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q12
story.extend(question(12, "Pre-deployment review requirements for new AI systems. Select all that are required before a system can be deployed."))
story.append(options_grid([
    "Risk assessment signed by a named risk owner",
    "Bias and fairness evaluation on a held-out test set",
    "Red-team or adversarial robustness testing",
    "Security review (threat model, data exposure, prompt injection if LLM)",
    "Legal review (IP, privacy, sector regulation)",
    "Privacy Impact Assessment if PII or PHI is processed",
    "Business owner sign-off",
    "None of the above",
], cols=2))
story.append(Spacer(1, 6))

# Q13
story.extend(question(13, "AI-specific training for personnel who develop, deploy, or operate AI systems."))
story.append(options_grid([
    ("Yes, mandatory", "tracked with completion records"),
    ("Yes, voluntary", None),
    ("In development", None),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q14
story.extend(question(14, "Named accountabilities for AI risk. Check every role that is explicitly assigned in writing."))
story.append(options_grid([
    "Executive sponsor for AI risk (C-suite or board member)",
    "Head of AI or Chief AI Officer",
    "AI ethics lead",
    "Model risk management lead",
    "Data governance lead",
    "AI security lead",
    "AI incident response lead",
    "AI legal or compliance lead",
], cols=2))

# ============================================================
# PAGE 6 — Section IV (Data Governance) questions 1–6
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("IV.  DATA GOVERNANCE"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Controls over data used to train, validate, fine-tune, and operate AI systems.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "Data lineage documentation for training, fine-tuning, and inference data.",
                      helper="Lineage means: for any prediction, the Applicant can reconstruct the data that produced it, the data the model was trained on, and the transformations applied between source and model."))
story.append(options_grid([
    ("Yes", "automated lineage tooling in place across all training pipelines"),
], cols=1, bold=True))
story.append(options_grid([
    ("Partial", "lineage tracked for some systems or some pipelines"),
], cols=1, bold=True))
story.append(options_grid([
    ("No", "no formal lineage"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "Data quality controls applied to training and fine-tuning data."))
story.append(options_grid([
    ("Comprehensive", "automated validation, lineage, and drift monitoring"),
    ("Partial", "automated validation or manual review, not both"),
    ("Basic", "manual spot checks only"),
    ("None", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "Bias and fairness testing on production AI models.",
                      helper="Applies to any system producing decisions or recommendations affecting individuals."))
story.append(options_grid([
    ("Yes, regular", "on a scheduled cadence at least quarterly"),
    ("Partial", "at deployment and after material changes, not on a schedule"),
    ("Yes, ad hoc", "performed when an issue is raised"),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 4))

# Q3a
story.append(Paragraph("<b>3a.</b>  If Yes or Partial, list the fairness metrics used (e.g., demographic parity, equal opportunity, calibration across groups), the protected attributes tested, and testing frequency.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Do any AI systems process or have been trained on the following categories of data? Select all that apply."))
story.append(options_grid([
    "Personally Identifiable Information (PII)",
    "Protected Health Information (PHI)",
    "Biometric data (BIPA-covered or equivalent)",
    "Financial account or transaction data",
    "Children's data (subject to COPPA or GDPR Art. 8)",
    "Special category data under GDPR Art. 9",
    "Geolocation data",
    "Confidential employer data (HR records, performance, compensation)",
    "Attorney-client privileged or work-product data",
    "None of the above",
], cols=2))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "Compliance status with applicable data privacy regulations."))
story.append(options_grid([
    ("Full compliance, audited", "documented and independently audited"),
    ("Full compliance, attested", "documented, internal attestation only"),
    ("Partial compliance", "assessment in progress"),
    ("Non-compliant or unknown", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q5a
story.append(Paragraph("<b>5a.</b>  Regulations the Applicant is subject to.", QUESTION))
story.append(options_grid([
    "GDPR (EU / UK GDPR)",
    "CCPA / CPRA",
    "HIPAA",
    "BIPA (Illinois)",
    "Texas CUBI",
    "Virginia CDPA, Colorado CPA, Connecticut, Utah, other state privacy laws",
    "Canada PIPEDA / Quebec Law 25",
    "None of the above",
], cols=2))
story.append(Spacer(1, 6))

# Q6 — wrap in KeepTogether so the options don't orphan onto the next page
_q6_block = question(6, "Formal data retention and deletion policy for AI training, fine-tuning, and inference data.")
_q6_block.append(options_grid([
    ("Yes", "written policy with defined retention periods and automated enforcement"),
    ("Partial", "policy exists but enforcement is manual"),
    ("In development", None),
    ("No", None),
], cols=2, bold=True))
story.append(KeepTogether(_q6_block))

# (no forced page break — let Q7-8 flow; Section V will break onto its own page)

# ============================================================
# PAGE 7 — Section IV questions 7–8
# ============================================================

# Q7
_q7_block = question(7, "Training data provenance and licensing.")
_q7_block.append(options_grid([
    "All training data is first-party or licensed",
    "Web-scraped data is filtered against known opt-out registries",
    "Copyrighted content is used only under license or fair-use legal opinion",
    "Data provider contracts include downstream-use indemnification",
    "Training data has been screened for PII leakage",
    "None of the above",
], cols=1))
story.append(KeepTogether(_q7_block))
story.append(Spacer(1, 6))

# Q8
_q8_block = question(8, "Ability to honor data-subject rights against AI systems.")
_q8_block.append(options_grid([
    ("Yes", "documented process for access, deletion, rectification, and opt-out"),
    ("Partial", "process exists for some rights or some systems"),
    ("No", "no documented process"),
    ("N/A", "no personal data in AI systems"),
], cols=2, bold=True))
story.append(KeepTogether(_q8_block))

# ============================================================
# PAGE 8 — Section V (Operations) Q1-7 + Section VI start
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("V.  SYSTEM OPERATIONS AND MONITORING"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Operational profile of the Applicant's AI infrastructure, including criticality, availability, monitoring, and model lifecycle management.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "Highest criticality tier assigned to any production AI system.",
                      helper="Criticality is determined by consequence of failure, not by usage volume."))
story.append(options_grid([
    ("Tier 1, Mission-Critical", "failure causes immediate service disruption, regulatory exposure, or third-party harm"),
], cols=1, bold=True))
story.append(options_grid([
    ("Tier 2, Important", "failure degrades service; manual fallbacks exist"),
], cols=1, bold=True))
story.append(options_grid([
    ("Tier 3, Ancillary", "limited operational impact"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "Dependency on external AI infrastructure.",
                      helper="External includes hyperscaler model APIs, managed inference services (Azure OpenAI, AWS Bedrock, Vertex AI), and GPU-as-a-service providers."))
story.append(options_grid([
    ("Critical, single provider", "failure of one provider halts AI service"),
    ("Critical, multi-provider", "redundant providers with tested failover"),
    ("Minor", "external providers for non-critical workloads only"),
    ("None", "fully self-hosted"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "Defined fallback or graceful-degradation mechanisms for AI system failure."))
story.append(options_grid([
    ("Yes", "documented and tested within the last 12 months"),
    ("Partial", "documented but not recently tested"),
    ("No", None),
], cols=3, bold=True))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Automated performance and drift monitoring for production AI.",
                      helper="Monitoring should include prediction distribution drift, input data drift, and quality metrics against ground truth where available."))
story.append(options_grid([
    ("Yes, real-time with alerting", "alerts to named on-call owner"),
    ("Yes, periodic batch", "daily or weekly review"),
    ("Manual only", "no automated monitoring"),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "Production AI model retrain or update cadence.",
                      helper="Report typical cadence for the most frequently updated production system."))
story.append(options_grid([
    ("Continuously", "online learning or daily retraining"),
    ("Periodically", "quarterly to annually on a schedule"),
    ("As needed", "triggered by drift or performance degradation"),
    ("Rarely or never", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q6
story.extend(question(6, "New model versions deployed via shadow or A / B testing before full rollout."))
story.append(options_grid([
    ("Yes, always", "standard practice for every material change"),
    ("Yes, for high-materiality systems only", None),
    ("Sometimes", "case-by-case"),
    ("No", "direct cutover"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q7
story.extend(question(7, "Logging of human overrides to AI recommendations.",
                      helper="Applies to any system where a human can override an AI output before action."))
story.append(options_grid([
    ("Yes, logged with reason code", None),
    ("Yes, logged without reason", None),
    ("No logging", None),
    ("N/A", "no override mechanism"),
], cols=2, bold=True))
story.append(Spacer(1, 8))

# --- Section VI start ---
story.append(PageBreak())
story.append(SectionHeader("VI.  AI INCIDENT RESPONSE"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Capability to detect, contain, communicate, and learn from AI-specific incidents, including model failures, biased outcomes, hallucinations, prompt injection, training-data poisoning, and inappropriate generative output.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "AI-specific incident response plan.",
                      helper="Generic IT incident response does not qualify. The plan must address AI-specific failure modes."))
story.append(options_grid([
    ("Yes, dedicated AI IR plan", "written, approved, tested in past 12 months"),
    ("Yes, written, untested", None),
    ("In development", None),
    ("General IT only", "no AI-specific plan"),
], cols=2, bold=True))
story.append(options_grid([
    ("No", None),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q2 — let it flow as one block across the natural page break
story.extend(question(2, "Primary detection methods for AI incidents. Select all that apply."))
story.append(options_grid([
    "Real-time automated alerts on model metrics (drift, latency, error rate)",
    "Real-time alerts on output content (toxicity, PII leakage, refusals)",
    "User or customer reporting channel",
    "Employee reporting channel",
    "Scheduled manual audits",
    "External researcher disclosure program",
    "No formal detection process",
], cols=1))
story.append(Spacer(1, 6))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "Tabletop exercises or simulations for AI incident scenarios in the past 12 months."))
story.append(options_grid([
    ("Yes, multiple", None),
    ("Yes, one", None),
    ("No", None),
], cols=3, bold=True))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Public-facing complaint mechanism for AI-driven decisions."))
story.append(options_grid([
    ("Yes, published with stated response time", None),
], cols=1, bold=True))
story.append(options_grid([
    ("Yes, published without stated response time", None),
], cols=1, bold=True))
story.append(options_grid([
    ("No", None),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "Appeal or human review process for individuals adversely affected by an AI decision."))
story.append(options_grid([
    ("Yes, documented with defined timelines", None),
    ("Yes, informal", None),
    ("No", None),
    ("N/A", "no decisions affecting individuals"),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q6
story.extend(question(6, "Post-incident remediation and root-cause analysis process."))
story.append(options_grid([
    ("Yes, formal", "written RCA, corrective actions tracked, lessons-learned shared"),
    ("Partial", "RCA performed but not consistently tracked"),
    ("Ad hoc", None),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q7
story.extend(question(7, "Internal AI incidents including near-misses in the past 24 months, whether or not they resulted in external harm or a claim.",
                      helper="A near-miss is an event that would have caused external harm but for a control that worked as intended. Materially understating this number will be treated as a misrepresentation."))
story.append(options_grid([
    ("0", None), ("1 to 3", None), ("4 to 10", None), ("11+", None),
], cols=4, bold=True))
story.append(Spacer(1, 4))

# Q7a
story.append(Paragraph("<b>7a.</b>  If 1 or more, briefly describe the nature and resolution of the most material incident or near-miss.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))

# ============================================================
# PAGE 10 — Section VII + Section VIII start
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("VII.  REGULATORY ENVIRONMENT AND COMPLIANCE"))
story.append(Spacer(1, 6))

# Q1
story.extend(question(1, "EU AI Act classification of the Applicant's AI systems.",
                      helper="Applicants who market, distribute, or have their AI output used in the EU are in scope regardless of establishment."))
story.append(options_grid([
    ("Yes, High Risk", "any system in Annex III or safety-component categories"),
    ("Yes, Limited Risk", "transparency obligations only"),
    ("Yes, Minimal Risk", None),
    ("No", "not in scope"),
], cols=2, bold=True))
story.append(options_grid([
    ("Unsure", "classification not yet assessed"),
], cols=1, bold=True))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "US AI-specific regulations the Applicant is subject to. Select all that apply."))
story.append(options_grid([
    "Colorado AI Act (SB 24-205, effective Feb 2026)",
    "Illinois BIPA",
    "Illinois HB 3773 (AI in employment)",
    "NYC Local Law 144 (Automated Employment Decision Tools)",
    "California AB 2013 (training-data transparency)",
    "California SB 942 (AI content provenance)",
    "Texas Responsible AI Governance Act (TRAIGA)",
    "SEC AI disclosure guidance",
    "FTC Section 5 AI enforcement guidance",
    "EEOC AI in employment guidance",
    "Utah AI Policy Act",
    "Other",
    "None or Unsure",
], cols=2))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "AI systems subject to sector-specific regulatory requirements.",
                      helper="Examples: banking (SR 11-7 model risk management), insurance (NAIC AI Model Bulletin, Colorado Regulation 10-1-1), healthcare (FDA SaMD, HTI-1), broker-dealer or RIA (FINRA, SEC), FCRA-regulated scoring, DOT autonomous vehicles."))
story.append(options_grid([
    ("Yes", "sector regulation applies and compliance program is in place"),
    ("Partial", "sector regulation applies; compliance program in development"),
    ("No", None),
    ("N/A", None),
], cols=2, bold=True))
story.append(Spacer(1, 4))

# Q3a
story.append(Paragraph("<b>3a.</b>  If Yes or Partial, identify regulator(s) and describe the compliance program.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "External audit of AI systems or governance in the past 24 months."))
story.append(options_grid([
    ("Yes, independent third party", "big-four or specialist AI audit firm"),
    ("Yes, consultant review", "scoped engagement, not a formal audit"),
    ("Internal audit only", None),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q5
story.extend(question(5, "ISO / IEC 42001 certification status."))
story.append(options_grid([
    ("Certified", "include certificate"),
    ("In progress", "gap assessment complete, audit scheduled"),
    ("Planned", "committed but not started"),
    ("No", None),
], cols=2, bold=True))
story.append(Spacer(1, 6))

# Q6 (Yes/No on right)
story.extend(question(6, "Regulatory inquiries, investigations, consent decrees, or enforcement actions relating to AI or algorithmic systems in the past 3 years.",
                      helper="Include inquiries that did not result in action. Include inquiries into affiliates where the Applicant's AI systems were the subject.",
                      yes_no=True))
story.append(Spacer(1, 4))

# Q6a
story.append(Paragraph("<b>6a.</b>  If yes, provide regulator, date, subject matter, status, and any remedial terms.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 8))

# Section VIII begins on page 10
story.append(PageBreak())
story.append(SectionHeader("VIII.  CLAIMS AND LOSS HISTORY"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Provide complete information for the prior three (3) years. Attach loss runs if available.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# ============================================================
# PAGE 11 — Section VIII questions 1-4
# ============================================================

# Q1 (Yes/No)
story.extend(question(1, "Any claim, suit, regulatory action, or complaint arising from an AI or algorithmic system in the past three years?", yes_no=True))
story.append(Paragraph("<b>1a.</b>  If yes, provide details (date, nature, status, amount paid or reserved).", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q2
story.extend(question(2, "Any D&amp;O, EPL, or E&amp;O claim or suit in the past three years, regardless of AI involvement?", yes_no=True))
story.append(Paragraph("<b>2a.</b>  If yes, provide details (date, line, nature, status, amount).", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q3
story.extend(question(3, "Aware of any facts or circumstances that could reasonably give rise to a claim?", yes_no=True))
story.append(Paragraph("<b>3a.</b>  If yes, provide details.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))
story.append(Spacer(1, 6))

# Q4
story.extend(question(4, "Has any insurer declined, cancelled, or non-renewed coverage for the Applicant?", yes_no=True))
story.append(Paragraph("<b>4a.</b>  If yes, provide details.", QUESTION))
story.append(AnswerBox(CONTENT_W, lines=2))

# ============================================================
# PAGE 12 — Section IX (Insurance grid) + Section X (Documentation table)
# ============================================================

story.append(SectionHeader("IX.  PRIOR AND CURRENT INSURANCE"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Complete for all current or expiring D&amp;O, EPL, and E&amp;O coverage.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

# Six-column grid: Coverage | Carrier | Policy Period | Limit | Retention/SIR | Premium
ins_headers = ["Coverage", "Carrier", "Policy Period", "Limit", "Retention / SIR", "Premium"]
empty_row = ["", "", "", "", "", ""]
ins_data = [ins_headers] + [empty_row] * 4
col_w = CONTENT_W / 6
ins_widths = [col_w * 0.85, col_w * 1.1, col_w * 1.05, col_w * 0.9, col_w * 1.1, col_w]
# Normalize to sum = CONTENT_W
s = sum(ins_widths)
ins_widths = [w * (CONTENT_W / s) for w in ins_widths]

ins_table = Table(ins_data, colWidths=ins_widths, rowHeights=[20] + [26] * 4)
ins_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD_BG),
    ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 8.5),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9FB6C8")),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cdd5dc")),
]))
story.append(ins_table)
story.append(Spacer(1, 8))
story.append(fields_row([("Proposed Retroactive Date", 1), ("Current Carrier Expiration Date", 1)]))
story.append(Spacer(1, 12))

story.append(PageBreak())
story.append(SectionHeader("X.  REQUIRED DOCUMENTATION"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Items marked with an asterisk (*) are required. All others are recommended and may improve terms.</i>", INSTR_ITAL))
story.append(Spacer(1, 6))

doc_rows = [
    ["Document", "Required", "Enclosed"],
    ["Completed ACORD Application(s) for applicable coverage lines", "*", ""],
    ["Three (3) years of loss runs for D&O, EPL, and E&O", "*", ""],
    ["Most recent annual financial statements or audited financials", "*", ""],
    ["AI Governance Policy or Responsible AI Framework", "*", ""],
    ["AI System Inventory (systems, use cases, data types)", "*", ""],
    ["Organizational chart showing AI oversight / reporting structure", "", ""],
    ["Board or committee minutes related to AI risk oversight", "", ""],
    ["Model documentation, model cards, or data sheets", "", ""],
    ["Bias audit or fairness testing results", "", ""],
    ["AI incident response plan", "", ""],
    ["ISO 42001 certificate or audit report (if applicable)", "", ""],
    ["Third-party AI vendor contracts or due-diligence summaries", "", ""],
    ["Privacy impact assessments for AI systems processing PII or PHI", "", ""],
]
doc_widths = [CONTENT_W * 0.66, CONTENT_W * 0.17, CONTENT_W * 0.17]
doc_table = Table(doc_rows, colWidths=doc_widths,
                  rowHeights=[20] + [22] * (len(doc_rows) - 1))
doc_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD_BG),
    ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 8.5),
    ("FONTSIZE", (0, 1), (-1, -1), 8.7),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("ALIGN", (0, 1), (0, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (0, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("FONTSIZE", (1, 1), (1, -1), 12),  # bigger asterisk
    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9FB6C8")),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cdd5dc")),
]))
story.append(doc_table)

# ============================================================
# PAGE 13 — Section XI Representation and Warranty
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("XI.  APPLICANT REPRESENTATION AND WARRANTY"))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "The undersigned authorized representative of the Applicant hereby declares, after diligent inquiry, that the statements and "
    "information contained in this Application and in any attached materials are true, accurate, and complete, and that no material facts "
    "have been suppressed or misstated.", WARRANTY_BODY))

story.append(Paragraph(
    "The Applicant acknowledges a continuing obligation to report to Mayflower Specialty, Ltd. as soon as practicable any material "
    "changes in such information after signing this Application and prior to issuance of the policy, and acknowledges that Mayflower "
    "Specialty shall have the right to withdraw or modify any outstanding quotation or authorization based upon such changes.", WARRANTY_BODY))

story.append(Paragraph("The Applicant further understands and acknowledges that:", WARRANTY_BODY))

warranty_items = [
    "(a) Completion of this Application does not bind coverage;",
    "(b) If a policy is issued, the Insurer will have relied upon, as representations, this Application and all supplemental materials furnished in conjunction herewith;",
    "(c) All supplemental applications, statements, and materials furnished are hereby incorporated by reference into this Application and made a part hereof;",
    "(d) This Application will be the basis of the contract and will be incorporated by reference into and made a part of the policy;",
    "(e) If a policy is issued, the Limit of Liability shall be reduced and may be completely exhausted by the payment of damages and defense costs, and the Insurer shall not be liable for any amount in excess thereof;",
    "(f) Defense costs incurred shall be applied against the Retention as provided in the policy;",
    "(g) The Applicant's failure to report to its current insurer any claim made during the current policy term, or any act, omission, or circumstance which the Applicant is aware of that may give rise to a claim, before expiration of the current policy, may create a lack of coverage;",
    "(h) Mayflower Specialty may use publicly available information to supplement this Application for purposes of risk assessment.",
]
for item in warranty_items:
    story.append(Paragraph(item, WARRANTY_LIST))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>This Application must be signed by the Chairman of the Board, Chief Executive Officer, Chief Financial Officer, President, "
    "or General Counsel of the Applicant.</b>", WARRANTY_BOLD))
story.append(Spacer(1, 14))

# Signature blocks: two columns of SignatureFieldRows
sig_widths = [CONTENT_W * 0.55, CONTENT_W * 0.45]
sig_grid = Table([
    [SignatureFieldRow("Signature of Authorized Representative", sig_widths[0] - 12), SignatureFieldRow("Date", sig_widths[1] - 12)],
    [Spacer(1, 8), Spacer(1, 8)],
    [SignatureFieldRow("Printed Name", sig_widths[0] - 12), SignatureFieldRow("Title", sig_widths[1] - 12)],
    [Spacer(1, 8), Spacer(1, 8)],
    [SignatureFieldRow("Organization", sig_widths[0] - 12), SignatureFieldRow("Email", sig_widths[1] - 12)],
], colWidths=sig_widths)
sig_grid.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(sig_grid)

# ============================================================
# PAGE 14 — Section XII Fraud Warnings
# ============================================================

story.append(PageBreak())
story.append(SectionHeader("XII.  FRAUD WARNINGS"))
story.append(Spacer(1, 3))
story.append(Paragraph("<i>Where applicable under the laws of your state.</i>", INSTR_ITAL))
story.append(Spacer(1, 4))

fraud_blocks = [
    ("All States (General)",
     "Any person who knowingly and with intent to defraud any insurance company or other person files an application for insurance or statement of claim containing any "
     "materially false information, or conceals for the purpose of misleading, information concerning any fact material thereto, commits a fraudulent insurance act, which is "
     "a crime and may be subject to civil fines and criminal penalties."),
    ("Alabama, Arkansas, District of Columbia, Louisiana, Maryland, New Mexico, Rhode Island, West Virginia",
     "Any person who knowingly (or willfully, in MD only) presents a false or fraudulent claim for payment of a loss or benefit or knowingly presents false information in an "
     "application for insurance is guilty of a crime and may be subject to fines and confinement in prison."),
    ("Arizona",
     "Misrepresentations, omissions, concealment of facts, and incorrect statements shall prevent recovery under the policy only if such are fraudulent or material to the "
     "acceptance of the risk or to the hazard assumed by the insurer."),
    ("California",
     "For your protection, California law requires the following to appear on this form: Any person who knowingly presents false or fraudulent information to obtain or "
     "amend insurance coverage or to make a claim for the payment of a loss is guilty of a crime and may be subject to fines and confinement in state prison."),
    ("Colorado",
     "It is unlawful to knowingly provide false, incomplete, or misleading facts or information to an insurance company for the purpose of defrauding or attempting to "
     "defraud the company. Penalties may include imprisonment, fines, denial of insurance, and civil damages."),
    ("District of Columbia",
     "WARNING: It is a crime to provide false or misleading information to an insurer for the purpose of defrauding the insurer or any other person. Penalties include "
     "imprisonment and/or fines. In addition, an insurer may deny insurance benefits if false information materially related to a claim was provided by the applicant."),
    ("Florida, Oklahoma",
     "Any person who knowingly and with intent to injure, defraud, or deceive any insurer files a statement of claim or an application containing any false, incomplete, or "
     "misleading information is guilty of a felony (of the third degree, FL only)."),
    ("Kansas",
     "Any person who, knowingly and with intent to defraud, presents, causes to be presented, or prepares with knowledge or belief that it will be presented to or by an "
     "insurer, purported insurer, broker or any agent thereof, any written statement as part of, or in support of, an application for insurance may be guilty of a crime and "
     "subject to fines and confinement."),
    ("Kentucky, New York, Ohio, Pennsylvania",
     "Any person who knowingly and with intent to defraud any insurance company or other person files an application for insurance or statement of claim containing any "
     "materially false information, or conceals for the purpose of misleading, information concerning any fact material thereto, commits a fraudulent insurance act, which is "
     "a crime and subjects such person to criminal and civil penalties. (In NY, also subject to a civil penalty not to exceed five thousand dollars and the stated value of the "
     "claim for each such violation.)"),
    ("Maine, Tennessee, Virginia, Washington",
     "It is a crime to knowingly provide false, incomplete, or misleading information to an insurance company for the purpose of defrauding the company. Penalties may "
     "include imprisonment, fines, and denial of insurance benefits."),
    ("New Jersey",
     "Any person who includes any false or misleading information on an application for an insurance policy is subject to criminal and civil penalties."),
    ("Oregon",
     "Any person who knowingly and with intent to defraud or solicit another to defraud the insurer by submitting an application containing a false statement as to any "
     "material fact may be violating state law."),
    ("Puerto Rico",
     "Any person who knowingly and with the intention of defrauding presents false information in an insurance application, or presents, helps, or causes the presentation "
     "of a fraudulent claim for the payment of a loss or any other benefit, or presents more than one claim for the same damage or loss, shall incur a felony subject to fines "
     "and imprisonment."),
    ("Vermont",
     "Any person who knowingly presents a false or fraudulent claim for payment of a loss or benefit or knowingly presents false information in an application for "
     "insurance may be subject to fines and confinement in prison."),
]
for title, body in fraud_blocks:
    story.append(Paragraph(title, FRAUD_TITLE))
    story.append(Paragraph(body, FRAUD_BODY))

# Bottom rule + End of Application
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cdd5dc")))
story.append(Paragraph("End of Application", END_APP))


# ---------------------------------------------------------------------------
# Build doc
# ---------------------------------------------------------------------------

OUT = "pdfs/Mayflower_AI_Liability_Supplemental_Application_v4.pdf"

doc = BaseDocTemplate(
    OUT,
    pagesize=LETTER,
    leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    title="AI Liability Supplemental Application",
    author="Mayflower Specialty, Ltd.",
    subject="Claims Made and Reported Coverage",
)

frame = Frame(
    LEFT_MARGIN, BOTTOM_MARGIN,
    CONTENT_W, PAGE_H - TOP_MARGIN - BOTTOM_MARGIN,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    id="content",
)
doc.addPageTemplates([
    PageTemplate(id="main", frames=[frame], onPage=page_header_footer),
])

doc.build(story)
print(f"Wrote: {OUT}")
