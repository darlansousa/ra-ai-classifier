import datetime
import os
from openai import OpenAI
from ai.model.complaint_input import ComplaintInput
from db.functions.ai_commands import retrieve_command_by
from db.functions.analysis import add_analysis
from db.functions.classification import retrieve_all_classification

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze(complaint_input: ComplaintInput):
    text = ""
    text_command = ""
    if complaint_input.title:
        text = f"{complaint_input.title}"

    if complaint_input.description:
        text = f"{text}. {complaint_input.description}"

    classification = ", ".join([item['description'] for item in await retrieve_all_classification()])
    command = await retrieve_command_by("chat_ai_command_01")

    if command:
        text_command = command['text_command']

    prompt = text_command.replace("${classifications}", classification)
    prompt = prompt.replace("${complaint}", text)

    try:
        response = client.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            prompt=prompt,
            max_tokens=30,
        )
        ai_classification = response.choices[0].text.strip()
        analysis = {
            "analyser": "chat-gpt",
            "timestamp": datetime.datetime.now(),
            "classification": ai_classification,
            "complaint_id": complaint_input.id,
            "complaint_title": complaint_input.title,
            "complaint_description": complaint_input.description
        }
        await add_analysis(analysis)
        return response.choices[0].text.strip()
    except Exception as e:
        return e



