# これは何

python を用いたスクレイピングを体験してみた。  
ドイツの学校検索システムから学校名とメールアドレスを取得し、csv として出力する。

# 準備

- pip をインストール

  pip はインストール用の get-pip.py を取得してそれを実行することでインストールできる

```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3 get-pip.py
```

- ライブラリ をインストール

```
$ pip3 install requests
$ pip3 install lxml
$ pip3 install tqdm
```

# 使い方

- 実行

```
$ python3 main.py
```

出力結果は `exports` 下に保存される  
途中で止めたい時は `Ctrl + C`

# 注意

google_search_url が入っている場合、「google 検索結果全体から最初にマッチしたメールアドレス」を入れているだけなので、
メールアドレスが正しいかどうか疑った方が良い。特にドメインがおかしい場合など。
