#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 水印工具 - 命令行版本
给照片添加豆包AI生成的水印
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image


def load_watermark_image():
    """加载豆包AI水印图片"""
    watermark_path = Path("doubao_ai_watermark.png")
    if watermark_path.exists():
        try:
            return Image.open(watermark_path).convert("RGBA")
        except Exception as e:
            print(f"加载水印图片失败: {e}")
            return None
    else:
        print("未找到豆包AI水印图片文件: doubao_ai_watermark.png")
        return None


def add_watermark(image_path, output_path=None, opacity=70, size="auto"):
    """
    为图片添加豆包AI水印
    
    Args:
        image_path (str): 输入图片路径
        output_path (str): 输出图片路径，如果为None则在原文件名后添加_watermarked
        opacity (int): 透明度（30-100）
        size (str): 水印大小（auto/small/medium/large）
    
    Returns:
        str: 输出文件路径
    """
    # 加载水印图片
    watermark_image = load_watermark_image()
    if watermark_image is None:
        raise Exception("无法加载豆包AI水印图片")
    
    try:
        # 打开原图
        with Image.open(image_path) as img:
            # 转换为RGBA模式以支持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 计算水印大小
            if size == "auto":
                # 基于原Android项目的逻辑：原图宽度/864
                scale = img.width / 864.0
            elif size == "small":
                scale = img.width / 1200.0
            elif size == "medium":
                scale = img.width / 800.0
            elif size == "large":
                scale = img.width / 600.0
            else:
                scale = img.width / 864.0
            
            # 确保最小尺寸
            scale = max(scale, 0.2)
            
            # 调整水印大小
            watermark_width = int(watermark_image.width * scale)
            watermark_height = int(watermark_image.height * scale)
            watermark_resized = watermark_image.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
            
            # 调整水印透明度
            if opacity < 100:
                # 创建透明度调整后的水印
                watermark_with_opacity = Image.new('RGBA', watermark_resized.size, (255, 255, 255, 0))
                
                # 调整alpha通道
                watermark_data = watermark_resized.getdata()
                new_data = []
                for item in watermark_data:
                    # item[3] 是alpha通道
                    new_alpha = int(item[3] * opacity / 100)
                    new_data.append((item[0], item[1], item[2], new_alpha))
                
                watermark_with_opacity.putdata(new_data)
                watermark_resized = watermark_with_opacity
            
            # 计算水印位置（右下角，留边距）
            margin = 12  # 与原Android项目保持一致
            x = img.width - watermark_width - margin
            y = img.height - watermark_height - margin
            
            # 粘贴水印
            img.paste(watermark_resized, (x, y), watermark_resized)
            
            # 转换回RGB模式以保存为JPEG
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1])
                img = rgb_img
            
            # 确定输出路径
            if output_path is None:
                file_path = Path(image_path)
                output_path = file_path.parent / f"{file_path.stem}_watermarked{file_path.suffix}"
            
            # 保存图片
            img.save(output_path, 'JPEG', quality=90)
            
            return str(output_path)
            
    except Exception as e:
        raise Exception(f"处理图片 {image_path} 时出错: {str(e)}")


def process_directory(input_dir, output_dir=None, opacity=70, size="auto"):
    """
    批量处理目录中的所有图片
    
    Args:
        input_dir (str): 输入目录
        output_dir (str): 输出目录，如果为None则在原目录下生成
        opacity (int): 透明度（30-100）
        size (str): 水印大小（auto/small/medium/large）
    
    Returns:
        list: 处理成功的文件列表
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise ValueError(f"输入目录不存在: {input_dir}")
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
    
    # 找到所有图片文件
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"在目录 {input_dir} 中未找到图片文件")
        return []
    
    processed_files = []
    
    for i, image_file in enumerate(image_files, 1):
        try:
            print(f"处理第 {i}/{len(image_files)} 张图片: {image_file.name}")
            
            if output_dir:
                output_path = Path(output_dir) / f"{image_file.stem}_watermarked{image_file.suffix}"
                os.makedirs(output_dir, exist_ok=True)
            else:
                output_path = None
            
            result_path = add_watermark(str(image_file), str(output_path) if output_path else None, 
                                      opacity, size)
            processed_files.append(result_path)
            print(f"✓ 完成: {result_path}")
            
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    return processed_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI 水印工具 - 为照片添加豆包AI生成水印")
    
    # 输入参数
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='单个图片文件路径')
    group.add_argument('-d', '--dir', help='图片目录路径（批量处理）')
    
    # 选项参数
    parser.add_argument('-o', '--output', help='输出路径（文件或目录）')
    parser.add_argument('-p', '--opacity', type=int, default=70, 
                       help='透明度 30-100 (默认: 70)')
    parser.add_argument('-s', '--size', choices=['auto', 'small', 'medium', 'large'], 
                       default='auto', help='水印大小 (默认: auto)')
    
    args = parser.parse_args()
    
    # 验证透明度参数
    if not 30 <= args.opacity <= 100:
        print("错误: 透明度必须在 30-100 之间")
        sys.exit(1)
    
    # 检查水印图片是否存在
    if not Path("doubao_ai_watermark.png").exists():
        print("错误: 未找到豆包AI水印图片文件 'doubao_ai_watermark.png'")
        print("请确保该文件与脚本在同一目录下")
        sys.exit(1)
    
    try:
        if args.file:
            # 处理单个文件
            if not os.path.exists(args.file):
                print(f"错误: 文件不存在 {args.file}")
                sys.exit(1)
            
            print(f"处理图片: {args.file}")
            print(f"参数: 透明度={args.opacity}%, 大小={args.size}")
            result_path = add_watermark(args.file, args.output, args.opacity, args.size)
            print(f"✓ 完成: {result_path}")
            
        elif args.dir:
            # 批量处理目录
            print(f"批量处理目录: {args.dir}")
            print(f"参数: 透明度={args.opacity}%, 大小={args.size}")
            processed_files = process_directory(args.dir, args.output, args.opacity, args.size)
            print(f"\n处理完成! 共处理 {len(processed_files)} 张图片")
            
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 