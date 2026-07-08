from pydantic import BaseModel, Field
from typing import List

class EducationEntry(BaseModel):
    Degree: str = Field(description="Degree title and major")
    School: str = Field(description="Name of university or institution")
    Location: str = Field(description="Location of school, e.g. City, State")
    GPA: str = Field(description="GPA or grade, e.g. 3.8/4.0")
    Year: str = Field(description="Graduation year, e.g. 2026")

class ProjectEntry(BaseModel):
    Role: str = Field(description="Name of the Project, Consulting Audit, or Case Study")
    Company: str = Field(description="Context, e.g. 'MBA Capstone Project' or 'Financial Modeling Case'")
    Duration: str = Field(description="Duration period, e.g. 'Jan 2026 - May 2026' (NO seasons)")
    Achievements: List[str] = Field(description="List of strategic or quantitative bullet points describing actions and methodologies")

class ResumeSchema(BaseModel):
    Name: str = Field(description="Full candidate name")
    Email: str = Field(description="Email address")
    Phone: str = Field(description="Phone number")
    LinkedIn: str = Field(description="LinkedIn URL")
    Location: str = Field(description="City/Country")
    Summary: str = Field(description="A highly ambitious, strategic summary of a recent PG/MBA graduate")
    Experience: List[ProjectEntry] = Field(description="Strategic consulting projects, capstones, or case studies")
    Skills: List[str] = Field(description="Core professional competencies and tools")
    Education: List[str] = Field(description="Education history details and target certifications")
