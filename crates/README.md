# Maya Umbrella Rust Lib

高性能 maya_umbrella 运行库

## 构建

- Rust 1.80
- Python 2.7

### 环境变量

> 环境变量按需配置
>

Python(Maya Python) 目录存在 ```includes``` ```libs```

VSCode Settings

```json
{
    // 开发环境
    "rust-analyzer.cargo.extraEnv": {
        "PYTHON_SYS_EXECUTABLE": "[MAYA_HOME]\\bin\\mayapy.exe"
    },
    "rust-analyzer.server.extraEnv": {
        "PYTHON_SYS_EXECUTABLE": "[MAYA_HOME]\\bin\\mayapy.exe"
    },
    // 构建环境
    "terminal.integrated.env.windows": {
        "PYTHON_SYS_EXECUTABLE": "[MAYA_HOME]\\bin\\mayapy.exe",
        "PATH": "[MAYA_HOME]\\bin;${env:PATH}",
        "PYTHONPATH": "[CURRENT]\\target\\release",
    }
}
```

构建命令

```shell
cargo build --release
```

修改文件

```[CURRENT]/target/release``` 会生成 ```maya_umbrella_rs.dll``` 修改为 ```maya_umbrella_rs.pyd```

## 性能测试

测试脚本：```[CURRENT]/tests/rust-lib-tests/test_text_virus_detector.py```

> 目前仅实现检查文本测试

```console
Files Count: 2000
2.43s
```
