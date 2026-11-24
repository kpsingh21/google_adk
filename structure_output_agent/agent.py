from google.adk.agents.llm_agent import Agent
from typing import Literal
from pydantic import BaseModel, Field

# class Enquiry(BaseModel):
#     name: str
#     email: str
#     interested_in:str
#     budget_inr:int

# root_agent = Agent(
#     model='gemini-3.5-flash',
#     name='enquiry_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Extract Details from the student ',
#     output_schema=Enquiry
# )


class Enquiry(BaseModel):
    name: str | None = Field(default=None, description="Student's full name, properly capitalized")
    email: str | None = Field(default=None, description="Email address exactly as written")
    interested_in: list[Literal["GenAI", "Data Science", "MLOps", "Deep Learning", "Other"]] = Field(
        description="CampusX courses the student is interested in"
    )
    budget_inr: int | None = Field(default=None, ge=0, le=500000,
        description="Total budget in rupees as a plain number. Convert '15k' to 15000")

root_agent = Agent(
    name="enquiry_agent",
    model="gemini-3.5-flash",
    description="Extracts student enquiry details from a message.",
    instruction="Read the student's message and extract their details. "
                "If something is not mentioned, leave it empty. Never guess.",
    output_schema=Enquiry,
    output_key='enquiry' #kind of memory store in python dict with key as outputkey ,can be seen as state
)