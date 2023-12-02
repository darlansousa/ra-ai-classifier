import datetime
import os
from openai import OpenAI
from ai.model.complaint_input import ComplaintInput
from db.functions.ai_commands import retrieve_command_by
from db.functions.analysis import add_analysis
from db.functions.classification import retrieve_all_classification

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def filter_classification(items, name) -> dict:
    first = None
    filtered = [item for item in items if item['name'] == name.lower()]
    others = [item for item in items if item['name'] == 'outros']
    if len(filtered) > 0:
        first = filtered[0]
    elif len(others) > 0:
        first = others[0]

    return first


async def analyze_with_gpt(complaint_input: ComplaintInput):
    text = ""
    text_command = ""
    if complaint_input.title:
        text = f"{complaint_input.title}"

    if complaint_input.description:
        text = f"{text}. {complaint_input.description}"

    items = await retrieve_all_classification()

    classification_names = ", ".join([item['name'] for item in items])
    command = await retrieve_command_by("chat_ai_command_01")

    if command:
        text_command = command['text_command']

    prompt = text_command.replace("${classifications}", classification_names)
    prompt = prompt.replace("${complaint}", text)
    try:
        response = client.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            prompt=prompt,
            max_tokens=30,
        )
        classification_name = response.choices[0].text.strip()
        classification_name = response.choices[0].text.strip()
        classification = filter_classification(items, classification_name)
        classification_name = classification['description']
        analysis = {
            "analyser": "chat-gpt",
            "timestamp": datetime.datetime.now(),
            "classification": classification_name,
            "complaint_id": complaint_input.id,
            "complaint_title": complaint_input.title,
            "complaint_description": complaint_input.description
        }
        await add_analysis(analysis)
        return classification
    except Exception as e:
        return e
