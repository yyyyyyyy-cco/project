# 数据集下载与放置指南

## 目录结构

下载的数据集应放置在以下目录中：

```text
datasets/dataset/
├── data.yaml                # YOLO 数据集配置文件
├── tt100k_to_yolo.py        # TT100K JSON → YOLO TXT 格式转换脚本
├── split_data.py            # 数据集划分脚本
├── TT100K/                  # 原始 TT100K 数据集（下载后放这里）
│   ├── train/
│   │   ├── images/          # 训练集图片
│   │   └── annotations.json # 训练集标注
│   └── test/
│       ├── images/          # 测试集图片
│       └── annotations.json # 测试集标注
├── labels_temp/             # 转换后的临时标签（由 tt100k_to_yolo.py 生成）
├── images/                  # 划分后的图片（由 split_data.py 生成）
│   ├── train/
│   ├── val/
│   └── test/
└── labels/                  # 划分后的标签
    ├── train/
    ├── val/
    └── test/
```

---

## 数据集下载方式

### TT100K（清华-腾讯交通标志数据集）

**数据集简介**：清华大学与腾讯联合发布的交通标志数据集，100,000 张街景图片，221 类标志（过滤后使用 45 类）。

#### 下载方式

1. 访问官方页面：[https://cg.cs.tsinghua.edu.cn/traffic-sign/](https://cg.cs.tsinghua.edu.cn/traffic-sign/)
2. 点击数据集下载链接（通常需要填写邮箱或同意使用协议）
3. 下载后解压到 `datasets/dataset/TT100K/`

#### 预期数据结构

```text
TT100K/
├── train/                # 训练集
│   ├── images/           # 图片
│   └── annotations.json  # 标注
├── test/                 # 测试集
│   ├── images/
│   └── annotations.json
└── meta.json             # 类别元数据（可选）
```

---

## 下载后处理步骤

### 第 1 步：确认数据完整性

```bash
# 检查训练集图片数量
ls TT100K/train/images/ | wc -l

# 检查测试集图片数量
ls TT100K/test/images/ | wc -l
```

训练集约 6,105 张，测试集约 3,071 张。

### 第 2 步：格式转换（JSON → YOLO TXT）

```bash
python tt100k_to_yolo.py
```

此脚本会将 TT100K 的 JSON 标注转换为 YOLO TXT 格式，保存到 `labels_temp/` 目录。只保留过滤后的 45 类（样本数 ≥ 100）。

### 第 3 步：划分数据集

```bash
python split_data.py
```

此脚本会将数据按 70% 训练 / 10% 验证 / 20% 测试 的比例划分到 `images/` 和 `labels/` 目录。

### 第 4 步：验证 data.yaml

确认 `data.yaml` 中的路径与实际目录一致。

---

## 常见问题

### Q: 下载速度慢怎么办？

- TT100K 文件较大（约 2-3GB），建议使用下载工具
- 可尝试使用 IDM 或 aria2 等多线程下载工具

### Q: 数据集标注格式不对怎么办？

- TT100K 原始标注为 JSON 格式，由 `tt100k_to_yolo.py` 自动转换
- 如果下载的已经是 YOLO TXT 格式（如 Roboflow 导出），可跳过转换步骤，直接运行 `split_data.py`
