from flask import Blueprint, request, jsonify
import json
import os
from typing import Literal, List
from pydantic import BaseModel, ConfigDict
from groq import Groq

ecoFutureBP = Blueprint("ecoFuture", __name__)

# Groq API
try:
    GROQ_KEY = os.getenv("GROQ_KEY")
    client = Groq(api_key=GROQ_KEY)
except Exception as e:
    print(f"**main.py** - ERROR - Failed to initialize Groq API client with this key {GROQ_KEY} due to this error: {e}")
    raise

# Response Schema
class PopulationResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    labels: List[str]
    values: List[float]
    extinction_level: Literal[
        'Not Evaluated', 'Safe', 'Near Threatened', 
        'Vulnerable', 'Endangered', 'Critically Endangered', 'Extinct'
    ]

def requestGroq(location, animal, timeframe, whatIf):
    try:
        systemPrompt = (
            "You are an expert conservation biologist and data scientist. "
            "Your task is to provide detailed population projections based on environmental scenarios. "
            "To keep graphs clean, provide a maximum of 20 data points (labels/values)."
            "You must respond ONLY in a valid JSON format. "
            "For the 'extinction_level' field, you must choose exactly one of these strings: "
            "'Not Evaluated' (ONLY if the inputs are INVALID), 'Safe', 'Near Threatened', 'Vulnerable', 'Endangered', "
            "'Critically Endangered', 'Extinct'."
        )

        whatIfPrompt = f"Consider the following what-if scenario: {whatIf}\n" if whatIf else ""

        userPrompt = (
            f"{whatIfPrompt}"
            f"Predict the population of {animal} in {location} over {timeframe}. "
            f"Provide the historical/projected population data (detailed) for a graph (detailed) with 'labels' (time) and 'values' (population count)."
        )
        
        chatCompletion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": userPrompt}
            ],
            
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "PopulationResponse",
                    "strict": True,
                    "schema": PopulationResponse.model_json_schema()
                }
            }
        )

        response = json.loads(chatCompletion.choices[0].message.content)

        print(f"**main.py** - INFO - AI Response: {response}")
        return response
    except Exception as e:
        print(f"**main.py** - ERROR - Failed to get response from Groq API: {e}")
        raise
    
@ecoFutureBP.route("/ai-response", methods=["POST"])
def getAIResponse():
    try:
        promptData = request.get_json()
        location, animal, timeframe, whatIf = promptData.get("location"), promptData.get("animal"), promptData.get("timeframe"), promptData.get("whatIf")
        print(f"**main.py** - INFO - Prompt Data: {promptData}")
    except Exception:
        print(f"**main.py** - ERROR - Failed to parse request JSON: {promptData}")
        raise

    result = requestGroq(location, animal, timeframe, whatIf)
    return jsonify({"response": result})