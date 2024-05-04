# maya_umbrella

Check and fix maya virus.

[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-19-orange.svg?style=flat-square)](#contributors-)
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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/loonghao"><img src="https://avatars1.githubusercontent.com/u/13111745?v=4?s=100" width="100px;" alt="Hal"/><br /><sub><b>Hal</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Code">💻</a> <a href="#infra-loonghao" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/voodraizer"><img src="https://avatars0.githubusercontent.com/u/1332729?v=4?s=100" width="100px;" alt="voodraizer"/><br /><sub><b>voodraizer</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Avoodraizer" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/brunosly"><img src="https://avatars2.githubusercontent.com/u/4326547?v=4?s=100" width="100px;" alt="brunosly"/><br /><sub><b>brunosly</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Abrunosly" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tubi-carrillo"><img src="https://avatars3.githubusercontent.com/u/33004093?v=4?s=100" width="100px;" alt="tubi"/><br /><sub><b>tubi</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Atubi-carrillo" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wjxiehaixin"><img src="https://avatars0.githubusercontent.com/u/48039822?v=4?s=100" width="100px;" alt="wjxiehaixin"/><br /><sub><b>wjxiehaixin</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Awjxiehaixin" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://it.econline.net"><img src="https://avatars0.githubusercontent.com/u/993544?v=4?s=100" width="100px;" alt="罗马钟"/><br /><sub><b>罗马钟</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Aenzozhong" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ClementHector"><img src="https://avatars.githubusercontent.com/u/7068597?v=4?s=100" width="100px;" alt="clement"/><br /><sub><b>clement</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3AClementHector" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/krevlinmen"><img src="https://avatars.githubusercontent.com/u/56278440?v=4?s=100" width="100px;" alt="krevlinmen"/><br /><sub><b>krevlinmen</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Akrevlinmen" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SThomasN"><img src="https://avatars.githubusercontent.com/u/63218023?v=4?s=100" width="100px;" alt="Thomas"/><br /><sub><b>Thomas</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3ASThomasN" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/CaptainCsaba"><img src="https://avatars.githubusercontent.com/u/59013751?v=4?s=100" width="100px;" alt="CaptainCsaba"/><br /><sub><b>CaptainCsaba</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3ACaptainCsaba" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ilharper.vbox.moe"><img src="https://avatars.githubusercontent.com/u/20179549?v=4?s=100" width="100px;" alt="Il Harper"/><br /><sub><b>Il Harper</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=Afanyiyu" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/blunderedbishop"><img src="https://avatars.githubusercontent.com/u/56189376?v=4?s=100" width="100px;" alt="blunderedbishop"/><br /><sub><b>blunderedbishop</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Ablunderedbishop" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MrTeferi"><img src="https://avatars.githubusercontent.com/u/92750180?v=4?s=100" width="100px;" alt="MrTeferi"/><br /><sub><b>MrTeferi</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=MrTeferi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/damienchambe"><img src="https://avatars.githubusercontent.com/u/42462209?v=4?s=100" width="100px;" alt="Damien Chambe"/><br /><sub><b>Damien Chambe</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=damienchambe" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/be42day"><img src="https://avatars.githubusercontent.com/u/20614168?v=4?s=100" width="100px;" alt="Ehsan Akbari Tabar"/><br /><sub><b>Ehsan Akbari Tabar</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Abe42day" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.linkedin.com/in/michael-ikemann"><img src="https://avatars.githubusercontent.com/u/33489959?v=4?s=100" width="100px;" alt="Michael Ikemann"/><br /><sub><b>Michael Ikemann</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3AAlyxion" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dsmtE"><img src="https://avatars.githubusercontent.com/u/37016704?v=4?s=100" width="100px;" alt="Enguerrand DE SMET"/><br /><sub><b>Enguerrand DE SMET</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=dsmtE" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.thbattle.net"><img src="https://avatars.githubusercontent.com/u/857880?v=4?s=100" width="100px;" alt="Proton"/><br /><sub><b>Proton</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=feisuzhu" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yjjjj"><img src="https://avatars.githubusercontent.com/u/12741735?v=4?s=100" width="100px;" alt="yjjjj"/><br /><sub><b>yjjjj</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
