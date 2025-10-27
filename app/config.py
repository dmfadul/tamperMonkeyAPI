import os


PORT = int(os.getenv("PORT", 8000))
ENV = os.getenv("ENV", "dev")

# CORS: start permissive; lock down later
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]