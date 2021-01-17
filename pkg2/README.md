# pkg2

## 

* バージョン番号の元は、``__init__.py``の``__version__``
* バージョン番号の参照は ``python setup.py --version``
* ``requirements.txt``は、もはやレガシー

* TBD: ``pipenv``に移行すべき？(``pipenv``は大げさ過ぎる?)

  [Pipenv をやめて venv を使いだした話](https://blog.uedder.com/2020_python_develop_envirionment.html)

## 

```
  +- README.md
  +- setup.py
  +- setup.cfg
  +- entry_points.cfg
  +- install.sh
  +- pkg2/
      +- __init__.py
      +- mod1.py
```

## Reference

* [Python: 自作ライブラリのパッケージングについて](https://blog.amedama.jp/entry/packaging-python)
* [setuptools —Pythonパッケージ作成](https://heavywatal.github.io/python/setuptools.html)
