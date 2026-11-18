
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_research(research_data, topic):

    print("Agent 2: Summarizing research...")

    context = ""

    for i, item in enumerate(research_data, start=1):

        context += f"""
        Source {i}
        Title: {item['title']}
        Content: {item['body']}
        URL: {item['url']}
        """

    prompt = f"""
    You are an expert research summarization agent.

    Research Topic: {topic}

    Analyze the following web research:

    {context}

    Your tasks:
    1. Identify the important findings.
    2. Remove irrelevant information.
    3. Identify common themes.
    4. Mention conflicting information if present.
    5. Do not invent facts.
    6. Preserve source references such as [1], [2].

    Provide a clear and organized summary.
    """

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert research analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        summary = response.choices[0].message.content

        print("Agent 2: Summary completed!")

        return summary

    except Exception as e:

        print("Summarization error:", str(e))

        raise
