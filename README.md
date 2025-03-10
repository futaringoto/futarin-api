# futarin-api
[![CI](https://github.com/futaringoto/futarin-api/actions/workflows/ci.yml/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/ci.yml)
[![Build container and push to ACR](https://github.com/futaringoto/futarin-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/deploy.yml)
[![Dependabot Updates](https://github.com/futaringoto/futarin-api/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/futaringoto/futarin-api/actions/workflows/dependabot/dependabot-updates)

## 目次
- [貢献者ガイド(CONTRIBUTING.md)](#貢献者ガイドcontributingmd)
- [動作環境（確認済み）](#動作環境確認済み)
- [動作確認](#動作確認)
- [APIエンドポイント](#apiエンドポイント)
- [ディレクトリ構成](#ディレクトリ構成)
- [VOICEVOX](#voicevox)
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
echo "OPENAI_ASSISTANT_ID=[openAI assistant id]" >> .env
echo "OPENAI_THREAD_ID=[openAI thread id]" >> .env
echo "AZURE_STORAGE_ACCOUNT=[azure storage-account name]" >> .env
echo "AZURE_SAS_TOKEN=[azure storage-account SAS token]" >> .env
echo "PUBSUB_CONNECTION_STRING=[azure Web PubSub connection string]" >> .env
echo "OPENAI_ASSISTANT_ID_PARAPHRASE=[openAI assistant id 2]" >> .env
```
    - `VOICEVOX_API_KEY` は https://su-shiki.com/api/ から、
    - `OPENAI_API_KEY` は https://platform.openai.com/docs/overview から
    - `OPENAI_API_KEY` は https://platform.openai.com/docs/overview から

3. Dockerイメージのビルド
```
sudo make build
```

4. コンテナ起動
```
sudo make run-dev
# Detachモード
sudo make run-dev-d
```

5. テーブル作成
```
sudo make create-table
```

6. localhost でドキュメントを開いてみましょう
http://localhost/docs

7. コンテナの停止
```
sudo make stop
```

## APIエンドポイント
詳しくは https://futaringoto.github.io/futarin-api/ を参照してください。
### v2
| メソッド | パス | 概要 | 実装状況 |
| :----- | :-- | :-- | :-- |
| GET POST PUT DELETE | `/v2/raspis` | ラズパイ関連 |  |
| POST | `/v2/raspis/{id}/` | 一連の処理全て |  |
| POST | `/v2/raspis/{id}/messages/` | messageの作成 |  |
| POST | `/v2/raspis/{id}/negotiate/` | websockets接続 |  |
| GET POST PUT DELETE | `/v2/users/` | ユーザ関連 | ✔️ |
| GET POST PUT DELETE | `/v2/couples/` | ペア関連 | ✔️ |
| GET POST | `/v2/rag/` | RAG（質問生成）関連 | ✔️ |

### v1
| メソッド | パス | 概要 |
| :----- | :-- | :-- |
| POST | `/v1/raspi/` | 一連の処理全て |
| POST | `/v1/sandbox/gpt/` | ChatGPTによる文章生成 |
| POST | `/v1/sandbox/transcript/` | whisperによる文字起こし |

> [!WARNING]
> 従来の`/raspi/xxx/`系のエンドポイントはdeprecated(非推奨)となりました。

## `make`コマンドについて
本リポジトリは`Makefile`を採用しています。
| Make | 実行する処理 | 元のコマンド |
| :--- | :-------- | :-------- |
| `make build` | コンテナのビルド | `docker compose -f docker-compose.yml -f docker-compose.dev.yml build` |
| `make build-no-cache` | コンテナのビルド(キャッシュなし) | `docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache` |
| `make run-dev` | コンテナの起動 | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` |
| `make run-dev-d` | コンテナの起動（デタッチ） | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` |
| `make stop` | コンテナの停止 | `docker compose down` |
| `make lint` | リントの実行 | `docker compose exec api flake8` |
| `make format` | フォーマットの実行 | `docker compose exec api black .` `docker compose exec api isort .` |
| `make test` | テストの実行 | `docker compose exec api pytest` |
| `make create-table` | テーブルの作成 | `docker compose exec api python migrate_db.py` |

## ディレクトリ構成
- api (application - FastAPI)
- nginx (web-server)
```
.
├── CONTRIBUTING.md
├── ER.md
├── LICENSE
├── Makefile
├── README.md
├── _docker
│   ├── api
│   │   └── Dockerfile
│   ├── db
│   │   ├── docker-entrypoint-initdb.d
│   │   │   └── create_table.sql
│   │   └── my.cnf
│   └── nginx
│       └── conf.d
│           └── app.conf
├── api
│   ├── alembic
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── alembic.ini
│   ├── config.py
│   ├── db-cert.pem
│   ├── db.py
│   ├── main.py
│   ├── migrate_db.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── tests
│   │   ├── __init__.py
│   │   ├── audio1.wav
│   │   ├── conftest.py
│   │   ├── cruds
│   │   │   └── conftest.py
│   │   ├── test_v1_raspi.py
│   │   ├── test_v2_raspi.py
│   │   └── test_v2_user.py
│   ├── uploads
│   ├── v0
│   ├── v1
│   └── v2
│       ├── __init__.py
│       ├── azure
│       ├── cruds
│       │   ├── __init__.py
│       │   ├── couple.py
│       │   ├── raspi.py
│       │   └── user.py
│       ├── models
│       │   ├── __init__.py
│       │   ├── couple.py
│       │   ├── message.py
│       │   ├── raspi.py
│       │   └── user.py
│       ├── routers
│       │   ├── __init__.py
│       │   ├── couple.py
│       │   ├── demo.py
│       │   ├── pubsub.py
│       │   ├── raspi.py
│       │   └── user.py
│       ├── schemas
│       │   ├── __init__.py
│       │   ├── couple.py
│       │   ├── raspi.py
│       │   ├── sandbox.py
│       │   └── user.py
│       ├── services
│       │   ├── __init__.py
│       │   ├── blob_storage.py
│       │   ├── gpt.py
│       │   ├── pubsub.py
│       │   ├── voicevox_api.py
│       │   └── whisper.py
│       └── utils
│           ├── __init__.py
│           ├── file_search.txt
│           ├── index.html
│           ├── logging.py
│           └── query.py
├── docker-compose.dev.yml
├── docker-compose.yml
├── init_mysql.sh
└── ws_client.py
```

## VOICEVOX
有志のVOICEVOX APIを使用しています。
- https://voicevox.su-shiki.com/su-shikiapis/
- https://github.com/ts-klassen/ttsQuestV3Voicevox/

## ライセンス
本リポジトリはMITライセンスです。（[LICENSE](https://github.com/futaringoto/futarin-api/blob/main/LICENSE)参照）ただし、一部`apache-2.0`や`LGPL v3`のライブラリを採用しています。それらに関してはそちらのライセンス内容を遵守してください。
