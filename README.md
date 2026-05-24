An AI agent that automatically diagnoses GitLab CI/CD pipeline failures using Google Gemini.

## Live Demo
🔗 https://agentops-oaj6.onrender.com

## What it does
- Connects to your GitLab project via API
- Fetches failed pipeline logs automatically
- Uses Gemini to analyze the root cause
- Suggests a specific fix with corrected code

## How to run locally

1. Clone the repo:
```bash
git clone https://github.com/sneha020902/agentops.git
cd agentops
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
GITLAB_TOKEN=your_gitlab_token
GITLAB_PROJECT_ID=your_group/your_project
GEMINI_API_KEY=your_gemini_api_key

4. Run:
```bash
python app.py
```

5. Open http://localhost:5001

## Tech Stack
- Python + Flask
- Google Gemini (function calling)
- GitLab REST API
- Deployed on Render

## License
MIT
