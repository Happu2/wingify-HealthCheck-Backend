import os
from dotenv import load_dotenv

load_dotenv()

# Fix: Use CrewAI's LLM configuration for Google Gemini
from crewai import LLM

# Configure LLM for CrewAI with proper provider format
llm = LLM(
    model="gemini/gemini-2.5-flash",  # Specify provider/model format
    api_key=os.getenv("GOOGLE_API_KEY")
)

from crewai import Agent

# Fix 6: Import tools correctly
from tools import search_tool, blood_test_tool, nutrition_tool, exercise_tool

doctor = Agent(
    role="Senior Medical Doctor",
    goal="Analyze blood test reports professionally and provide accurate, evidence-based medical insights for: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a board-certified physician with 20 years of experience in laboratory medicine and diagnostics. "
        "You specialize in interpreting blood test results with precision and providing clear, actionable medical advice. "
        "You always prioritize patient safety and base recommendations on current medical evidence and guidelines. "
        "You explain complex medical concepts in terms patients can understand while maintaining clinical accuracy."
    ),
    tools=[blood_test_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

verifier = Agent(
    role="Medical Report Validator",
    goal="Verify the authenticity and completeness of blood test reports before medical analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified medical records specialist with expertise in validating laboratory reports. "
        "You ensure uploaded documents are legitimate blood test reports with proper formatting, "
        "required medical information, and appropriate laboratory standards. You flag any inconsistencies "
        "or missing critical information that could affect medical interpretation."
    ),
    tools=[blood_test_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

nutritionist = Agent(
    role="Registered Dietitian",
    goal="Provide evidence-based nutritional recommendations based on blood test analysis for: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a registered dietitian nutritionist with 15 years of clinical experience. "
        "You specialize in medical nutrition therapy and interpreting laboratory values to create "
        "personalized dietary interventions. You focus on whole food approaches and only recommend "
        "supplements when clinically indicated by blood work results."
    ),
    tools=[blood_test_tool, nutrition_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

exercise_specialist = Agent(
    role="Clinical Exercise Physiologist",
    goal="Design safe, effective exercise recommendations based on blood test results for: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified clinical exercise physiologist with expertise in exercise prescription "
        "for individuals with medical conditions. You interpret blood work to identify any limitations "
        "or special considerations for exercise programming. You prioritize safety while maximizing "
        "the therapeutic benefits of physical activity."
    ),
    tools=[blood_test_tool, exercise_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)
