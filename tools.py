# ============================================================================
# FIXED tools.py
# ============================================================================

import os
from dotenv import load_dotenv
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

load_dotenv()

from crewai_tools import SerperDevTool

# Creating search tool
search_tool = SerperDevTool()

# Fix 1: Import PDFLoader properly
try:
    from langchain_community.document_loaders import PyPDFLoader as PDFLoader
except ImportError:
    from langchain.document_loaders import PyPDFLoader as PDFLoader

# Fix 2: Create proper tool input schema
class BloodTestReportInput(BaseModel):
    """Input for BloodTestReportTool."""
    path: str = Field(default="data/sample.pdf", description="Path to the PDF file containing the blood test report")

# Fix 3: Make BloodTestReportTool inherit from BaseTool
class BloodTestReportTool(BaseTool):
    name: str = "blood_test_reader"
    description: str = "Reads and extracts data from blood test PDF reports"
    args_schema: Type[BaseModel] = BloodTestReportInput

    def _run(self, path: str = "data/sample.pdf") -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file content
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
            
            # Load PDF using the proper loader
            loader = PDFLoader(file_path=path)
            docs = loader.load()

            full_report = ""
            for data in docs:
                # Clean and format the report data
                content = data.page_content
                
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                    
                full_report += content + "\n"
                
            return full_report if full_report.strip() else "No content found in PDF"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

# Create tool instance
blood_test_tool = BloodTestReportTool()

# Fix 4: Implement proper nutrition and exercise tools
class NutritionAnalysisInput(BaseModel):
    """Input for NutritionTool."""
    blood_report_data: str = Field(description="Blood test report data to analyze")

class NutritionTool(BaseTool):
    name: str = "nutrition_analyzer"
    description: str = "Analyzes blood test results and provides nutrition recommendations"
    args_schema: Type[BaseModel] = NutritionAnalysisInput
    
    def _run(self, blood_report_data: str) -> str:
        """Analyze blood report and provide nutrition recommendations"""
        try:
            # Basic nutrition analysis based on common blood markers
            recommendations = []
            
            # Convert to lowercase for easier matching
            data_lower = blood_report_data.lower()
            
            # Check for common deficiencies and imbalances
            if any(term in data_lower for term in ['hemoglobin', 'hgb', 'hb']):
                if any(term in data_lower for term in ['low', 'below', 'deficient']):
                    recommendations.append("Consider iron-rich foods: spinach, red meat, lentils, fortified cereals")
            
            if 'vitamin d' in data_lower or 'vit d' in data_lower:
                if any(term in data_lower for term in ['low', 'deficient', 'insufficient']):
                    recommendations.append("Increase vitamin D: fatty fish, fortified milk, sunlight exposure")
            
            if 'cholesterol' in data_lower:
                if any(term in data_lower for term in ['high', 'elevated']):
                    recommendations.append("Heart-healthy diet: reduce saturated fats, increase fiber, omega-3 fatty acids")
            
            if 'glucose' in data_lower or 'blood sugar' in data_lower:
                if any(term in data_lower for term in ['high', 'elevated']):
                    recommendations.append("Blood sugar management: complex carbohydrates, regular meals, limit refined sugars")
            
            if not recommendations:
                recommendations.append("Maintain a balanced diet with variety of fruits, vegetables, lean proteins, and whole grains")
            
            return "Nutrition Recommendations:\n" + "\n".join([f"• {rec}" for rec in recommendations])
            
        except Exception as e:
            return f"Error in nutrition analysis: {str(e)}"

class ExerciseAnalysisInput(BaseModel):
    """Input for ExerciseTool."""
    blood_report_data: str = Field(description="Blood test report data to analyze for exercise planning")

class ExerciseTool(BaseTool):
    name: str = "exercise_planner"
    description: str = "Creates exercise recommendations based on blood test results"
    args_schema: Type[BaseModel] = ExerciseAnalysisInput
    
    def _run(self, blood_report_data: str) -> str:
        """Create exercise plan based on blood analysis"""
        try:
            recommendations = []
            data_lower = blood_report_data.lower()
            
            # Check for conditions that affect exercise
            if any(term in data_lower for term in ['hemoglobin', 'hgb']) and any(term in data_lower for term in ['low', 'anemia']):
                recommendations.append("Start with light exercise: walking, gentle yoga. Gradually increase intensity as iron levels improve")
            
            if 'cholesterol' in data_lower and any(term in data_lower for term in ['high', 'elevated']):
                recommendations.append("Cardiovascular exercise: 30 minutes moderate activity 5 days/week (walking, swimming, cycling)")
            
            if 'glucose' in data_lower and any(term in data_lower for term in ['high', 'diabetes']):
                recommendations.append("Blood sugar management: regular exercise, resistance training 2-3x/week, post-meal walks")
            
            # General recommendations
            recommendations.extend([
                "Strength training: 2-3 sessions per week targeting major muscle groups",
                "Flexibility: Daily stretching or yoga",
                "Cardio: 150 minutes moderate or 75 minutes vigorous activity per week"
            ])
            
            return "Exercise Plan:\n" + "\n".join([f"• {rec}" for rec in recommendations])
            
        except Exception as e:
            return f"Error in exercise planning: {str(e)}"

# Create tool instances
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()