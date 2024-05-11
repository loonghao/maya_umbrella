# maya-umbrella

[![Python Version](https://img.shields.io/pypi/pyversions/maya-umbrella)](https://img.shields.io/pypi/pyversions/maya-umbrella)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![PyPI Version](https://img.shields.io/pypi/v/maya-umbrella?color=green)](https://pypi.org/project/maya-umbrella/)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella)](https://pepy.tech/project/maya-umbrella)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella/month)](https://pepy.tech/project/maya-umbrella)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella/week)](https://pepy.tech/project/maya-umbrella)
[![License](https://img.shields.io/pypi/l/maya-umbrella)](https://pypi.org/project/maya-umbrella/)
[![PyPI Format](https://img.shields.io/pypi/format/maya-umbrella)](https://pypi.org/project/maya-umbrella/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/loonghao/maya-umbrella/graphs/commit-activity)
[![maya-2024](https://img.shields.io/badge/maya-2024-green)](https://img.shields.io/badge/maya-2024-green)
[![maya-2023](https://img.shields.io/badge/maya-2023-green)](https://img.shields.io/badge/maya-2023-green)
[![maya-2022](https://img.shields.io/badge/maya-2022-green)](https://img.shields.io/badge/maya-2022-green)
[![maya-2021](https://img.shields.io/badge/maya-2021-green)](https://img.shields.io/badge/maya-2021-green)
[![maya-2020](https://img.shields.io/badge/maya-2020-green)](https://img.shields.io/badge/maya-2020-green)
[![maya-2019](https://img.shields.io/badge/maya-2019-green)](https://img.shields.io/badge/maya-2019-green)
[![maya-2018](https://img.shields.io/badge/maya-2018-green)](https://img.shields.io/badge/maya-2018-green)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-8-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This tool is designed to provide a robust solution for identifying and resolving any potential viruses within Autodesk
Maya.
It ensures a secure and seamless user experience by proactively scanning for threats and effectively neutralizing them.

It can be provided as an API for seamless integration into your existing pipeline.

# 安装

## pip 安装
maya_umbrella是以标准pipy包去发布的，所以我们可以通过pip install去安装
```shell
your/maya-root/mayapy -m pip install maya-umbrella
```
## 一键安装
在release里面下载对应版本的zip包，解压后双击`install.bat`即可安装

更新版本
```shell
your/maya-root/mayapy -m pip install maya-umbrella --upgrade
```
卸载
```shell
your/maya-root/mayapy -m pip uninstall  maya-umbrella
```

# 开发环境设置

Set up the development environment using a virtual environment,
and it is recommended to use Python 3.8 or higher versions.

通过虚拟环境去设置开发环境, 推荐python-3.8以上的版本

通过pip安装相关开发依赖

```shell
pip install -r requirements-dev.txt
```

# 开发调试


## 在maya中测试

通过`nox -s maya -- <maya version>`, 启动maya.
nox会动态根据你本地安装得maya去注册nox session, 比如你本地安装了`maya-2020`，
那么通过可以启动带有测试环境的maya
```shell
nox -s maya -- 2018
```

**注意：maya 与 版本号之间有 俩个`-`**

启动maya后在脚本编辑器中执行下面得代码，就会动态的从`<repo>/tests/virus/`里面去open ma文件去进行测试.

```python
import manual_test_in_maya

manual_test_in_maya.start()
```

也可以通过pytest去执行对应的测试，也需要本地安装了对应的maya

```shell
nox -s maya -- 2018 --test
```

**注意：在maya-2022 (PY2) 以下的版本可能会出现命令行crash的情况**


## 增加新的疫苗

在`<repo>/maya_umbrella/vaccines/` 新建一个py, 因为有很多病毒没有具体的名字代号，我们统一以`vaccine<id>.py`
继承`from maya_umbrella.vaccine import AbstractVaccine`并且class名字叫`Vaccine`即可, 然后去写具体的收集病毒逻辑

## 代码检查

我们可以利用封装好的`nox`命令去执行进行代码检查

```shell
nox -s lint
```

进行代码整理
```shell
nox -s lint-fix
```

# 生成安装包

执行下面的命令可以在<repo>/.zip下面创建zip，参数 `--version` 当前工具的版本号

**注意：`make-zip` 与 `--version`之间有 俩个`-`**

```shell
nox -s make-zip -- --version 0.5.0
```

# 环境变量

我们可以通过下列环境变量去修改maya_umbrella的一些设置，方便有pipeline的公司可以更好的集成

修改maya umbrella的日志保存目录，默认是windows temp目录

```shell
MAYA_UMBRELLA_LOG_ROOT
```

修改maya umbrella的日志文件名称, 默认是`maya_umbrella`

```shell
MAYA_UMBRELLA_LOG_NAME
```

设置日志级别，默认是info, 可以是debug可以看到更多的日志信息

```shell
MAYA_UMBRELLA_LOG_LEVEL
```
修改杀毒后文件的备份文件夹名称， 默认是`_virus`
比如:
你文件路径是  `c:/your/path/file.ma`
那么备份文件路径是 `c:/your/path/_virus/file.ma`
```shell
MAYA_UMBRELLA_BACKUP_FOLDER_NAME
```
默认的显示语言，包含日志打印输出等，默认是根据你当前maya的界面语言来设置的，当然我们也可以通过下面的环境变量去设置
```shell
MAYA_UMBRELLA_LANG
```

忽略保存到备份文件夹，*请注意，如果你不清楚这个会导致的后果请不要轻易修改*，默认批量杀毒后会把源文件自动备份到当前文件的备份文件夹.
```shell
MAYA_UMBRELLA_IGNORE_BACKUP
```

如果忽略请设置为
```shell
SET MAYA_UMBRELLA_IGNORE_BACKUP=true
```

如果是便携版Maya，可以通过添加 `MAYA_LOCATION` 环境变量指定Maya路径
```shell
SET MAYA_LOCATION=d:/your/path/maya_version/
```
也可以通过命令行指定目录

```shell
nox -s maya -- 2018 --install-root /your/local/maya/root

```

# API
获取当前场景没有被修复的病毒文件

```python
from maya_umbrella import MayaVirusDefender

api = MayaVirusDefender()
print(api.get_unfixed_references())
```

批量修复文件, 通过正则表达式
```python
from maya_umbrella import MayaVirusScanner

api = MayaVirusScanner()
print(api.scan_files_from_pattern("your/path/*.m[ab]"))

```

# 案例
如果你想要快速通过maya standalone去批量清理maya文件，
可以`下载`或者`git clone`当前`main`分支的工程，
根据上面指引设置好开发环境,
通过`nox`命令去启动maya `standalone`环境，maya版本根据你当前本地安装的maya为准，
比如你本地安装了`2018`,
那么就是 `nox -s maya -- 2018 --standalone`
下面的语法是启动一个maya-2020的环境去动态从`c:/test`文件夹下去查杀病毒

```shell
nox -s maya -- 2018 --standalone --pattern c:/test/*.m[ab]
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/loonghao"><img src="https://avatars1.githubusercontent.com/u/13111745?v=4?s=100" width="100px;" alt="Hal"/><br /><sub><b>Hal</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Code">💻</a> <a href="#infra-loonghao" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hotwinter0"><img src="https://avatars.githubusercontent.com/u/106237305?v=4?s=100" width="100px;" alt="hotwinter0"/><br /><sub><b>hotwinter0</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=hotwinter0" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=hotwinter0" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lingyunfx"><img src="https://avatars.githubusercontent.com/u/73666629?v=4?s=100" width="100px;" alt="lingyunfx"/><br /><sub><b>lingyunfx</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=lingyunfx" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yjjjj"><img src="https://avatars.githubusercontent.com/u/12741735?v=4?s=100" width="100px;" alt="yjjjj"/><br /><sub><b>yjjjj</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/uncleschen"><img src="https://avatars.githubusercontent.com/u/37014389?v=4?s=100" width="100px;" alt="Unclechen"/><br /><sub><b>Unclechen</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=uncleschen" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/CGRnDStudio"><img src="https://avatars.githubusercontent.com/u/8320794?v=4?s=100" width="100px;" alt="andyvfx"/><br /><sub><b>andyvfx</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=CGRnDStudio" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cundesi"><img src="https://avatars.githubusercontent.com/u/15829469?v=4?s=100" width="100px;" alt="cundesi"/><br /><sub><b>cundesi</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=cundesi" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Wenfeng-Zhang"><img src="https://avatars.githubusercontent.com/u/54899080?v=4?s=100" width="100px;" alt="Wenfeng Zhang"/><br /><sub><b>Wenfeng Zhang</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=Wenfeng-Zhang" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=Wenfeng-Zhang" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
