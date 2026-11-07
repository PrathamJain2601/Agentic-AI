
from pydantic import BaseModel, Field
from typing import Optional
import json


# 1. Experience model
class Experience(BaseModel):
    minimum_years: Optional[float] = Field(
        default=None,
        description="Minimum years of professional experience required"
    )

    maximum_years: Optional[float] = Field(
        default=None,
        description="Maximum years of professional experience, if specified"
    )

    relevant_domains: list[str] = Field(
        default_factory=list,
        description="Relevant technical or industry domains"
    )


# 2. Job Description model
class JobDescription(BaseModel):

    title: str = Field(
        description="Job title"
    )

    responsibilities: list[str] = Field(
        default_factory=list,
        description="List of job responsibilities"
    )

    required_skills: list[str] = Field(
        default_factory=list,
        description="Mandatory technical skills"
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
        description="Additional desirable skills"
    )

    experience: Optional[Experience] = Field(
        default=None,
        description="Experience requirements for the job"
    )


# 3. System prompt
SYSTEM_PROMPT = """
You are an expert Job Description parser.

Your task is to extract structured information from
unstructured job description text.

Extract:
- Job title
- Responsibilities
- Required technical skills
- Preferred technical skills
- Experience requirements
- Relevant experience domains

Rules:
1. Extract only information explicitly mentioned in the JD.
2. Never invent or assume information.
3. Keep required and preferred skills separate.
4. Break responsibilities into individual list items.
5. Extract minimum and maximum experience in years.
6. If only minimum experience is mentioned,
   maximum_years should be null.
7. If experience is not mentioned, use null.
8. Use an empty list when a list field has no information.
9. Return only a valid JSON object.
10. Do not include Markdown or explanations outside JSON.
"""


# 4. JD parsing function
def parse_jd(jd_text: str, client, model: str) -> JobDescription:

    if not jd_text or not jd_text.strip():
        raise ValueError("Job description cannot be empty.")

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"Parse the following job description:\n\n{jd_text}"
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        max_completion_tokens=1500
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("LLM returned an empty response.")

    # Validate JSON using Pydantic
    parsed_jd = JobDescription.model_validate_json(result)

    return parsed_jd
