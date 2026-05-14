"""
Shared Pydantic models used across multiple crews.
"""
from pydantic import BaseModel, Field


class SQLQuery(BaseModel):
    """SQL query model for structured output from query generator"""
    sqlquery: str = Field(..., description="The raw sql query for the user input")


class ReviewedSQLQuery(BaseModel):
    """Reviewed SQL query model for structured output from query reviewer"""
    reviewed_sqlquery: str = Field(
        ..., description="The reviewed sql query for the raw sql query"
    )


class ComplianceReport(BaseModel):
    """Compliance report model for structured output from compliance checker"""
    report: str = Field(
        ..., description="Comprehensive compliance report with security assessment"
    )


class QueryInterpretation(BaseModel):
    """Query interpretation model for business-friendly explanations"""
    title: str = Field(..., description="Title of the interpretation")
    summary: str = Field(
        ..., description="A brief summary of the query results in business terms"
    )
    insights: str = Field(
        ..., description="Key insights and patterns found in the data"
    )
    recommendations: str = Field(
        ..., description="Actionable recommendations based on the results"
    )
