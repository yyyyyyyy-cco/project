# 数据集下载与放置指南

## 目录结构

下载的数据集应放置在以下目录中：

```
E:\study\projects\A\project\datasets\dataset\
├── data.yaml                # YOLO 数据集配置文件（自动生成）
├── xml2txt.py               # VOC XML → YOLO TXT 格式转换脚本
├── split_data.py            # 数据集划分脚本
├── CCTSDB/                  # 原始 CCTSDB 数据集（下载后放这里）
│   ├── JPEGImages/          # 原始图片
│   └── Annotations/         # VOC XML 标注文件
├── TT100K/                  # 原始 TT100K 数据集（可选，下载后放这里）
│   ├── images/              # 原始图片
│   └── annotations/         # 标注文件
├── images/                  # 划分后的图片（由 split_data.py 生成）
│   ├── train/
│   ├── val/
│   └── test/
└── labels/                  # 划分后的标签（由 xml2txt.py + split_data.py 生成）
    ├── train/
    ├── val/
    └── test/
```

---

## 数据集下载方式

### 一、CCTSDB（主数据集，必下载）

**数据集简介**：中南大学发布的中国交通标志检测基准数据集，约 15,000+ 张真实道路场景图片，包含禁令、警告、指示三大类标志。

#### 方式 1：GitHub 搜索下载（推荐）

1. 打开 GitHub，搜索关键词：`CCTSDB` 或 `Chinese Traffic Sign Detection Benchmark`
2. 找到包含数据集的仓库，通常以 ZIP 压缩包形式提供
3. 下载后解压到 `E:\study\projects\A\project\datasets\dataset\CCTSDB\`

#### 方式 2：Kaggle 下载

1. 打开 <https://www.kaggle.com>
2. 搜索 `CCTSDB` 或 `Chinese traffic sign`
3. 找到数据集后点击 "Download" 按钮
4. 解压到 `E:\study\projects\A\project\datasets\dataset\CCTSDB\`

#### 方式 3：学术资源网站

- 中南大学官方资源页面
- Papers With Code 网站搜索 "CCTSDB"

#### 预期数据结构

下载解压后，CCTSDB 目录应包含：

```
CCTSDB/
├── JPEGImages/           # 图片文件（.jpg）
│   ├── 000001.jpg
│   ├── 000002.jpg
│   └── ...
└── Annotations/          # Pascal VOC XML 标注文件
    ├── 000001.xml
    ├── 000002.xml
    └── ...
```

---

### 二、TT100K（补充数据集，可选下载）

**数据集简介**：清华大学与腾讯联合发布的交通标志数据集，100,000 张街景图片，200+ 类标志。

#### 下载方式

1. 访问官方页面：<https://cg.cs.tsinghua.edu.cn/traffic-sign/>
2. 点击数据集下载链接（通常需要填写邮箱或同意使用协议）
3. 下载后解压到 `E:\study\projects\A\project\datasets\dataset\TT100K\`

#### 预期数据结构

```
TT100K/
├── train/                # 训练集
│   ├── images/           # 图片
│   └── annotations.json  # 标注
├── test/                 # 测试集
│   ├── images/
│   └── annotations.json
└── meta.json             # 类别元数据
```

---

## 下载后处理步骤

### 第 1 步：确认数据完整性

```bash
# 检查 CCTSDB 图片数量
ls E:/study/projects/A/project/datasets/dataset/CCTSDB/JPEGImages/ | wc -l

# 检查标注数量
ls E:/study/projects/A/project/datasets/dataset/CCTSDB/Annotations/ | wc -l
```

图片数和标注数应一致（约 15,000+）。

### 第 2 步：格式转换（VOC XML → YOLO TXT）

```bash
cd E:/study/projects/A/project/datasets/dataset
python xml2txt.py
```

此脚本会将 `CCTSDB/Annotations/` 中的 XML 文件转换为 YOLO TXT 格式。

### 第 3 步：划分数据集

```bash
python split_data.py
```

此脚本会将数据按 70% 训练 / 10% 验证 / 20% 测试 的比例划分到 `images/` 和 `labels/` 目录。

### 第 4 步：生成 data.yaml

根据实际路径生成 `data.yaml` 配置文件，供 YOLOv8 训练使用。

---

## 常见问题

### Q: 下载速度慢怎么办？

- Kaggle 和 GitHub 支持断点续传
- TT100K 文件较大（约 2-3GB），建议使用下载工具
- 可以先只下载 CCTSDB（约 500MB），验证流程后再补充 TT100K

### Q: 找不到下载链接？

- 在 GitHub 搜索 `CCTSDB YOLO`，很多仓库提供了预处理好的 YOLO 格式数据集
- 在 Kaggle 搜索 `Chinese Traffic Sign`
- 在 CSDN/知乎搜索 "CCTSDB 下载"，社区用户常分享网盘链接

### Q: 数据集标注格式不对怎么办？

- 如果下载的是 COCO JSON 格式，需要编写转换脚本
- 如果下载的已经是 YOLO TXT 格式，可跳过 xml2txt.py 步骤
- 参考 `class_Detection` 项目中的 `xml2txt.py` 和 `yolo2coco.py` 脚本
