import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}
GITLAB_API = "https://gitlab.com/api/v4"

def list_pipelines(status: str = "failed") -> dict:
    """List recent pipelines for the project."""
    url = f"{GITLAB_API}/projects/{requests.utils.quote(GITLAB_PROJECT_ID, safe='')}/pipelines"
    resp = requests.get(url, headers=HEADERS, params={"status": status, "per_page": 5})
    return resp.json()

def get_pipeline_jobs(pipeline_id: int) -> dict:
    """Get all jobs for a pipeline."""
    url = f"{GITLAB_API}/projects/{requests.utils.quote(GITLAB_PROJECT_ID, safe='')}/pipelines/{pipeline_id}/jobs"
    resp = requests.get(url, headers=HEADERS)
    return resp.json()

def get_job_log(job_id: int) -> str:
    """Get the log output of a specific job."""
    url = f"{GITLAB_API}/projects/{requests.utils.quote(GITLAB_PROJECT_ID, safe='')}/jobs/{job_id}/trace"
    resp = requests.get(url, headers=HEADERS)
    return resp.text[:8000]

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

tools = [list_pipelines, get_pipeline_jobs, get_job_log]

def run_agent(user_query: str):
    print(f"\n🤖 Agent: Processing '{user_query}'\n")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query,
        config=types.GenerateContentConfig(
            tools=tools,
            system_instruction="""You are AgentOps, a CI/CD debugging assistant.
When asked about pipeline failures:
1. Call list_pipelines to find recent failed pipelines
2. Call get_pipeline_jobs to find which jobs failed
3. Call get_job_log to get the error logs
4. Analyze the logs and explain the root cause clearly
5. Suggest a specific fix the developer can implement
Always be specific about file names, line numbers, and commands to fix.""",
        ),
    )
    print(f"✅ {response.text}")
    return response.text

if __name__ == "__main__":
    run_agent("Why did my latest pipeline fail and how do I fix it?")
