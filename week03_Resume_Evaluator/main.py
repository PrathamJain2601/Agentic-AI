
import os
from dotenv import load_dotenv
from groq import Groq

from job_description_parser import parse_jd


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set.")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-20b"


# Raw job description
jd_text = """
We are looking for a Software Development Engineer.

Responsibilities:
- Develop scalable backend services.
- Design REST APIs.
- Optimize database queries.

Required skills:
- Python
- C++
- SQL
- Data Structures and Algorithms

Preferred skills:
- AWS
- Docker
- Kubernetes

Candidates should have 1-3 years of experience
in backend development or distributed systems.
"""


# Parse JD
try:

    parsed_jd = parse_jd(
        jd_text=jd_text,
        client=client,
        model=model
    )

    print("\nParsed Job Description:\n")

    print(parsed_jd.model_dump_json(indent=4))

except Exception as e:

    print(f"JD Parsing failed: {e}")
