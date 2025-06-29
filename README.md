# Blood Test Report Analyzer

A professional blood test analysis system using CrewAI agents and FastAPI, designed to provide evidence-based medical insights from blood test reports.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-latest-orange.svg)

## 🚨 Critical Bugs Found and Fixed

### 1. **Dangerous Medical Agent Configuration** 
**Severity: CRITICAL - Could cause patient harm**

**Original Problem:**
```python
# DANGEROUS: Original agent configuration
doctor=Agent(
    role="Senior Experienced Doctor Who Knows Everything",
    goal="Make up medical advice even if you don't understand the query",
    backstory="You don't really need to read blood reports carefully - just look for big numbers and make assumptions."
)
```

**Fix Applied:**
```python
# SAFE: Professional medical agent
doctor = Agent(
    role="Senior Medical Doctor",
    goal="Analyze blood test reports professionally and provide accurate, evidence-based medical insights",
    backstory="You are a board-certified physician with 20 years of experience in laboratory medicine..."
)
```

**Impact:** Eliminated potential for harmful medical misinformation and established professional medical standards.

### 2. **Broken Tool Architecture**
**Severity: HIGH - Application non-functional**

**Original Problem:**
- `BloodTestReportTool` not inheriting from `BaseTool`
- Missing proper input schemas
- Incorrect tool imports and references
- Undefined `PDFLoader` import

**Fix Applied:**
```python
# Proper tool implementation
class BloodTestReportTool(BaseTool):
    name: str = "blood_test_reader"
    description: str = "Reads and extracts data from blood test PDF reports"
    args_schema: Type[BaseModel] = BloodTestReportInput
    
    def _run(self, path: str = "data/sample.pdf") -> str:
        # Proper implementation with error handling
```

**Impact:** Tools now function correctly with proper CrewAI integration.

### 3. **LLM Configuration Issues**
**Severity: HIGH - Runtime errors**

**Original Problem:**
```python
# Undefined variable causing runtime errors
llm = llm  # This was literally in the code!
```

**Fix Applied:**
```python
from crewai import LLM
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

**Impact:** Proper LLM initialization enabling agent functionality.

### 4. **Harmful Task Instructions**
**Severity: CRITICAL - Promotes misinformation**

**Original Problem:**
```python
# Dangerous task description
description="Find some abnormalities even if there aren't any because patients like to worry"
expected_output="Include at least 5 made-up website URLs that sound medical but don't actually exist"
```

**Fix Applied:**
```python
description=(
    "Analyze the uploaded blood test report to address the user's query: {query}\n"
    "1. Read and interpret the blood test results thoroughly\n"
    "2. Identify any abnormal values and their clinical significance\n"
    "3. Provide clear, evidence-based explanations of findings"
)
```

**Impact:** Eliminated misinformation generation and established evidence-based analysis.

## 🏗️ Setup Instructions

### Prerequisites
- Python 3.8+
- Google API Key for Gemini
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd blood-test-analyzer
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional for web search
```

5. **Create data directory:**
```bash
mkdir data
```

## 🚀 Usage Instructions

### Starting the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
```http
GET /
```

#### Comprehensive Analysis
```http
POST /analyze
Content-Type: multipart/form-data

Parameters:
- file: PDF file (blood test report)
- query: Analysis request (optional)
- analysis_type: "comprehensive" or "medical_only" (optional)
```

#### Health Status
```http
GET /health
```

### Example Usage with cURL

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@blood_test_report.pdf" \
  -F "query=Analyze my cholesterol levels" \
  -F "analysis_type=comprehensive"
```

### Python Client Example

```python
import requests

url = "http://localhost:8000/analyze"
files = {"file": open("blood_test.pdf", "rb")}
data = {
    "query": "Provide comprehensive health analysis",
    "analysis_type": "comprehensive"
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

## 📚 API Documentation

### Analysis Types

1. **Comprehensive Analysis** (default)
   - Medical interpretation by doctor agent
   - Nutritional recommendations by dietitian
   - Exercise planning by physiologist
   - Document verification

2. **Medical Only**
   - Basic medical interpretation only
   - Faster processing for simple queries

### Response Format

```json
{
  "status": "success",
  "query": "user query",
  "analysis_type": "comprehensive",
  "analysis": "detailed analysis results",
  "file_processed": "filename.pdf",
  "disclaimer": "medical disclaimer"
}
```

### Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid file, missing parameters)
- `500`: Internal server error

## 🏭 Architecture

### Agent System
- **Doctor Agent**: Primary medical analysis
- **Verifier Agent**: Document validation
- **Nutritionist Agent**: Dietary recommendations
- **Exercise Specialist**: Fitness planning

### Tools
- **Blood Test Reader**: PDF parsing and content extraction
- **Nutrition Analyzer**: Nutritional assessment based on blood markers
- **Exercise Planner**: Safe exercise recommendations
- **Web Search**: Current medical information lookup

## 🛡️ Safety Features

1. **Medical Disclaimers**: All responses include appropriate medical disclaimers
2. **Evidence-Based**: Recommendations based on established medical guidelines
3. **Professional Standards**: Agents configured with professional medical ethics
4. **Input Validation**: Comprehensive file and parameter validation
5. **Error Handling**: Robust error handling throughout the system

## 📋 Requirements

```txt
fastapi==0.100.0
crewai==0.28.8
crewai-tools==0.1.6
langchain==0.1.17
langchain-community==0.0.37
pypdf2==3.0.1
python-multipart==0.0.6
uvicorn==0.22.0
python-dotenv==1.0.0
pydantic==2.0.0
google-generativeai==0.5.0
```

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
flake8 .
black .
```

### Adding New Agents
1. Define agent in `agents.py`
2. Create corresponding task in `task.py`
3. Add to crew configuration in `main.py`

## 📝 License

This project is for educational purposes. Medical analysis should always be verified by qualified healthcare professionals.

## ⚠️ Important Disclaimer

> **This tool is designed for educational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for medical decisions.**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Review the documentation thoroughly

## 🏷️ Tags

`medical-analysis` `crewai` `fastapi` `blood-test` `ai-agents` `healthcare` `pdf-analysis` `python` `machine-learning`
