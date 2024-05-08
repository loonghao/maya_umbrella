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
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This tool is designed to provide a robust solution for identifying and resolving any potential viruses within Autodesk
Maya.
It ensures a secure and seamless user experience by proactively scanning for threats and effectively neutralizing them.

It can be provided as an API for seamless integration into your existing pipeline.

# 安装
maya_umbrella是以标准pipy包去发布的，所以我们可以通过pip install去安装
```shell
your/maya-root/mayapy -m pip install maya-umbrella
```
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

```shell
pip install nox poetry
```

# 开发调试

```shell
nox -s maya-2020
```

## 在maya中测试

通过`nox -s maya-xxx`, 启动maya.
nox会动态根据你本地安装得maya去注册nox session, 比如你本地安装了`maya-2020`，那么通过`nox -s maya-2018`

启动maya后在脚本编辑器中执行下面得代码，就会动态的从`<repo>/tests/virus/`里面去open ma文件去进行测试.

```python
import manual_test_in_maya

manual_test_in_maya.start()
```

## 增加新的疫苗

在`<repo>/maya_umbrella/vaccines/` 新建一个py, 因为有很多病毒没有具体的名字代号，我们统一以`vaccine<id>.py`
继承`from maya_umbrella.vaccine import AbstractVaccine`并且class名字叫`Vaccine`即可, 然后去写具体的收集病毒逻辑

## 代码检查

我们可以利用封装好的`nox`命令去执行进行代码检查

```shell
nox -s ruff_check
```

# 生成安装包

执行下面的命令可以在<repo>/.zip下面创建zip，参数 `--version` 当前工具的版本号

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
那么备份文件路径是 `c:/your/path/_maya_umbrella/file.ma`
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

# API
获取当前场景没有被修复的病毒文件

```python
from maya_umbrella import MayaVirusDefender

api = MayaVirusDefender()
print(api.get_unfixed_references())
```

批量修复文件
```python
from maya_umbrella import MayaVirusScanner

api = MayaVirusScanner()
print(api.scan_files_from_pattern("your/path/*.m[ab]"))

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
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
