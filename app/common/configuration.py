from decouple import config
from socket import gethostname

# Hostname - For when we need to figure out which node we are running on; This variable is passed to the template
HOSTNAME: str = gethostname()

# Hash Salting
PASSWORD_SALT = config("PASSWORD_SECRET", f"{HOSTNAME}_CH4NG3_M3")

# Flask Configuration
FLASK_SECRET: str           = config("FLASK_SECRET", "CH4NG3_M3")
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
MONGO_URI: str  = f"mongodb{'+srv' if MONGO_SRV else ''}://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}{(':' + str(MONGO_PORT)) if not MONGO_SRV else ''}"

# Database configuration
PCM_DATABASE               = config("PCM_DATABASE", "ProCM")
PCM_COLLECTION_USERS       = config("PCM_USERS", "Users")
PCM_COLLECTION_PROJECTS    = config("PCM_ARTICLES", "Projects")
PCM_COLLECTION_POSTS       = config("PCM_DISCUSSIONS", "Posts")
