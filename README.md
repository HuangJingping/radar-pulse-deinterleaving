# Radar Pulse Deinterleaving Research

Turing Synthetic Radar Dataset (TSRD) 雷达脉冲信号分选研究

## 项目结构

```
.
├── PROGRESS.md          # 项目进度文件
├── README.md            # 项目说明
├── requirements.txt     # Python 依赖
├── src/                 # 源代码
│   ├── __init__.py
│   ├── data_loader.py   # 数据加载
│   ├── preprocessing.py # 数据预处理
│   ├── baseline.py      # 基线模型
│   ├── models/          # 深度学习模型
│   └── evaluation.py   # 评估指标
├── data/                # 数据目录（需手动下载）
│   └── README.md        # 数据下载说明
└── notebooks/           # Jupyter notebooks
```

## 数据下载

数据集位于 NAS: `/opt/data/workspace/雷达信号分选/`

如需在其他机器上运行:
1. 下载 TSRD 数据集: https://huggingface.co/datasets/TuringBombe/TSRD
2. 解压到 `data/` 目录

## 开始使用

```bash
pip install -r requirements.txt
```

## 研究计划

见 `PROGRESS.md`
