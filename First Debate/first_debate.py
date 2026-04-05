import os
from google import genai
from openai import OpenAI # For Grok

geminiPersonality = (
    "You are a scientific debater and writer focused on the report's design, being sure that the report is in Chicago formatting "
    "and formatted with markdown while being easy to read. "
    "You also focus on coming to agreements with other debater who are in disagreement."
)
grokPersonality = (
    "You are a scientific debater and writer focused on following the given instructions and making sure that the report is set up properly. "
    "You also like to focus on adding style in the report's writing "
    "while making sure that the report is easy to read by those without knowledge on the topic."
)

# Set up clients
geminiClient = genai.Client()
grokClient = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

OPENAI_MD = "conversation_openai.md"
CLAUDE_MD = "conversation_claude.md"

# Topic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
topic_path = os.path.join(BASE_DIR, "..", "Topic.txt")
with open(topic_path, "r", encoding="utf-8") as f:
    topic = f.read().strip()

# Save To Markdown
def SaveToMarkdown(path: str, text: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n\n")

# Get Full Conversation To Update Gemini and Grok's Context
def ConversationLog(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# Prompt Gemini
def GeminiRespond(context: str, md_path: str):
    response = geminiClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=context,
        config={
            "system_instruction": (
                geminiPersonality
            )
        }
    )
    text = response.text if response.text is not None else "[No response from Gemini]"
    print("Gemini sent a message")
    SaveToMarkdown(md_path, "**Gemini:** " + text)
    return text

# Prompt Grok
def GrokRespond(context: str, md_path: str):
    # Grok has a higher temperature, so it will be more random/creative
    response = grokClient.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        messages=[
            {"role": "system", "content": grokPersonality}, # Personality
            {"role": "user", "content": context}
        ],
        temperature=0.8
    )
    text = response.choices[0].message.content
    print("Grok sent a message")
    SaveToMarkdown(md_path, "**Grok:** " + text)
    return text

def LoadReport(report_path: str) -> str:
    with open(report_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def RunDebate(model: str, report_path: str, output_report_name: str):
    report = LoadReport(report_path)

    md_path = CLAUDE_MD if model == "claude" else OPENAI_MD

    base_prompt = (
        f"We are fact-checking and improving a fact-based report about: {topic}. "
        "Criticize the report and suggest improvements. "
        "Feel free to suggest anything from formatting changes, to removing unneeded sections, combining sections, "
        "adding new sections, or anything else you think could make the report better. "
        "All suggestions MUST be backed by a scientific paper which must also be cited in your response. "
        "The report must be in chicago formatting with footnotes when sources are referenced. "
        "Respond concisely but with justification. "
        "You are making changes to the report, not entirely rewriting it. "
        "This report is meant to be an in-depth answer to the user's scientific question. "
        "Consider others' suggestions and make sure to respond to them with your opinions. "
        f"Stay strictly on topic. Reminder, the user is asking about {topic}. "
        "If you have nothing new to add, you may simply say 'pass'. "
        "You have a total of 5 rounds of discussion before you must make a final decision. "
        "Your final decision is the full report with all the changes agreed upon. "
        f"This is the report: {report}"
    )

    # Reset conversation
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"Gemini and Grok report critiques about {topic}\n\n")

    gemini_context = base_prompt
    grok_context = base_prompt

    # Round 1
    SaveToMarkdown(md_path, f"--- Round 1 ---")
    GeminiRespond(gemini_context, md_path)
    GrokRespond(grok_context, md_path)

    for round_number in range(2, 6):
        SaveToMarkdown(md_path, f"--- Round {round_number} ---")

        # Gemini response, sees Grok's input
        gemini_context = (
            f"Original prompt:\n{base_prompt}\n\n"
            f"Full conversation thus far:\n{ConversationLog(md_path)}\n\n"
            "Your turn to respond. Stay on topic, aim for a merged consensus, and only add new insights. "
            "You have a total of 5 rounds of discussion before you have to come to an agreement with Grok. "
            f"It is currently round {round_number}. "
            "The report should be formatted as markdown without [```]. Don't add anything unnecessary, such as using html in the report. "
            "Make sure to confirm the **full** report by round 5 so that your final answers are the same. "
            "If nothing new, say 'pass'."
        )
        GeminiRespond(gemini_context, md_path)

        # Grok responds, sees Gemini's input
        grok_context = (
            f"Original prompt:\n{base_prompt}\n\n"
            f"Full conversation thus far:\n{ConversationLog(md_path)}\n\n"
            "Your turn to respond. Stay on topic, aim for a merged consensus, and only add new insights. "
            "You have a total of 5 rounds of discussion before you have to come to an agreement with Gemini. "
            f"It is currently round {round_number}. "
            "The report should be formatted as markdown without [```]. Don't add anything unnecessary, such as using html in the report. "
            "Make sure to confirm the **full** report by round 5 so that your final answers are the same. "
            "If nothing new, say 'pass'."
        )
        GrokRespond(grok_context, md_path)

    # Final round: Ask both to agree on a final list
    SaveToMarkdown(md_path, "--- Final Agreement ---")

    final_prompt = (
        f"Original prompt:\n{base_prompt}\n\n"
        f"Full conversation thus far:\n{ConversationLog(md_path)}\n\n"
        "Based on your previous conversation, come to a final **merged consensus** on the new, full, report. "
        "All scientific papers that were used to add additional data to the report MUST be cited at the end of the report. "
        "The report should be formatted as markdown without [```]. "
        "Stay strictly on topic and provide only the final agreed report. "
        "Do not add any unnecessary final remarks, provide just the report. "
        "If you have no further changes, simply confirm the report."
    )

    final_report = GrokRespond(final_prompt, md_path)

    with open(output_report_name, "w", encoding="utf-8") as f:
        f.write(final_report.strip() + "\n")

# --- Begin Debate ---

# First run (Claude report)
RunDebate(
    model="claude",
    report_path=os.path.join("..", "crew_council_claud", "final_report.md"),
    output_report_name="first_debate_report_claude.md"
)

# Second run (OpenAI report)
RunDebate(
    model="openai",
    report_path=os.path.join("..", "crew_council", "final_report.md"),
    output_report_name="first_debate_report_openai.md"
)
