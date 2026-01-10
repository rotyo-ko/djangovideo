# 簡易動画掲示板

## 概要

このプロジェクトは、Django の学習目的で作成した Web アプリケーションです。

画像掲示板プロジェクト（`my_imageboard`）をベースにした動画掲示板です。

動画とそのコメントの CRUD 機能があります。

認証には `django-allauth` を導入しています。

- トップページは未ログインでも動画の閲覧が可能です。

- ログインすると動画が投稿可能です。投稿する動画とサムネイル用の画像を用意してください。

- 動画詳細ページではログイン中のユーザーが以下の操作を行えます。
  - コメントを投稿
  - 編集
  - 削除
  
## データベースについて

開発は PostgreSQL でおこないましたが、このリポジトリでは SQLite を使用しています。
  
また、環境変数の管理に `django-environ` を導入しているので `.env` を設定していただければ PostgreSQL でも実行できるようになっています。
  
`.env.example` を参考に `.env` を設定してください。そのままでしたら SQLite で実行できます。
  

## 導入方法

  
```bash  
git clone https://github.com/rotyo-ko/djangovideo
# git がないときは zipファイルをダウンロードしてください。

cd djangovideo

# .env の作成
# .env.example をコピーして .env を作成してください

# 仮想環境の作成
python -m venv venv
```

## 仮想環境の有効化
### Windows (コマンドプロンプト)
```bash
venv\Scripts\activate
```

### Windows PowerShell
```bash
.\venv\Scripts\Activate.ps1
```
### macOS / Linux (bash/zsh)
```bash
source venv/bin/activate
```

## パッケージのインストール
```bash
pip install -r requirements.txt
```
## SECRET_KEY の設定

Django を起動するには SECRET_KEY が必要です。

以下のコマンドを実行して、表示された文字列を `.env` の `SECRET_KEY` に設定してください。


```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 
```

## マイグレーション と　サーバー起動
```bash
python manage.py migrate
python manage.py runserver
```
  
### ブラウザでアクセス
http://127.0.0.1:8000/
  
## テストの実行

```bash
python manage.py test
```
