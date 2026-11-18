
import os
import re
import tempfile
from datetime import datetime
from html import escape

import gradio as gr

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

from research_agent import research_topic
from summarizer_agent import summarize_research
from report_agent import generate_report


# ==========================================
# PDF GENERATION
# ==========================================

def create_pdf(topic, report, research_data):

    fd, pdf_path = tempfile.mkstemp(
        suffix=".pdf",
        prefix="AI_Research_Report_"
    )
    os.close(fd)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=21,
        leading=27,
        textColor=colors.HexColor("#4338CA"),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=13,
        spaceAfter=7
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=15,
        spaceAfter=7
    )

    story = []

    story.append(
        Paragraph("AI RESEARCH ASSISTANT", title_style)
    )

    story.append(
        Paragraph(escape(topic), heading_style)
    )

    story.append(
        Paragraph(
            "Generated on: " + datetime.now().strftime(
                "%d %B %Y, %I:%M %p"
            ),
            styles["Italic"]
        )
    )

    story.append(Spacer(1, 15))

    # Convert basic Markdown formatting into PDF sections
    for line in report.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(escape(line[2:]), heading_style)
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(escape(line[3:]), heading_style)
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    escape(line[4:]),
                    styles["Heading3"]
                )
            )

        elif line.startswith("- ") or line.startswith("* "):
            story.append(
                Paragraph(
                    "&#8226; " + escape(line[2:]),
                    body_style
                )
            )

        else:
            story.append(
                Paragraph(escape(line), body_style)
            )

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", color=colors.grey))

    story.append(
        Paragraph("SOURCE REFERENCES", heading_style)
    )

    for i, item in enumerate(research_data, start=1):

        source_title = escape(item.get("title", "Untitled source"))
        source_url = escape(item.get("url", ""))

        story.append(
            Paragraph(
                f"[{i}] {source_title}",
                body_style
            )
        )

        story.append(
            Paragraph(source_url, body_style)
        )

    doc.build(story)

    return pdf_path


# ==========================================
# MAIN RESEARCH WORKFLOW
# ==========================================

def run_research(topic, progress=gr.Progress()):

    if not topic or not topic.strip():
        return (
            "Please enter a research topic.",
            "",
            "",
            None,
            "Please enter a valid topic."
        )

    try:

        # AGENT 1
        progress(0.15, desc="Agent 1: Searching the web...")

        research_data = research_topic(topic)

        # AGENT 2
        progress(0.40, desc="Agent 2: Analyzing research...")

        summary = summarize_research(
            research_data,
            topic
        )

        # AGENT 3
        progress(0.70, desc="Agent 3: Writing research report...")

        report = generate_report(
            topic,
            summary,
            research_data
        )

        # FORMAT SOURCES
        sources = "## Research Sources\n\n"

        for i, item in enumerate(research_data, start=1):

            title = item.get("title", "Untitled source")
            url = item.get("url", "")

            sources += f"{i}. [{title}]({url})\n\n"

        # GENERATE PDF
        progress(0.90, desc="Preparing downloadable PDF...")

        pdf_path = create_pdf(
            topic,
            report,
            research_data
        )

        progress(1.0, desc="Research completed!")

        status = (
            "### Research completed successfully!\n\n"
            f"- Sources collected: {len(research_data)}\n"
            "- Summarization completed\n"
            "- Research report generated\n"
            "- PDF ready for download"
        )

        return report, summary, sources, pdf_path, status

    except Exception as e:

        error_message = str(e)

        print("Research error:", error_message)

        return (
            f"### Research failed\n\n{error_message}",
            "",
            "",
            None,
            "Something went wrong. Check the terminal for details."
        )


# ==========================================
# CUSTOM FRONTEND DESIGN
# ==========================================

CUSTOM_CSS = """

.gradio-container {
    max-width: 1250px !important;
    margin: auto !important;
    font-family: 'Inter', sans-serif !important;
}

#hero {
    text-align: center;
    padding: 35px 20px 25px;
    border-radius: 20px;
    background: linear-gradient(
        125deg,
        #111827,
        #312e81,
        #581c87
    );
    margin-bottom: 24px;
}

#hero h1 {
    font-size: 38px !important;
    font-weight: 800 !important;
    color: white !important;
    margin-bottom: 10px;
}

#hero p {
    color: #ddd6fe !important;
    font-size: 15px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    color: white;
    padding: 7px 15px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 12px;
}

.agent-card {
    border: 1px solid var(--border-color-primary);
    border-radius: 14px;
    padding: 17px;
    min-height: 115px;
    background: var(--background-fill-secondary);
}

.agent-card h3 {
    font-size: 16px;
    margin-bottom: 8px;
}

.agent-card p {
    font-size: 13px;
    color: var(--body-text-color-subdued);
}

#research-button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 48px;
}

#status-panel {
    border-radius: 12px;
}

footer {
    display: none !important;
}

"""

# ==========================================
# GRADIO INTERFACE
# ==========================================

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="indigo",
        neutral_hue="slate"
    ),
    css=CUSTOM_CSS,
    title="AI Research Assistant"
) as demo:

    # HERO SECTION

    gr.HTML("""
        <div id="hero">
            <div class="hero-tag">
                MULTI-AGENT INTELLIGENCE PLATFORM
            </div>

            <h1>AI Research Assistant</h1>

            <p>
                Research smarter. Analyze faster.
                Generate structured reports with AI.
            </p>
        </div>
    """)

    # AGENT CARDS

    with gr.Row():

        gr.HTML("""
            <div class="agent-card">
                <h3>01 | Web Research</h3>
                <p>
                    Searches the web and collects
                    relevant information and sources.
                </p>
            </div>
        """)

        gr.HTML("""
            <div class="agent-card">
                <h3>02 | AI Summarization</h3>
                <p>
                    Analyzes findings and extracts
                    important research insights.
                </p>
            </div>
        """)

        gr.HTML("""
            <div class="agent-card">
                <h3>03 | Report Generation</h3>
                <p>
                    Creates a professional,
                    structured research report.
                </p>
            </div>
        """)

    gr.Markdown("## Start your research")

    topic_input = gr.Textbox(
        label="Research Topic",
        placeholder=(
            "Example: Applications of Generative AI "
            "in Healthcare"
        ),
        lines=3
    )

    with gr.Row():

        research_button = gr.Button(
            "Start Research",
            variant="primary",
            elem_id="research-button",
            scale=3
        )

        clear_button = gr.ClearButton(
            components=[
                topic_input,
            ],
            value="Clear Topic",
            scale=1
        )

    gr.Examples(
        examples=[
            ["Applications of Generative AI in Healthcare"],
            ["Artificial Intelligence in Education"],
            ["AI-Based Image Forgery Detection"],
            ["Computer Vision in Agriculture"],
            ["Future of Large Language Models"]
        ],
        inputs=topic_input,
        label="Try these research topics"
    )

    status_output = gr.Markdown(
        "Your research results will appear here.",
        elem_id="status-panel"
    )

    # OUTPUT TABS

    gr.Markdown("## Your Research Workspace")

    with gr.Tabs():

        with gr.Tab("Research Report"):

            report_output = gr.Markdown()

        with gr.Tab("AI Summary"):

            summary_output = gr.Markdown()

        with gr.Tab("Sources & References"):

            sources_output = gr.Markdown()

    gr.Markdown("## Download your research")

    pdf_output = gr.File(
        label="Download your research report (PDF)",
        interactive=False
    )

    research_button.click(
        fn=run_research,
        inputs=topic_input,
        outputs=[
            report_output,
            summary_output,
            sources_output,
            pdf_output,
            status_output
        ],
        show_progress="full"
    )


# ==========================================
# LAUNCH
# ==========================================

if __name__ == "__main__":

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
