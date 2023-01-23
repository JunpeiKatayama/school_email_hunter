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

- celenium をインストール

```
$ pip3 install selenium
```

# 使い方

- 実行

```
$ python3 get.py
```

下記のような出力が出るが気にしなくて OK

```
/usr/xxx/xxx/scrapingByPython/get.py:10: DeprecationWarning: executable_path has been deprecated, please pass in a Service object
  driver = webdriver.Chrome('./chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
```

出力結果は `list.csv` に保存される  
途中で止めたい時は `Ctrl + C`
