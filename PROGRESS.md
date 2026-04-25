# 雷达脉冲信号分选 — 项目进度文件

> 本文件是项目的核心进度文档。每次会话开始时应阅读此文件，了解项目状态和下一步行动。

---

## 📌 项目概述

**项目名称**: Turing Synthetic Radar Dataset (TSRD) 雷达脉冲信号分选研究

**数据位置**: `/opt/data/workspace/雷达信号分选/`

**数据集规模**: 62GB zip，解压后约 18000+ 文件，包含 ~40亿个脉冲

**核心任务**: 给定混合的 5 维 PDW 脉冲序列，聚类出各个独立辐射源的脉冲（发射器数量未知）

---

## 📊 数据集结构

```
turing-radar-data.zip
├── archive/
│   ├── train/        (2501 files)
│   ├── validation/   (251 files)
│   └── test/         (251 files)
├── scan/
│   ├── train_scan/   (2504 files)
│   ├── val_scan/     (254 files)
│   └── test_scan/    (254 files)
├── stare/
│   ├── train_stare/  (2504 files)
│   ├── val_stare/    (254 files)
│   └── test_stare/   (254 files)
└── README.md
```

**数据格式**: HDF5 (.h5)

**每条 PDW 特征 (5维)**:
- ToA (Time of Arrival) — 微秒
- Centre Frequency — MHz
- Pulse Width — 微秒
- AoA (Angle of Arrival) — 度
- Amplitude — dB

**两种接收模式**:
- **Stare Mode**: 全频谱同时监测 (0-18 GHz)，10秒，~38亿脉冲，训练集每条~129万脉冲
- **Scan Mode**: 扫频模式，~2.82亿脉冲，训练集每条~9.4万脉冲

---

## ✅ 已完成任务

### 阶段一：数据探索
- [x] 数据集解压（后台运行中，见下方进度）
- [x] README.md 阅读与分析
- [x] 数据集结构确认
- [x] 数据集规模统计

### 阶段二：研究计划制定
- [x] 制定 8 阶段完整研究计划
- [x] 确定评估指标（V-measure、ARI、AMI、MCC、F1）

---

## 🔄 当前进行中

### 解压进度
- **状态**: 后台运行中
- **Session ID**: `proc_85357d2033e0`
- **命令**: Python zipfile 解压
- **总文件数**: 18,071
- **预计完成时间**: 取决于磁盘I/O，约需数小时

**检查进度命令**:
```bash
process(action='log', session_id='proc_85357d2033e0')
```

---

## 📋 待完成任务

### 阶段一：数据探索（已完成 ✅）
- [x] 加载 HDF5 数据，了解内部结构
- [x] 统计脉冲数量、发射器数量分布
- [x] 特征（5维）统计分析
- [x] 不平衡度分析
- [x] Stare vs Scan 模式差异分析
- [ ] t-SNE/UMAP 可视化探索（可选，后续可视化阶段做）

**数据探索关键发现：**

| 数据集 | 脉冲数 | 发射器数 | 不平衡度 | 难度 |
|--------|--------|---------|---------|------|
| archive | 20k-47k | 7-78 | 3k-5k x | ⭐ 较易 |
| scan | 59k-170k | 15-72 | 10k-23k x | ⭐⭐ 中等 |
| stare | 550k-2M | 10-71 | 12k-129k x | ⭐⭐⭐ 最难 |

**数据格式：**
- `data`: (N, 5) float32, 特征=[ToA, Freq, PW, AoA, Amp]
- `labels`: (N, 1) int8, 发射器标签 (0 到 N_emitters-1)
- `metadata`: 接收机/发射器配置（频率模式、PRI模式等）

**发射器行为模式：**
- 频率: FixedSingle, FixedMultiSimultaneous, HoppingSawtooth, HoppingLinear, RandomRange...
- PRI: Fixed, Staggered, Sliding, Jittered, SwitchDwell
- 扫描: Circular, Omni

### 阶段二：数据预处理
- [ ] 特征标准化方案对比
- [ ] ToA → PRI 转换研究
- [ ] PCA/t-SNE 降维分析

### 阶段三：基线模型
- [ ] K-Means 基线
- [ ] DBSCAN/HDBSCAN
- [ ] GMM
- [ ] 层次聚类
- [ ] Spectral Clustering
- [ ] 批量实验对比

### 阶段四：深度聚类
- [ ] DeepCluster
- [ ] DEC (Deep Embedded Clustering)
- [ ] DCN
- [ ] 对比学习聚类 (SCCL)

### 阶段五：时序感知方法
- [ ] GRU/LSTM AutoEncoder
- [ ] Transformer-based 方法
- [ ] PRI 模式挖掘

### 阶段六：开放域聚类
- [ ] 无需预设 k 的方法调研
- [ ] 发射器数量估计

### 阶段七：评价与分析
- [ ] 指标计算框架
- [ ] 误差分析
- [ ] 可视化

### 阶段八：论文写作
- [ ] 初稿撰写

---

## 🎯 下一步行动

**立即执行（当前会话）**:

1. ~~数据探索~~ ✅ 已完成
2. **开始阶段二：数据预处理** — 标准化、ToA→PRI转换

**具体任务**:

```python
# 加载数据
from src.data_loader import TSRDLoader
loader = TSRDLoader()
data, labels, meta = loader.load_sample('archive/train/train_0.h5')

# 下一步：标准化实验
from sklearn.preprocessing import StandardScaler, MinMaxScaler
# ...
```

---

## 📝 关键发现

### 数据集特点
1. **超大规模**: ~40亿脉冲，62GB 压缩
2. **两种模式**: Stare（全场监测）vs Scan（扫频）— 难度差异大
3. **极端不平衡**: README 提到最大不平衡达 99.7%
4. **未知聚类数**: 测试时发射器数量未知
5. **时序依赖**: ToA 可转为 PRI（脉冲重复间隔）模式

### 核心挑战
1. 发射器数量未知
2. 特征空间重叠严重
3. 极端不平衡
4. 需要利用时序模式

---

## 🛠️ 工具与环境

**Python 环境**: 默认 Python 3 环境

**可用库**:
- `h5py` / `hdf5` — HDF5 数据读取
- `numpy`, `pandas` — 数据处理
- `scikit-learn` — 传统聚类、指标计算
- `scipy` — 层次聚类、统计
- `torch`, `tensorflow` — 深度学习（如需）
- `umap-learn` — UMAP 降维
- `matplotlib`, `seaborn` — 可视化

**数据路径**: `/opt/data/workspace/雷达信号分选/`

---

## 📚 参考资料

- 原论文: Gunn et al., "The Turing Synthetic Radar Dataset: A dataset for pulse deinterleaving"
- GitHub: Turing Deinterleaving Challenge (见 README)
- 评估指标: V-measure, ARI, AMI, MCC, F1

---

*最后更新: 2026-04-25*
*更新人: Hermes Agent*
