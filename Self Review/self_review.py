import os
from openai import OpenAI
from anthropic import Anthropic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Topic
topic_path = os.path.join(BASE_DIR, "..", "Topic.txt")
with open(topic_path, "r", encoding="utf-8") as f:
    topic = f.read().strip()

# OpenAI
# Reviewed Report
report_path = os.path.join(BASE_DIR, "..", "First Debate", "first_debate_report_openai.md")
with open(report_path, "r", encoding="utf-8") as f:
    report_openai = f.read()
# OG Report
og_report_path = os.path.join(BASE_DIR, "..", "crew_council", "final_report.md")
with open(og_report_path, "r", encoding="utf-8") as f:
    og_report_openai = f.read()
# Convo
conversation_path = os.path.join(BASE_DIR, "..", "First Debate", "conversation_openai.md")
with open(conversation_path, "r", encoding="utf-8") as f:
    conversation_openai = f.read()

# Claude
# Reviewed Report
report_path = os.path.join(BASE_DIR, "..", "First Debate", "first_debate_report_claude.md")
with open(report_path, "r", encoding="utf-8") as f:
    report_claude = f.read()
# OG Report
og_report_path = os.path.join(BASE_DIR, "..", "crew_council_claud", "final_report.md")
with open(og_report_path, "r", encoding="utf-8") as f:
    og_report_claude = f.read()
# Convo
conversation_path = os.path.join(BASE_DIR, "..", "First Debate", "conversation_claude.md")
with open(conversation_path, "r", encoding="utf-8") as f:
    conversation_claude = f.read()

og_prompt = (
    "Review the context you got and create a full report based on the provided scientific papers. "
    "Do not create a section for each paper, instead use the information from all of the papers"
    "combined to create your report. "
    f"Make sure the report is detailed and contains any and all relevant information to {topic}. "
    "Assume that the reader of your report does not know much about the topic, so explain"
    "systems that they would not be familliar with. "
    "Do not use information that is not given from the research papers. "
    "expected_output: >\n"
    f"A fully fledged report about {topic} with the main topics, each with a full section of information. "
    "Formatted as markdown without '```'"
    "The report must be in chicago formatting with footnotes when sources are referenced. "
)

QUERY_OPENAI = (
    # pass in ALL of their previous instruction from the crew
    "You were originally given the following instrctions to create a report.\n\n"
    f"Original instructions:\n{og_prompt}\n\n"
    f"The topic is as follows:\n{topic}\n\n"
    f"The original report that you created is as follows:\n{og_report_openai}\n\n"

    "Google Gemini and Grok revised your report, fact-checking the report and adding new content.\n\n"
    f"Gemini and Grok's conversation is as follows:\n{conversation_openai} \n\n"
    f"The modified report is as followed:\n{report_openai}\n\n"
    "Revise the report that Gemini and Grok made based on your original instructions. "
    "Do not add any unnecessary final remarks, provide just the report."
)
QUERY_CLAUDE = (
    # pass in ALL of their previous instruction from the crew
    "You were originally given the following instrctions to create a report.\n\n"
    f"Original instructions:\n{og_prompt}\n\n"
    f"The topic is as follows:\n{topic}\n\n"
    f"The original report that you created is as follows:\n{og_report_claude}\n\n"

    "Google Gemini and Grok revised your report, fact-checking the report and adding new content.\n\n"
    f"Gemini and Grok's conversation is as follows:\n{conversation_claude} \n\n"
    f"The modified report is as followed:\n{report_claude}\n\n"
    "Revise the report that Gemini and Grok made based on your original instructions. "
    "Do not add any unnecessary final remarks, provide just the report."
)

openai_client = OpenAI()
anthropic_client = Anthropic()

# OpenAI
def ChatGPTResponse():
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "goal: >\n"
                    f"Create detailed reports based on {topic} data analysis and research findings using easy to understand language.\n\n"
                    "backstory: >\n"
                    "You're a meticulous analyst with a keen eye for detail. You're known for "
                    "your ability to turn complex data into clear and concise reports, making "
                    "it easy for others to understand and act on the information you provide. "
                    "You also like to focus on making sure each section of the report has plenty of information, "
                    "expanding on smaller sections where necessary."
                )
            },
            {
                "role": "user",
                "content": QUERY_OPENAI
            }
        ]
    )
    text = response.choices[0].message.content
    print("GPT Finished Self Review")
    return text

# Anthropic
def ClaudeRespond():
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        system=(
            "goal: >\n"
            f"Create detailed reports based on {topic} data analysis and research findings using easy to understand language.\n\n"
            "backstory: >\n"
            "You're a meticulous analyst with a keen eye for detail. You're known for "
            "your ability to turn complex data into clear and concise reports, making "
            "it easy for others to understand and act on the information you provide. "
            "You like to focus on small details with a strong sense of attention to detail. "
            "You also focus on making sure that every scientific paper is cited correctly and that there are papers supporting every claim."
        ),
        messages=[
            {
                "role": "user",
                "content": QUERY_CLAUDE
            }
        ]
    )

    text = response.content[0].text
    print("Claude Finished Self Review")
    return text

openai_response = ChatGPTResponse()
claude_response = ClaudeRespond()

with open("self_review_openai.md", "w", encoding="utf-8") as f:
        f.write(openai_response)
with open("self_review_claude.md", "w", encoding="utf-8") as f:
        f.write(claude_response)