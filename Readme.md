# OverView
this is an app to manage for "something something slip"

いわゆる業務系システムの文脈で「伝票」を管理するサービスです。
用途に応じてカスタマイズすることで様々な伝票を扱えます。

今回は見積伝票を管理するアプリとして実装しました。
djangoで作成しています。

# Usage
required python 3.x

* clone this repo
* create venv (recomended)
* pip install -r requirements.txt
* need some database, you config it in mysite/setting.py
* make migrations, migrate, create superuser
* pyhotn manage.py runserver

# todo
modelのクラス設計を見直して、もっと汎用的に、カスタマイズしやすい様に改善する。

