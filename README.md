# 跟我的AI说去吧！

![image](https://github.com/user-attachments/assets/62d9f65c-36a1-46ae-bf80-60ab30930942)

**为照片添加豆包AI生成的水印**

<p align="left">
  <img src="https://github.com/user-attachments/assets/9e96d20c-93fd-469e-87c9-e1d9e372f955" alt="1" width="48%">
  <img src="https://github.com/user-attachments/assets/27d83689-c52a-4eed-bc04-931d9b6fb32f" alt="1_watermarked" width="48%">
</p>

## 快速开始

### 安装依赖

```bash
pip install Pillow>=10.0.0
```

### 使用方法

#### 1. 图形界面版本

```bash
python ai_watermark.py
```

<p align="left">
  <img src="https://github.com/user-attachments/assets/6a57b599-414d-439a-904b-758bdad5d9be" alt="1" width="48%">
</p>

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

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--file` | `-f` | 单个图片文件路径 | `-f photo.jpg` |
| `--dir` | `-d` | 图片目录路径（批量） | `-d ./photos/` |
| `--output` | `-o` | 输出路径 | `-o result.jpg` |
| `--opacity` | `-p` | 透明度 (30-100) | `-p 80` |
| `--size` | `-s` | 水印大小 | `-s large` |

## 设计目标

- **创建合理推诿** - 为暴露的私人内容提供合理的推诿性
- **保持归属模糊** - 在社区中保持归属的模糊性  
- **建立隐私防护** - 为意外的隐私分发建立防护

本项目基于原开源项目 [kazutoiris/ai-watermark](https://github.com/kazutoiris/ai-watermark) 进行Python重构。

## 贡献

欢迎提交 Issue 和 Pull Request！

- **报告问题**: 发现bug请提交issue
- **功能建议**: 有好的想法欢迎讨论  
- **代码贡献**: 欢迎提交PR改进代码

## 致谢

感谢原作者 [kazutoiris](https://github.com/kazutoiris) 的优秀开源项目！
