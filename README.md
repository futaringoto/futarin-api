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
echo "VOICEVOX_API_KEY=[voicevox api key]" >> .env
echo "OPENAI_API_KEY=[openAI api key]" >> .env

# Only production mode(開発環境用)
echo "STORAGE_ACCOUNT_NAME=[azure storage-account-name]" >> .env
echo "SAS_TOKEN=[azure storage-account SAS token]" >> .env
```
Create `VOICEVOX_API_KEY` from https://su-shiki.com/api/

4. Build docker image (Only first time)
```
sudo docker compose build
```

5. Build and Start image
```
# Production(本番環境)
sudo docker compose up
# Development(開発環境)
sudo docker compose -f docker-compose.yml -f docker-compose.dev.yml up
# Detachモード
sudo docker compose up -d
```
6. access to localhost to check docs
http://localhost/docs

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
│   ├── schemas
│   │   └── __init__.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── gpt.py
│   │   ├── tts.py
│   │   ├── voicevox.py
│   │   ├── voicevox_api.py
│   │   └── whisper.py
│   ├── uploads
│   └── utils
│       ├── __init__.py
│       ├── config.py
│       └── log.py
├── docker-compose.dev.yml
└── docker-compose.yml
```

## VOICEVOX API
有志のVOICEVOX APIを使用しています。
- https://voicevox.su-shiki.com/su-shikiapis/
- https://github.com/ts-klassen/ttsQuestV3Voicevox/
