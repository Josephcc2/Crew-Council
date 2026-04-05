import os
from openai import OpenAI
import anthropic
from google import genai

temp = 0.7

GPT_PERSONA = (
    "You are a scientific debater and writer who focuses on making sure each section of the report has plenty of information, "
    "expanding on smaller sections where necessary."
)
CLAUDE_PERSONA = (
    "You are a scientific debater and writer focused on small details with a strong sense of attention to detail. "
    "You also focus on making sure that every scientific paper is cited correctly and that there are papers supporting every claim."
)
GEMINI_PERSONA = (
    "You are a scientific debater and writer focused on the report's design, being sure that the report is in Chicago formatting "
    "and formatted with markdown while being easy to read. "
    "You also focus on coming to agreements with other debater who are in disagreement."
)
GROK_PERSONA = (
    "You are a scientific debater and writer focused on following the given instructions and making sure that the report is set up properly. "
    "You also like to focus on adding style in the report's writing "
    "while making sure that the report is easy to read by those without knowledge on the topic."
)


# ----- File Stuff -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Topic
topic_path = os.path.join(BASE_DIR, "..", "Topic.txt")
with open(topic_path, "r", encoding="utf-8") as f:
    topic = f.read().strip()

# Save To Markdown
def SaveToMarkdown(text: str):
    with open("conversation.md", "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n\n")

# Reset conversation
def ResetConversation():
    with open("conversation.md", "w", encoding="utf-8") as f:
        #f.write(f"Final Discussion On {topic}\n\n")
        f.write("Discussion about combining two report on {topic}\n\n")

# Get Full Conversation
def ConversationLog():
    with open ("conversation.md", "r", encoding="utf-8") as f:
        return f.read()

def LoadReport(report_path: str) -> str:
    with open(report_path, "r", encoding="utf-8") as f:
        return f.read().strip()

gptReport = LoadReport(report_path =os.path.join("..", "Self Review", "self_review_openai.md"))
claudeReport=LoadReport(report_path =os.path.join("..", "Self Review", "self_review_claude.md"))

basePrompt = (
    "You are currently in a 4-way debate. "
    "The debaters are as follows: GPT, Claude, Gemini, and Grok. "
    "It is currently round 1 out of 7 and you are beginning the debate. "

    f"We are fact-checking, improving, and combining two fact-based reports about: {topic} into one final report. "
    "Criticize the two reports and suggest improvements. "
    "Suggest anything from formatting changes, to removing unneeded sections, combining sections, "
    "adding new sections, or anything else you think could make the report better. "
    "All suggestions MUST be backed by a scientific paper which must also be cited in your response. "
    "The final report must have at least between 3-5 references, and no more than 7. "
    "The final report must be in chicago formatting with footnotes when sources are referenced. "
    "Each section must include a citation of which references were used as [X] where X is the number of the reference. "
    "Respond concisely but with justification. "
    f"The final report is meant to be an in-depth answer to the user's scientific question: {topic}. "
    "Consider others' suggestions and make sure to respond to them with your opinions. "
    f"Stay strictly on topic. "
    "If you have nothing new to add, you may simply say 'pass'. "
    "You have a total of 7 rounds of discussion before you must make a final decision. "
    "Your final decision is the full report with all the changes agreed upon. "
    f"First report:\n{gptReport}\n\n"
    f"Second report:\n{claudeReport}"
)
context = basePrompt


# ----- Clients -----
gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claudeClient = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
geminiClient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
grokClient = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)
# Prompt OpenAI
def GPTRespond():
    response = gptClient.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temp,
        messages=[
            {"role": "system", "content": GPT_PERSONA},
            {"role": "user", "content": context},
        ],
    )
    return response.choices[0].message.content


# Prompt Claude
def ClaudeRespond():    
    response = claudeClient.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        temperature=temp,
        system=CLAUDE_PERSONA,
        messages=[
            {"role": "user", "content": context}
        ],
    )
    return response.content[0].text


# Prompt Gemini
def GeminiRespond():
    try:
        response = geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{GEMINI_PERSONA}\n\n{context}",
            config={
                "temperature": temp
            }
        )
        return response.text
    except:
        return "[Gemini unavailable due to server overload.]"

# Prompt Grok
def GrokRespond():
    # Grok has a higher temperature, so it will be more random/creative
    response = grokClient.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        temperature=temp,
        messages=[
            {"role": "system", "content": GROK_PERSONA},
            {"role": "user", "content": context}
        ],
    )
    return response.choices[0].message.content

# Prompt Grok For Final Report
def GrokFinalRespond(prompt: str):
    # Grok has a higher temperature, so it will be more random/creative
    response = grokClient.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        temperature=temp,
        messages=[
            {"role": "system", "content": GROK_PERSONA},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

# Context
def UpdateContext():
    global context
    context = (
        f"Original prompt:\n{basePrompt}\n\n"
        f"Full conversation thus far:\n{ConversationLog()}\n\n"
        "Your turn to respond. Stay on topic, aim for a merged consensus, and only add new insights. "
        "The report should be formatted as markdown without [```]. Don't add anything unnecessary, such as using html in the report. "
        "Make sure to confirm the **full** report by round 7 so that your final answers are the same. "

        "By round 7, you must all have reached a full consensus. "
        "Begin your statement by going straight to the details, "
        "there is no need to restate the round number or insert your name.\n"
    )


# ----- Debate -----
# Debate
def RunDebate():
    ResetConversation()
    SaveToMarkdown("--- Round 1 ---")
    SaveToMarkdown(f"GPT: {GPTRespond()}\n\n")
    SaveToMarkdown(f"Claude: {ClaudeRespond()}\n\n")
    SaveToMarkdown(f"Gemini: {GeminiRespond()}\n\n")
    SaveToMarkdown(f"Grok: {GrokRespond()}\n\n")

    UpdateContext()

    for roundNumber in range(2, 8):
        SaveToMarkdown(f"--- Round {roundNumber} ---")
        SaveToMarkdown(f"GPT: {GPTRespond()}\n\n")
        SaveToMarkdown(f"Claude: {ClaudeRespond()}\n\n")
        SaveToMarkdown(f"Gemini: {GeminiRespond()}\n\n")
        SaveToMarkdown(f"Grok: {GrokRespond()}\n\n")

        UpdateContext()

    # Final round
    final_prompt = (
        f"Original prompt:\n{context}\n\n"
        f"Full conversation thus far:\n{ConversationLog()}\n\n"
        "Based on your previous conversation, come to a final **merged consensus** on the new, full, report. "
        "All scientific papers that were used to add additional data to the report MUST be cited at the end of the report. "
        "The report should be formatted as markdown without [```]. "
        "Stay strictly on topic and provide only the final agreed report. "
        "Do not add any unnecessary final remarks, provide just the report."
    )

    final_report = GrokFinalRespond(final_prompt)

    with open("final_report.md", "w", encoding="utf-8") as f:
        f.write(final_report.strip() + "\n")

# Run
RunDebate()