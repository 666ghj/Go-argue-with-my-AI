#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 水印工具 - 安装脚本
自动安装依赖并验证环境
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return True
        else:
            print(f"❌ {description} 失败")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} 出现异常: {e}")
        return False


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 7):
        print("✅ Python版本符合要求 (>= 3.7)")
        return True
    else:
        print("❌ Python版本过低，需要 3.7 或更高版本")
        return False


def install_dependencies():
    """安装依赖包"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ 未找到 requirements.txt 文件")
        return False
    
    print("📦 正在安装依赖包...")
    
    # 检查是否在conda环境中
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"🌟 检测到Conda环境: {conda_env}")
    
    # 尝试安装依赖
    commands = [
        "pip install --upgrade pip",
        "pip install -r requirements.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"执行: {cmd}"):
            return False
    
    return True


def test_imports():
    """测试是否能正确导入所需模块"""
    print("🧪 测试模块导入...")
    
    modules = [
        ("PIL", "Pillow"),
        ("tkinter", "tkinter (通常自带)"),
    ]
    
    all_success = True
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name} 导入成功")
        except ImportError:
            print(f"❌ {display_name} 导入失败")
            all_success = False
    
    return all_success


def create_test_command():
    """创建测试命令"""
    print("📝 创建测试命令...")
    
    test_commands = [
        "# 测试GUI版本",
        "python ai_watermark.py",
        "",
        "# 测试命令行版本",
        "python ai_watermark_cli.py --help",
        "",
        "# 处理单张图片示例",
        "# python ai_watermark_cli.py -f your_image.jpg --preset doubao",
        "",
        "# 批量处理示例", 
        "# python ai_watermark_cli.py -d ./images/ --preset chatgpt -p 80"
    ]
    
    with open("test_commands.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(test_commands))
    
    print("✅ 测试命令已保存到 test_commands.txt")


def main():
    """主函数"""
    print("🚀 AI 水印工具 - 安装程序")
    print("="*50)
    
    # 检查Python版本
    if not check_python_version():
        print("\n❌ 安装失败：Python版本不符合要求")
        sys.exit(1)
    
    print()
    
    # 安装依赖
    if not install_dependencies():
        print("\n❌ 安装失败：无法安装依赖包")
        sys.exit(1)
    
    print()
    
    # 测试导入
    if not test_imports():
        print("\n⚠️ 警告：部分模块导入失败，程序可能无法正常运行")
    
    print()
    
    # 创建测试命令
    create_test_command()
    
    print()
    print("🎉 安装完成！")
    print()
    print("📖 使用方法：")
    print("  GUI版本: python ai_watermark.py")
    print("  命令行版本: python ai_watermark_cli.py --help")
    print()
    print("📚 详细说明请查看: README_Python.md")


if __name__ == "__main__":
    main() 