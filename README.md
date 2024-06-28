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
git@github.com:futaringoto/futarin-api.git
```

2. Change directory
```
cd futarin-api
```

3. Build docker image (Only first time)
```
docker compose build
```

4. Build and Start image
```
docker compose up
docker compose up -d # detach
```
5. access to localhost
http://localhost/

## Structure
- app (Fast API)
- web (nginx)
```
.
├── README.md
├── app
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── src
│       ├── __init__.py
│       └── main.py
├── docker-compose.yml
└── web
    └── conf.d
        └── app.conf
```
