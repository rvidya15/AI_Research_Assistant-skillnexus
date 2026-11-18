
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_report(topic, summary, research_data):

    print("Agent 3: Generating research report...")

    sources = ""

    for i, item in enumerate(research_data, start=1):

        sources += f"""
        [{i}] {item['title']}
        Link: {item['url']}
        """

    prompt = f"""
    You are a professional academic research report writer.

    Research Topic: {topic}

    Research Summary:
    {summary}

    Available Sources:
    {sources}

    Generate a structured research report using
    the following sections:

    1. Title
    2. Abstract
    3. Introduction
    4. Research Findings
    5. Key Insights
    6. Challenges and Limitations
    7. Conclusion
    8. References

    Instructions:
    - Use professional language.
    - Make the report easy to understand.
    - Use headings and bullet points.
    - Do not invent statistics or citations.
    - Cite sources using their reference numbers.
    - Clearly distinguish evidence from suggestions.
    """

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": "You are a professional academic research report writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        report = response.choices[0].message.content

        print("Agent 3: Report completed!")

        return report

    except Exception as e:

        print("Report generation error:", str(e))

        raise
