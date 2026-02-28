from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI(title="OpenAPI Mock Generator")

# Initialize OpenAI client once
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/generate-sandbox")
async def generate_sandbox(file: UploadFile = File(...)):
    """
    Accepts an OpenAPI spec file and generates:
    1. NodeRED mock endpoints JSON
    2. Postman collection JSON
    """

    # Read uploaded file content
    try:
        content_bytes = await file.read()
        file_content = content_bytes.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    # Build prompt for GPT
    prompt = f"""
You are an agent that generates mock APIs and Postman collections from OpenAPI specs.

OpenAPI Specification:
{file_content}

Instructions:
1. Generate a NodeRED script (JSON format) that can be imported into NodeRED to create mock endpoints.
2. Generate a Postman collection (JSON format) that can be imported into Postman to test all endpoints.
3. Respond in a JSON object with two keys: 
   - "nodered": <NodeRED JSON string>
   - "postman": <Postman collection JSON string>
"""

    # Call OpenAI chat API
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You understand OpenAPI specifications and generate outputs as instructed."},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API call failed: {str(e)}")

    # Extract GPT response
    assistant_content = response.choices[0].message.content

    # Try to parse JSON from GPT output
    try:
        parsed = json.loads(assistant_content)
        nodered_json = parsed.get("nodered")
        postman_json = parsed.get("postman")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Assistant output is not valid JSON:\n{assistant_content}")

    # Return both files content as JSON
    return JSONResponse(content={
        "nodered": nodered_json,
        "postman": postman_json
    })
