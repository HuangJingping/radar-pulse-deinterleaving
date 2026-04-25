# 数据目录

本目录用于存放 TSRD 数据集。

## 下载方式

```bash
# 方式1: HuggingFace
pip install datasets
from datasets import load_dataset
ds = load_dataset("TuringBombe/TSRD")

# 方式2: 直接下载 ZIP
# https://huggingface.co/datasets/TuringBombe/TSRD/tree/main
```

## 数据格式

- 格式: HDF5 (.h5)
- 特征: 5维 PDW (ToA, Frequency, PulseWidth, AoA, Amplitude)
- 模式: Stare (全场监测) / Scan (扫频)

## 注意事项

- 完整数据集约 62GB
- archive/: 通用脉冲数据
- scan/: 扫频模式数据
- stare/: 全景模式数据
