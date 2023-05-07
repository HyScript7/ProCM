from socket import gethostname

from decouple import config

# Hostname - For when we need to figure out which node we are running on; This variable is passed to the template
HOSTNAME: str = gethostname()

# Hash Salting
PASSWORD_SALT = config("PASSWORD_SECRET", f"{HOSTNAME}_CH4NG3_M3")

# Flask Configuration
FLASK_SECRET: str = config("FLASK_SECRET", "CH4NG3_M3")
FLASK_SESSION_LIFETIME: int = int(config("FLASK_SESSION_LIFETIME", 30))

# Database Authentication
MONGO_HOST: str = config("MONGO_HOST", "localhost")
try:
    MONGO_PORT: int = int(config("MONGO_PORT", 27017))
except ValueError:
    MONGO_PORT: int = 27017
MONGO_USER: str = config("MONGO_USER", "root")
MONGO_PASS: str = config("MONGO_PASS", "root")
MONGO_SRV: bool = config("MONGO_SRV", "false").lower() == "true"

# This gibberish builds the full mongo connection string from the above parsed variables
MONGO_URI: str = f"mongodb{'+srv' if MONGO_SRV else ''}://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}{(':' + str(MONGO_PORT)) if not MONGO_SRV else ''}"

# Database configuration
PCM_DATABASE = config("PCM_DATABASE", "ProCM")
PCM_COLLECTION_USERS = "PCM_" + config("PCM_COLLECTION_USERS", "Users")
PCM_COLLECTION_PROJECTS = "PCM_" + \
    config("PCM_COLLECTION_ARTICLES", "Projects")
PCM_COLLECTION_POSTS = "PCM_" + config("PCM_COLLECTION_DISCUSSIONS", "Posts")
PCM_COLLECTION_GROUPS = "PCM_" + config("PCM_COLLECTION_GROUPS", "Groups")
PCM_COLLECTION_COMMENTS = "PCM_" + \
    config("PCM_COLLECTION_COMMENTS", "Comments")

REGISTRATION_ENABLED: bool = config("REGISTRATION", "false").lower() == "true"

# Branding
BRAND: str = config("BRAND", "ProCM")

# Projects API Token
GITHUB_TOKEN: str = config("GIT_TOKEN", None)
if GITHUB_TOKEN is None:
    raise ValueError("No github token provided!")
