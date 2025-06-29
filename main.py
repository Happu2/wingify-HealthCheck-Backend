from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
# Fix 8: Import all necessary agents and tasks
from agents import doctor, nutritionist, exercise_specialist, verifier
from task import help_patients, nutrition_analysis, exercise_planning, verification

app = FastAPI(title="Professional Blood Test Report Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf", analysis_type: str = "comprehensive"):
    """Run the medical analysis crew"""
    try:
        # Fix 9: Create different crew configurations based on analysis type
        if analysis_type == "comprehensive":
            medical_crew = Crew(
                agents=[verifier, doctor, nutritionist, exercise_specialist],
                tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
                process=Process.sequential,
                verbose=True
            )
        elif analysis_type == "medical_only":
            medical_crew = Crew(
                agents=[doctor],
                tasks=[help_patients],
                process=Process.sequential,
                verbose=True
            )
        else:
            medical_crew = Crew(
                agents=[doctor],
                tasks=[help_patients],
                process=Process.sequential,
                verbose=True
            )
        
        # Update task context with file path
        context = {'query': query, 'file_path': file_path}
        result = medical_crew.kickoff(context)
        return result
        
    except Exception as e:
        raise Exception(f"Error running medical analysis: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Professional Blood Test Report Analyzer API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive analysis of my blood test report"),
    analysis_type: str = Form(default="comprehensive")
):
    """Analyze blood test report and provide professional health recommendations"""
    
    # Fix 10: Add proper file validation
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            f.write(content)
        
        # Validate query
        if not query or query.strip() == "":
            query = "Provide a comprehensive analysis of my blood test report"
            
        # Process the blood report
        response = run_crew(
            query=query.strip(), 
            file_path=file_path,
            analysis_type=analysis_type
        )
        
        return {
            "status": "success",
            "query": query,
            "analysis_type": analysis_type,
            "analysis": str(response),
            "file_processed": file.filename,
            "disclaimer": "This analysis is for educational purposes only and should not replace professional medical advice. Please consult with your healthcare provider for medical decisions."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Blood Test Analyzer",
        "agents_available": ["doctor", "nutritionist", "exercise_specialist", "verifier"],
        "analysis_types": ["comprehensive", "medical_only"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
