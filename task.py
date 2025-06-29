from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import blood_test_tool, nutrition_tool, exercise_tool

# Fix 7: Create professional, ethical task descriptions
help_patients = Task(
    description=(
        "Analyze the uploaded blood test report to address the user's query: {query}\n"
        "1. Read and interpret the blood test results thoroughly\n"
        "2. Identify any abnormal values and their clinical significance\n"
        "3. Provide clear, evidence-based explanations of findings\n"
        "4. Offer appropriate medical insights while emphasizing the need for professional medical consultation\n"
        "5. Use reliable medical sources and current clinical guidelines"
    ),
    expected_output=(
        "A comprehensive blood test analysis report including:\n"
        "- Summary of key findings from the blood work\n"
        "- Explanation of any abnormal values and their potential clinical significance\n"
        "- Professional medical insights based on current evidence\n"
        "- Clear recommendations for follow-up with healthcare providers\n"
        "- Emphasis that this analysis is for educational purposes and not a substitute for professional medical advice"
    ),
    agent=doctor,
    tools=[blood_test_tool],
    async_execution=False,
)

nutrition_analysis = Task(
    description=(
        "Based on the blood test results, provide evidence-based nutritional recommendations for: {query}\n"
        "1. Analyze blood markers relevant to nutritional status\n"
        "2. Identify any nutrient deficiencies or imbalances\n"
        "3. Recommend appropriate dietary modifications\n"
        "4. Suggest meal planning strategies\n"
        "5. Only recommend supplements if clearly indicated by blood work"
    ),
    expected_output=(
        "A detailed nutrition plan including:\n"
        "- Analysis of nutrition-related blood markers\n"
        "- Specific dietary recommendations based on blood work findings\n"
        "- Meal planning suggestions and food choices\n"
        "- Supplement recommendations only if clinically indicated\n"
        "- Timeline for dietary implementation and follow-up testing recommendations"
    ),
    agent=nutritionist,
    tools=[blood_test_tool, nutrition_tool],
    async_execution=False,
)

exercise_planning = Task(
    description=(
        "Create a safe, personalized exercise plan based on blood test results for: {query}\n"
        "1. Review blood work for any exercise contraindications\n"
        "2. Assess cardiovascular and metabolic markers\n"
        "3. Design appropriate exercise intensity and duration\n"
        "4. Include safety considerations and monitoring guidelines\n"
        "5. Provide progressive exercise recommendations"
    ),
    expected_output=(
        "A comprehensive exercise plan including:\n"
        "- Safety assessment based on blood work findings\n"
        "- Specific exercise recommendations (type, intensity, duration, frequency)\n"
        "- Progressive training plan with clear milestones\n"
        "- Monitoring guidelines and warning signs to watch for\n"
        "- Recommendations for medical clearance if needed"
    ),
    agent=exercise_specialist,
    tools=[blood_test_tool, exercise_tool],
    async_execution=False,
)

verification = Task(
    description=(
        "Validate the uploaded document to ensure it's a legitimate blood test report\n"
        "1. Verify the document contains appropriate medical formatting\n"
        "2. Check for required laboratory information and reference ranges\n"
        "3. Ensure the report includes necessary patient and lab identifiers\n"
        "4. Flag any inconsistencies or missing critical information"
    ),
    expected_output=(
        "Document validation report including:\n"
        "- Confirmation of document type and legitimacy\n"
        "- Assessment of report completeness and formatting\n"
        "- Identification of any missing critical information\n"
        "- Recommendations for proceeding with analysis or requesting additional documentation"
    ),
    agent=verifier,
    tools=[blood_test_tool],
    async_execution=False
)