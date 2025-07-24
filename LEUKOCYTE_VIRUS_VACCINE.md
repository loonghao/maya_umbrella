# Leukocyte Virus Vaccine Documentation

## 概述

本文档描述了针对 Leukocyte（白细胞）病毒的疫苗实现。该病毒是一种复杂的 Maya 恶意软件，使用多层 base64 编码和多种感染机制。

## 病毒特征分析

### 病毒名称
- **主要名称**: `leukocyte` (白细胞)
- **类名**: `phage` (噬菌体)

### 感染机制

1. **ScriptJob 感染**
   - 创建 `cmds.scriptJob(event=["SceneSaved", "leukocyte.antivirus()"], protected=True)`
   - 在场景保存时自动执行恶意代码

2. **文件感染**
   - 修改 `userSetup.py` 和 `userSetup.mel` 文件
   - 在 APPDATA 目录创建 `syssztA` 文件夹
   - 创建 `uition.t` 恶意文件

3. **节点感染**
   - 利用 `uifiguration` 节点存储恶意代码
   - 通过 `uifiguration.notes` 属性传播

4. **反疫苗机制**
   - 主动检测并删除现有疫苗文件
   - 检测 `import vaccine`, `import fuckVirus` 等疫苗特征

### 编码技术
- 使用多层 base64 编码隐藏恶意代码
- 使用 `base64.urlsafe_b64decode()` 解码执行
- 动态构建文件路径避免静态检测

## 疫苗实现

### 文件位置
- **疫苗文件**: `maya_umbrella/vaccines/vaccine4.py`
- **签名文件**: `maya_umbrella/signatures.py` (已更新)

### 检测签名

#### JOB_SCRIPTS_VIRUS_SIGNATURES
```python
leukocyte_sig1 = VirusSignature("leukocyte", r"class\s+phage:")
leukocyte_sig2 = VirusSignature("leukocyte", r"leukocyte\s*=\s*phage\(\)")
leukocyte_sig3 = VirusSignature("leukocyte", r"leukocyte\.occupation\(\)")
leukocyte_sig4 = VirusSignature("leukocyte", r"leukocyte\.antivirus\(\)")
leukocyte_sig5 = VirusSignature("leukocyte", r"cmds\.scriptJob\(event=\[\"SceneSaved\",\s*\"leukocyte\.antivirus\(\)\"\]")
```

#### FILE_VIRUS_SIGNATURES
```python
"base64.urlsafe_b64decode.*exec.*pyCode"
"os.getenv.*APPDATA.*syssztA"
"uifiguration.notes"
```

### 清理功能

#### 1. 恶意文件清理
- `leukocyte.py` / `leukocyte.pyc`
- `phage.py` / `phage.pyc`
- `%APPDATA%/syssztA/` 目录
- `%APPDATA%/syssztA/uition.t` 文件

#### 2. 感染文件清理
- 检测并清理感染的 `userSetup.py`
- 检测并清理感染的 `userSetup.mel`
- 支持本地和用户脚本目录

#### 3. 恶意节点清理
- 检测并删除感染的 script 节点
- 特别检测 `uifiguration` 节点
- 清理节点的 `before`, `after`, `notes` 属性

#### 4. ScriptJob 清理
- 自动检测并终止恶意 scriptJob
- 匹配关键词: `leukocyte.antivirus`, `leukocyte.occupation`, `phage`

## 测试验证

### 单元测试
- **文件**: `tests/test_leukocyte_vaccine.py`
- **覆盖**: 8 个测试用例，覆盖所有主要功能
- **结果**: 全部通过 ✓

### 病毒样本测试
- **样本文件**: `tests/virus/leukocyte_virus_sample.py`
- **检测结果**: 15 个病毒特征被成功检测
- **验证脚本**: `test_leukocyte_detection.py`

### 检测效果
```
JOB_SCRIPTS_VIRUS_SIGNATURES detected 7 patterns:
  - userSetup: 5 matches
  - fuckVirus: 2 matches
  - class\s+phage:: 1 matches
  - leukocyte\s*=\s*phage\(\): 1 matches
  - leukocyte\.occupation\(\): 3 matches
  - leukocyte\.antivirus\(\): 1 matches
  - cmds\.scriptJob\(event=\[\"SceneSaved\",\s*\"leukocyte\.antivirus\(\)\"\]: 1 matches

FILE_VIRUS_SIGNATURES detected 8 patterns:
  - import vaccine: 1 matches
  - cmds.evalDeferred.*leukocyte.+: 1 matches
  - class\s+phage:: 1 matches
  - leukocyte\s*=\s*phage\(\): 1 matches
  - leukocyte\.occupation\(\): 3 matches
  - leukocyte\.antivirus\(\): 1 matches
  - base64.urlsafe_b64decode.*exec.*pyCode: 1 matches
  - uifiguration.notes: 1 matches
```

## 使用方法

疫苗会自动加载到 maya_umbrella 系统中，无需手动配置。当运行病毒扫描时：

1. 疫苗会自动检测所有 leukocyte 病毒特征
2. 识别感染的文件、节点和 scriptJob
3. 提供清理建议和自动清理功能
4. 记录所有检测和清理操作

## 技术特点

1. **全面检测**: 覆盖病毒的所有感染机制
2. **智能清理**: 区分感染文件和正常文件
3. **安全操作**: 避免误删重要文件
4. **详细日志**: 记录所有操作便于审计
5. **测试完备**: 包含完整的测试套件

## 更新历史

- **2025-01-24**: 初始版本，支持 leukocyte 病毒检测和清理
- 基于真实病毒样本分析和逆向工程
- 通过完整测试验证有效性

## 注意事项

1. 该疫苗专门针对 leukocyte 病毒变种
2. 建议定期更新病毒签名以应对新变种
3. 清理操作不可逆，建议先备份重要文件
4. 如发现新的病毒特征，请及时更新签名库
