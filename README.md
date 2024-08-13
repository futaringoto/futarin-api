# futarin-api
[![CI](https://github.com/futaringoto/futarin-api/actions/workflows/ci.yml/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/ci.yml)
[![Build container and push to ACR](https://github.com/futaringoto/futarin-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/deploy.yml)
[![Dependabot Updates](https://github.com/futaringoto/futarin-api/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/dependabot/dependabot-updates)

## 目次
- [貢献者ガイド(CONTRIBUTING.md)](#貢献者ガイド(CONTRIBUTING.md))
- [動作環境](#動作環境)
- [動作確認](#動作確認)
- [APIエンドポイント(v1)](#APIエンドポイント(v1))
- [ディレクトリ構成](#ディレクトリ構成)
- [VOICEVOX](#VOICEVOX)
- [ライセンス](#ライセンス)

## 貢献者ガイド(CONTRIBUTING.md)
本リポジトリにコミットする場合、[CONTRIBUTING.md](https://github.com/futaringoto/futarin-api/blob/main/CONTRIBUTING.md)を**必ず確認ください**

## 動作環境（確認済み）
- Ubuntu(WSL2)
  - Docker
- macOS(x86-64,arm64)
  - Docker Desktop もしくは OrbStack

## 動作確認
1. リポジトリのクローンと移動
```
git clone git@github.com:futaringoto/futarin-api.git
cd futarin-api
```

2. `.env`の作成
```
touch .env
echo "VOICEVOX_API_KEY=[voicevox api key]" >> .env
echo "OPENAI_API_KEY=[openAI api key]" >> .env

# Only production mode(開発環境用)
echo "STORAGE_ACCOUNT_NAME=[azure storage-account-name]" >> .env
echo "SAS_TOKEN=[azure storage-account SAS token]" >> .env
```
`VOICEVOX_API_KEY` は https://su-shiki.com/api/ から、  
`OPENAI_API_KEY` は https://platform.openai.com/docs/overview から取得します

3. Dockerイメージのビルド
```
sudo docker compose build
```

4. コンテナ起動
```
# Production(本番環境)
sudo docker compose up
# Development(開発環境)
sudo docker compose -f docker-compose.yml -f docker-compose.dev.yml up
# Detachモード
sudo docker compose up -d
```
5. localhost でドキュメントを開いてみましょう
http://localhost/docs

6. コンテナの停止
```
docker compose down
```

## APIエンドポイント(v1)
詳しくは http://localhost/docs を参照してください。
| メソッド | パス | 概要 |
| :----- | :-- | :-- |
| POST | `/v1/raspi` | 一連の処理全て |
| POST | `/v1/sandbox/gpt` | ChatGPTによる文章生成 |
| POST | `/v1/sandbox/transcript` | whisperによる文字起こし |

> [!WARNING]
> 従来の`/raspi/xxx`系のエンドポイントはdeprecated(非推奨)となりました。

## ディレクトリ構成
- api (application - FastAPI)
- nginx (web-server)
```
.
├── main.py
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── __init__.py
│   ├── audio1.wav
│   └── test_v1_raspi.py
├── v0
│   ├── __init__.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── raspi.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── gpt.py
│   │   ├── tts.py
│   │   ├── voicevox.py
│   │   ├── voicevox_api.py
│   │   └── whisper.py
│   └── utils
│       ├── __init__.py
│       ├── config.py
│       └── log.py
└── v1
    ├── __init__.py
    ├── routers
    │   ├── __init__.py
    │   ├── raspi.py
    │   └── sandbox.py
    ├── schemas
    │   ├── __init__.py
    │   └── sandbox.py
    ├── services
    │   ├── __init__.py
    │   ├── gpt.py
    │   ├── voicevox_api.py
    │   └── whisper.py
    └── utils
        ├── __init__.py
        └── config.py
```

## VOICEVOX
有志のVOICEVOX APIを使用しています。
- https://voicevox.su-shiki.com/su-shikiapis/
- https://github.com/ts-klassen/ttsQuestV3Voicevox/

## ライセンス
本リポジトリはMITライセンスです。（[LICENSE](https://github.com/futaringoto/futarin-api/blob/main/LICENSE)参照）ただし、一部`apache-2.0`や`LGPL v3`のライブラリを採用しています。それらに関してはそちらのライセンス内容を遵守してください。
