# ProCM

Jednoduchý Content Management projekt napsaný v flask frameworku pro python.
Tento projekt je závěrečnou prací Štefana Prokopa pro rok 2023 na G+SOŠ Rokycany.

## Setup

1. Create a new virtual environment
2. Activate the new virtual environment
3. Install requirements: `pip install -r ./app/requirements.txt`
4. Copy config: `cp ./app/.env_example ./app/.env`
5. Configure database: `vim ./app/.env`
6. Run server: `gunicorn main:app`
