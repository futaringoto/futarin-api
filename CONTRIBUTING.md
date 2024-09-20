# 貢献者ガイド
futarin-api を開発するにあたっての注意事項を記述していく。

## 目次
futarin-api の開発方針について
- [ブランチ戦略](#ブランチ戦略)
- [プルリクエスト](#プルリクエスト)
- [静的解析](#静的解析)
- [テスト](#テスト)
- [GitHub Actions](#github-actions)
- [Issue](#issue)
- [ライセンス](#ライセンス)

## ブランチ戦略

本リポジトリでは、GitHub Flow を採用しています。
プルリクエストは基本的に`main`ブランチへマージされます。
**`main`ブランチは常にリリース可能な状態が保証されます。**
参考：https://docs.github.com/ja/get-started/using-github/github-flow

### ブランチ命名規則
開発時は必ずmainからブランチをきってください。mainに直接pushすることがないように！
ブランチ名の例："feat/#1_hoge"
- feat: ブランチの特徴
  - 新機能：feat
  - 修正：fix
- /#1_hoge
  - issue番号
  - memo
```
git checkout main
git pull
git checkout -b feat/#1_hoge
```

## プルリクエスト
全てのコード変更は[プルリクエスト](https://github.com/futaringoto/futarin-api/pulls)を介して行います。
### プルリクエストを送る
以下の手順で作成します。
- [環境構築](#環境構築)
- リポジトリをクローンする
- ブランチを切る [ブランチ戦略](#ブランチ戦略)参照
- コードを編集する
- [静的解析を実行する](#静的解析)
- [コードのテストを行う](#コードをテストする)
- リモートへプッシュして、`main`ブランチへのプルリクエストを作成する

## 環境構築
開発環境はすべて`docker compose`で完結するよう実装されています。
```
git clone git@github.com:futaringoto/futarin-api.git
cd futarin-api
touch .env
echo "VOICEVOX_API_KEY=[voicevox api key]" >> .env
echo "OPENAI_API_KEY=[openAI api key]" >> .env
```
環境変数を設定してください。詳しくは[README](https://github.com/futaringoto/futarin-api/blob/main/README.md)へ
```
sudo make build
```
> [!IMPORTANT]
> Dockerfileを更新した際は、キャッシュが使われないよう、`sudo docker compose build --no-cache`でビルドしましょう

## コード実行
```
sudo make run-dev
```
> [!TIP]
> ホットリロードを採用しています。pythonファイルの変更が保存されると再度自動でビルドが走ります


## コードの編集
### パッケージ
パッケージ管理に`poetry`を採用しています。
#### パッケージの追加
```
docker compose run --entrypoint "poetry add `パッケージ名`" api
docker compose run --entrypoint "poetry add --group dev `パッケージ名`" api # 開発依存の追加
```
#### パッケージの更新
```
docker compose run --entrypoint "poetry update" api
```

## 静的解析
自動リントと自動整形を採用しています。
### リント
安全性の向上のため、リンターの`flake8`を導入しています。
```
sudo make lint
```
### 整形
可読性の向上のため、フォーマッタの`black`と`isort`を導入しています。
```
sudo make format
```

## テスト
自動テストを採用しています。テストランナーは`pytest`です。
### コードをテストする
```
sudo make test
```

## GitHub Actions
### Workflows
- ci.yml
  - pull request時に起動
  - 静的解析(flake8)とテスト(pytest)を行う
- deploy.yml
  - workflow_dispatch(手動トリガー)で実行
  - イメージの作成とAzure Container Registryへのプッシュ、App Serviceへのデプロイを行う

### Variable
| name               | description         |
| :----------------- | :------------------ |
| LOGIN_SERVER | Azure Container Registry(ACR) サーバURL |


### Secrets
| name | description |
| :--- | :---------- |
| REGISTRY_USERNAME | ACR　ユーザ名 |
| REGISTRY_PASSWORD | ACR パスワード |
| AZURE_WEBAPP_PUBLISH_PROFILE | Azure 認証情報 |
| OPENAI_API_KEY | OpenAI Platform APIキー(テスト用) |
| VOICEVOX_API_KEY | VOICEVOX API APIキー(テスト用) |

## Issue
不具合の報告、機能要望は、[Issue](https://github.com/futaringoto/futarin-api/issues)に報告してください。

## ライセンス
本リポジトリはMITライセンスです。（[LICENSE](https://github.com/futaringoto/futarin-api/blob/main/LICENSE)参照）ただし、一部`apache-2.0`や`LGPL v3`のライブラリを採用しています。それらに関してはそちらのライセンス内容を遵守してください。
