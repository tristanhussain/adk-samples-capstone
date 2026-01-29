import os

import google.auth

try:
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
except google.auth.exceptions.DefaultCredentialsError:
    # This is a fallback for when the user has not authenticated with Google Cloud.
    # It is intended for local development and testing.
    print(
        "Warning: Could not find default credentials. Using a fallback for local"
        " development."
    )

from . import agent