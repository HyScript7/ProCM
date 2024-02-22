FROM python:3.10.11

WORKDIR /app
COPY . .

# Install requirements
RUN ["pip", "install", "--upgrade", "pip"]

RUN ["python", "-m", "pip", "install", "--no-cache-dir", "-r", "./requirements.txt"]

WORKDIR /app/static
RUN ["./download_libraries.sh"]

WORKDIR /app

# Setup Env
ENV PASSWORD_SECRET=ProCM
ENV FLASK_SECRET=SessionSecret
ENV FLASK_SESSION_LIFETIME=1400
ENV MONGO_HOST=db
ENV MONGO_PORT=27017
ENV MONGO_USER=root
ENV MONGO_PASS=root
ENV MONGO_SRV=false
ENV PCM_DATABASE=ProCM
ENV PCM_COLLECTION_USERS=Users
ENV PCM_COLLECTION_GROUPS=Groups
ENV PCM_COLLECTION_PROJECTS=Projects
ENV PCM_COLLECTION_POSTS=Posts
ENV PCM_COLLECTION_COMMENTS=Comments
ENV REGISTRATION=true
ENV BRAND=ProCM
ENV GIT_TOKEN=0
ENV GIT_USERNAME=0

# Expose ports
EXPOSE 8000

# Run the application
CMD ["gunicorn", "main:app", "-b", "0.0.0.0"]
