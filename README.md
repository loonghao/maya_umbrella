# maya_umbrella

Check and fix maya virus.

[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END --> 





# 发开环境设置
python 版本 3.9

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
继承`from maya_umbrella.vaccine import BaseVaccine`并且class名字叫`Vaccine`即可, 然后去写具体的逻辑



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
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
