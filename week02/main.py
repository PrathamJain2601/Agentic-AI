import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from pydantic import BaseModel
from typing import Optional, Literal

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=api_key)
model="openai/gpt-oss-20b" 

class Ticket(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    issue: Optional[str] = None

class TicketResponse(BaseModel):
    status: Literal["success", "need_information"]
    message: str
    ticket: Optional[Ticket] = None
    missing_fields: list[str] = []

schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object",
    "schema": schema
}


message_system = {
    "role": "system",
    "content": """
Extract customer support ticket information.

Required fields:
- name
- email
- issue

Rules:
- Extract only explicitly provided information.
- Never invent missing information.
- Return only a valid JSON object.
- Use null for missing fields.
- Follow the requested output structure.

Expected format:
{
    "name": "Pratham",
    "email": null,
    "issue": "Phone is not working properly"
}
"""
}

message = {
    "role": "user",
    "content": "Hello My name is Pratham. I have a phone which is not working properly. My address is Ludhiana. I have tried to fix it but I am not able to fix it. Can you please help me to fix my phone?"
}

messages = [message_system, message]

try:
    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

    result = response.choices[0].message.content

    if not result:
        raise ValueError("LLM returned an empty response.")

    print("\nLLM Raw Response:")
    print(result)

    # 5. Validate response using Pydantic
    extracted = Ticket.model_validate_json(result)

    print("\nExtracted Information:")
    print(extracted.model_dump())

    # 6. Let Python determine missing fields
    ticket_data = extracted.model_dump()

    missing_fields = [
        field
        for field, value in ticket_data.items()
        if value is None or not value.strip()
    ]

    # 7. Application business logic
    if missing_fields:

        print("\nTicket cannot be created yet.")

        print("Missing information:", missing_fields)

        print(
            "Please provide:",
            ", ".join(missing_fields)
        )

    else:

        # Ticket is complete
        print("\nTicket created successfully!")

        print(json.dumps(ticket_data, indent=4))


except (json.JSONDecodeError, ValidationError) as e:

    print("Invalid LLM response:", e)

except Exception as e:

    print("Something went wrong:", e)
