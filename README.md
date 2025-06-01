# 豆包AI水印工具 - Python版本

![Python Version](https://img.shields.io/badge/python-3.7+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**为照片添加豆包AI生成的水印，创建合理的推诿性！**

这是基于开源项目 [kazutoiris/ai-watermark](https://github.com/kazutoiris/ai-watermark) 的精简Python实现版本，使用原项目的豆包AI水印图案。

## 功能特点

- **图形界面版本** - 简单易用的GUI界面
- **命令行版本** - 适合批量处理和自动化
- **豆包AI水印** - 使用原项目的豆包AI水印图案
- **智能位置** - 自动在图片右下角添加水印
- **透明度控制** - 可调节水印的透明度
- **尺寸控制** - 支持自动或手动调节水印大小
- **批量处理** - 支持一次处理多张图片
- **跨平台支持** - Windows、macOS、Linux

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- pip 包管理器

### 安装依赖

```bash
# 使用conda环境（推荐）
conda activate LATESNA
pip install -r requirements.txt

# 或者直接安装
pip install Pillow>=10.0.0
```

### 使用方法

#### 1. 图形界面版本（推荐新手）

```bash
python ai_watermark.py
```

**操作步骤：**
1. 点击"选择图片文件"按钮选择要处理的图片
2. 在"水印设置"中调整透明度和大小
3. 点击"开始处理"按钮
4. 等待处理完成，文件会保存在原图同目录下

#### 2. 命令行版本（适合批处理）

**处理单张图片：**
```bash
python ai_watermark_cli.py -f your_image.jpg
```

**批量处理目录：**
```bash
python ai_watermark_cli.py -d /path/to/images/
```

**调整透明度和大小：**
```bash
python ai_watermark_cli.py -f image.jpg -p 80 -s large
python ai_watermark_cli.py -d ./photos/ -p 60 -s small
```

**指定输出路径：**
```bash
python ai_watermark_cli.py -f input.jpg -o output.jpg
python ai_watermark_cli.py -d input_dir/ -o output_dir/
```

## 详细参数说明

### 命令行参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--file` | `-f` | 单个图片文件路径 | `-f photo.jpg` |
| `--dir` | `-d` | 图片目录路径（批量） | `-d ./photos/` |
| `--output` | `-o` | 输出路径 | `-o result.jpg` |
| `--opacity` | `-p` | 透明度 (30-100) | `-p 80` |
| `--size` | `-s` | 水印大小 | `-s large` |

### 水印大小选项

| 大小选项 | 说明 | 适用场景 |
|----------|------|----------|
| `auto` | 自动（默认）| 基于原项目算法，适合大多数图片 |
| `small` | 小尺寸 | 适合高分辨率图片或需要低调水印 |
| `medium` | 中等尺寸 | 平衡可见性和美观性 |
| `large` | 大尺寸 | 适合低分辨率图片或需要明显水印 |

## 设计目标

- **创建合理推诿** - 为暴露的私人内容提供合理的推诿性
- **保持归属模糊** - 在社区中保持归属的模糊性  
- **建立隐私防护** - 为意外的隐私分发建立防护

## 使用示例

```bash
# 处理单张照片，使用默认设置
python ai_watermark_cli.py -f selfie.jpg

# 批量处理相册文件夹，使用高透明度小尺寸水印
python ai_watermark_cli.py -d ~/Pictures/vacation/ -p 90 -s small

# 自定义透明度和大尺寸水印
python ai_watermark_cli.py -f portrait.jpg -p 60 -s large

# 处理图片并保存到指定位置
python ai_watermark_cli.py -f original.jpg -o watermarked.jpg -p 75 -s medium
```

## 技术实现

- **图像处理**: 使用 Pillow (PIL) 库进行图像操作
- **图形界面**: 基于 tkinter 的现代化GUI设计
- **水印算法**: 完全复制原Android项目的水印位置和大小算法
- **透明度处理**: Alpha通道混合技术
- **原生水印**: 使用原项目的豆包AI水印图片

## 项目结构

```
ai-watermark-python/
├── ai_watermark.py              # GUI版本主程序
├── ai_watermark_cli.py          # 命令行版本
├── doubao_ai_watermark.png      # 豆包AI水印图片
├── requirements.txt             # 依赖包列表
├── install.py                   # 安装脚本
└── README.md                    # 说明文档
```

## 开发环境

推荐使用 Conda 环境管理：

```bash
# 创建新环境
conda create -n ai-watermark python=3.9
conda activate ai-watermark

# 安装依赖
pip install -r requirements.txt

# 运行程序
python ai_watermark.py
```

## 许可证

本项目基于原开源项目 [kazutoiris/ai-watermark](https://github.com/kazutoiris/ai-watermark) 进行Python重构。

## 贡献

欢迎提交 Issue 和 Pull Request！

- **报告问题**: 发现bug请提交issue
- **功能建议**: 有好的想法欢迎讨论  
- **代码贡献**: 欢迎提交PR改进代码

## 致谢

感谢原作者 [kazutoiris](https://github.com/kazutoiris) 的优秀开源项目！

---

**享受使用吧！** 