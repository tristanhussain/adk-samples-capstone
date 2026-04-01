import os
import google.auth

try:
    _, project_id = google.auth.default()
except Exception:
    project_id = "your-default-project"

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id or "your-default-project")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

from app.agent import root_agent
