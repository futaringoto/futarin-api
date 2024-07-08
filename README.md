# futarin-api

## Requirement
- Ubuntu(WSL2)
  - Docker
- macOS(x86-64,arm64)
  - Docker Desktop
  - (or) OrbStack

## Getting Started
1. Clone this repository
```
git clone git@github.com:futaringoto/futarin-api.git
```

2. Change directory
```
cd futarin-api
```

3. Create `.env` file
```
touch .env
echo "VOICEVOX_URL=[endpoint url]" >> .env
```

4. Build docker image (Only first time)
```
docker compose build
```

5. Build and Start image
```
docker compose up
docker compose up -d # detach
```
6. access to localhost
http://localhost/

## Structure
- api (application - FastAPI)
- nginx (web-server)
```
.
├── README.md
├── _docker
│   ├── api
│   │   └── Dockerfile
│   └── nginx
│       └── conf.d
│           └── app.conf
├── api
│   ├── __init__.py
│   ├── main.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── routers
│   │   ├── __init__.py
│   │   └── raspi.py
│   └── schemas
│       └── __init__.py
└── docker-compose.yml
```
