#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 水印工具
给照片添加豆包AI生成的水印，创建合理的推诿性
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PIL import Image, ImageTk
import threading
from pathlib import Path


class AIWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("跟我的AI说去吧！")
        self.root.geometry("800x650")
        self.root.resizable(False, False)  # 固定窗口大小
        
        # 设置窗口图标（如果水印图片存在）
        try:
            if Path("doubao_ai_watermark.png").exists():
                icon = ImageTk.PhotoImage(Image.open("doubao_ai_watermark.png").resize((32, 32)))
                self.root.iconphoto(True, icon)
        except:
            pass
        
        # 设置黑白配色主题
        self.primary_color = "#2d3748"  # 深灰色
        self.secondary_color = "#4a5568"  # 中灰色
        self.success_color = "#2d3748"  # 深灰色
        self.warning_color = "#718096"  # 浅灰色
        self.bg_color = "#ffffff"  # 白色背景
        self.border_color = "#e2e8f0"  # 淡灰色边框
        
        # 设置样式
        self.setup_styles()
        
        # 加载豆包AI水印图片
        self.watermark_image = self.load_watermark_image()
        
        # 初始化变量
        self.selected_files = []
        self.output_directory = tk.StringVar(value="与原图相同目录")
        self.opacity_var = tk.IntVar(value=70)
        self.auto_size_var = tk.BooleanVar(value=True)  # 自动尺寸复选框
        self.manual_size_var = tk.IntVar(value=50)  # 手动尺寸滑轨 (1-100)
        self.is_processing = False
        
        self.setup_ui()
        self.center_window()
        
    def setup_styles(self):
        """设置黑白配色样式"""
        self.root.configure(bg=self.bg_color)
        
        # 创建样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure('Primary.TButton',
                           background=self.primary_color,
                           foreground='white',
                           borderwidth=1,
                           focuscolor='none',
                           padding=(20, 10))
        
        self.style.configure('Secondary.TButton',
                           background=self.secondary_color,
                           foreground='white',
                           borderwidth=1,
                           focuscolor='none',
                           padding=(15, 8))
        
        self.style.configure('Success.TButton',
                           background=self.primary_color,
                           foreground='white',
                           borderwidth=1,
                           focuscolor='none',
                           padding=(20, 12))
        
        # 配置进度条样式
        self.style.configure('Custom.Horizontal.TProgressbar',
                           background=self.primary_color,
                           troughcolor=self.border_color,
                           borderwidth=1,
                           lightcolor=self.primary_color,
                           darkcolor=self.primary_color)
        
    def load_watermark_image(self):
        """加载豆包AI水印图片"""
        watermark_path = Path("doubao_ai_watermark.png")
        if watermark_path.exists():
            try:
                return Image.open(watermark_path).convert("RGBA")
            except Exception as e:
                print(f"加载水印图片失败: {e}")
                return None
        else:
            print("未找到豆包AI水印图片文件")
            return None
        
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # 头部区域
        self.create_header(main_frame)
        
        # 主要内容区域
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # 左侧：文件选择区域 (占60%宽度)
        left_frame = tk.Frame(content_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.create_file_section(left_frame)
        
        # 右侧：设置选项区域 (占40%宽度)
        right_frame = tk.Frame(content_frame, bg=self.bg_color, width=280)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        right_frame.pack_propagate(False)  # 保持固定宽度
        
        self.create_settings_section(right_frame)
        
        # 状态区域
        self.create_status_area(main_frame)
        
    def create_header(self, parent):
        """创建头部区域"""
        header_frame = tk.Frame(parent, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 主标题 (去掉图标)
        title_label = tk.Label(
            header_frame,
            text="跟我的AI说去吧！",
            font=("微软雅黑", 26, "bold"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="豆包AI水印添加",
            font=("微软雅黑", 14),
            fg=self.secondary_color,
            bg=self.bg_color
        )
        subtitle_label.pack(pady=(5, 15))
        
        # 分隔线
        separator = tk.Frame(header_frame, height=2, bg=self.border_color)
        separator.pack(fill=tk.X)
        
    def create_file_section(self, parent):
        """创建文件选择区域"""
        # 输入文件区域
        input_frame = tk.LabelFrame(
            parent,
            text="  📁 选择图片文件  ",
            font=("微软雅黑", 12, "bold"),
            fg=self.primary_color,
            bg=self.bg_color,
            relief=tk.SOLID,
            borderwidth=1
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 选择图片按钮
        select_frame = tk.Frame(input_frame, bg=self.bg_color)
        select_frame.pack(fill=tk.X, padx=20, pady=15)
        
        self.select_btn = ttk.Button(
            select_frame,
            text="🖼️ 选择图片文件",
            style='Primary.TButton',
            command=self.select_images
        )
        self.select_btn.pack(fill=tk.X)
        
        # 已选文件列表 (固定高度)
        self.file_list_frame = tk.Frame(input_frame, bg=self.bg_color, height=200)
        self.file_list_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.file_list_frame.pack_propagate(False)  # 保持固定高度
        
        # 输出路径区域
        output_frame = tk.LabelFrame(
            parent,
            text="  📂 输出设置  ",
            font=("微软雅黑", 12, "bold"),
            fg=self.primary_color,
            bg=self.bg_color,
            relief=tk.SOLID,
            borderwidth=1
        )
        output_frame.pack(fill=tk.X)
        
        # 输出路径选择
        path_frame = tk.Frame(output_frame, bg=self.bg_color)
        path_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(
            path_frame,
            text="保存路径:",
            font=("微软雅黑", 10, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        ).pack(anchor=tk.W, pady=(0, 5))
        
        path_select_frame = tk.Frame(path_frame, bg=self.bg_color)
        path_select_frame.pack(fill=tk.X)
        
        self.output_label = tk.Label(
            path_select_frame,
            textvariable=self.output_directory,
            font=("微软雅黑", 9),
            bg="#f8f9fa",
            fg=self.secondary_color,
            relief=tk.SOLID,
            borderwidth=1,
            anchor=tk.W,
            padx=10,
            pady=8
        )
        self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.output_btn = ttk.Button(
            path_select_frame,
            text="浏览",
            style='Secondary.TButton',
            command=self.select_output_directory
        )
        self.output_btn.pack(side=tk.RIGHT)
        
    def create_settings_section(self, parent):
        """创建设置选项区域"""
        settings_frame = tk.LabelFrame(
            parent,
            text="  ⚙️ 水印设置  ",
            font=("微软雅黑", 12, "bold"),
            fg=self.primary_color,
            bg=self.bg_color,
            relief=tk.SOLID,
            borderwidth=1
        )
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        settings_content = tk.Frame(settings_frame, bg=self.bg_color)
        settings_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 透明度设置
        opacity_frame = tk.Frame(settings_content, bg=self.bg_color)
        opacity_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            opacity_frame,
            text="💧 透明度",
            font=("微软雅黑", 11, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        ).pack(anchor=tk.W, pady=(0, 8))
        
        self.opacity_scale = tk.Scale(
            opacity_frame,
            from_=30,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.opacity_var,
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg=self.primary_color,
            highlightthickness=0,
            troughcolor=self.border_color,
            activebackground=self.secondary_color,
            command=self.update_opacity_label,
            length=220
        )
        self.opacity_scale.pack(fill=tk.X)
        
        self.opacity_value_label = tk.Label(
            opacity_frame,
            text="70%",
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg=self.secondary_color
        )
        self.opacity_value_label.pack(pady=(5, 0))
        
        # 水印大小设置
        size_frame = tk.Frame(settings_content, bg=self.bg_color)
        size_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            size_frame,
            text="📏 水印大小",
            font=("微软雅黑", 11, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # 自动尺寸复选框
        self.auto_size_checkbox = tk.Checkbutton(
            size_frame,
            text="自动调整尺寸",
            variable=self.auto_size_var,
            font=("微软雅黑", 10),
            bg=self.bg_color,
            fg=self.primary_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.primary_color,
            command=self.toggle_size_mode
        )
        self.auto_size_checkbox.pack(anchor=tk.W, pady=(0, 8))
        
        # 手动尺寸调节框架 (初始隐藏)
        self.manual_size_frame = tk.Frame(size_frame, bg=self.bg_color)
        
        tk.Label(
            self.manual_size_frame,
            text="手动调节:",
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg=self.secondary_color
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.size_scale = tk.Scale(
            self.manual_size_frame,
            from_=20,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.manual_size_var,
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg=self.primary_color,
            highlightthickness=0,
            troughcolor=self.border_color,
            activebackground=self.secondary_color,
            command=self.update_size_label,
            length=220
        )
        self.size_scale.pack(fill=tk.X)
        
        self.size_value_label = tk.Label(
            self.manual_size_frame,
            text="50%",
            font=("微软雅黑", 9),
            bg=self.bg_color,
            fg=self.secondary_color
        )
        self.size_value_label.pack(pady=(5, 0))
        
        # 处理按钮
        self.process_btn = ttk.Button(
            settings_content,
            text="🚀 开始处理",
            style='Success.TButton',
            command=self.process_images,
            state=tk.DISABLED
        )
        self.process_btn.pack(fill=tk.X, pady=(30, 0))
        
    def create_status_area(self, parent):
        """创建状态显示区域"""
        status_frame = tk.Frame(parent, bg=self.bg_color)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 进度条
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=400,
            style='Custom.Horizontal.TProgressbar'
        )
        
        # 状态标签
        self.status_label = tk.Label(
            status_frame,
            text="请选择要处理的图片文件",
            font=("微软雅黑", 11),
            fg=self.secondary_color,
            bg=self.bg_color
        )
        self.status_label.pack(pady=10)
        
    def update_opacity_label(self, value):
        """更新透明度标签"""
        self.opacity_value_label.config(text=f"{value}%")
        
    def update_size_label(self, value):
        """更新尺寸标签"""
        self.size_value_label.config(text=f"{value}%")
        
    def toggle_size_mode(self):
        """切换自动/手动尺寸模式"""
        if self.auto_size_var.get():
            # 自动模式，隐藏手动调节
            self.manual_size_frame.pack_forget()
        else:
            # 手动模式，显示手动调节
            self.manual_size_frame.pack(fill=tk.X, pady=(0, 0))
        
    def select_images(self):
        """选择图片文件"""
        if self.watermark_image is None:
            messagebox.showerror("错误", "豆包AI水印图片加载失败，请确保 doubao_ai_watermark.png 文件存在")
            return
            
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
            ("所有文件", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="选择要添加水印的图片",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
            self.status_label.config(
                text=f"已选择 {len(files)} 张图片，配置参数后点击开始处理",
                fg=self.primary_color
            )
            self.process_btn.config(state=tk.NORMAL)
        else:
            self.selected_files = []
            self.update_file_list()
            self.status_label.config(
                text="请选择要处理的图片文件",
                fg=self.secondary_color
            )
            self.process_btn.config(state=tk.DISABLED)
            
    def update_file_list(self):
        """更新文件列表显示"""
        # 清除旧的列表
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
            
        if not self.selected_files:
            no_files_label = tk.Label(
                self.file_list_frame,
                text="暂未选择文件",
                font=("微软雅黑", 10),
                fg=self.warning_color,
                bg=self.bg_color
            )
            no_files_label.pack(expand=True)
            return
            
        # 显示选中的文件
        files_label = tk.Label(
            self.file_list_frame,
            text=f"已选择 {len(self.selected_files)} 个文件:",
            font=("微软雅黑", 10, "bold"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        files_label.pack(anchor=tk.W, pady=(5, 8))
        
        # 创建文本框显示文件名 (固定高度，内置滚动)
        files_text = tk.Text(
            self.file_list_frame,
            height=8,
            font=("微软雅黑", 9),
            bg="#f8f9fa",
            fg=self.secondary_color,
            relief=tk.SOLID,
            borderwidth=1,
            wrap=tk.WORD,
            state=tk.NORMAL
        )
        
        # 添加滚动条
        scrollbar_files = ttk.Scrollbar(self.file_list_frame, orient="vertical", command=files_text.yview)
        files_text.configure(yscrollcommand=scrollbar_files.set)
        
        for i, file_path in enumerate(self.selected_files, 1):
            filename = Path(file_path).name
            files_text.insert(tk.END, f"{i}. {filename}\n")
            
        files_text.config(state=tk.DISABLED)
        
        # 布局文本框和滚动条
        files_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_files.pack(side=tk.RIGHT, fill=tk.Y)
        
    def select_output_directory(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_directory.set(directory)
        else:
            self.output_directory.set("与原图相同目录")
            
    def add_watermark(self, image_path, output_path, opacity, size_setting):
        """为单张图片添加豆包AI水印"""
        try:
            # 打开原图
            with Image.open(image_path) as img:
                # 转换为RGBA模式以支持透明度
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 计算水印大小
                if self.auto_size_var.get():
                    # 自动模式：基于原项目算法
                    scale = img.width / 864.0
                else:
                    # 手动模式：根据滑轨值计算
                    # 将1-100的值映射到合理的缩放范围
                    size_percent = self.manual_size_var.get()
                    # 映射到0.1到1.5的缩放范围
                    scale = 0.1 + (size_percent / 100.0) * 1.4
                    scale = scale * (img.width / 864.0)  # 基于图片宽度调整
                
                # 确保最小尺寸
                scale = max(scale, 0.1)
                
                # 调整水印大小
                watermark_width = int(self.watermark_image.width * scale)
                watermark_height = int(self.watermark_image.height * scale)
                watermark_resized = self.watermark_image.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
                
                # 调整水印透明度
                if opacity < 100:
                    watermark_with_opacity = Image.new('RGBA', watermark_resized.size, (255, 255, 255, 0))
                    watermark_data = watermark_resized.getdata()
                    new_data = []
                    for item in watermark_data:
                        new_alpha = int(item[3] * opacity / 100)
                        new_data.append((item[0], item[1], item[2], new_alpha))
                    watermark_with_opacity.putdata(new_data)
                    watermark_resized = watermark_with_opacity
                
                # 计算水印位置（右下角，留边距）
                margin = 12
                x = img.width - watermark_width - margin
                y = img.height - watermark_height - margin
                
                # 粘贴水印
                img.paste(watermark_resized, (x, y), watermark_resized)
                
                # 转换回RGB模式以保存为JPEG
                if img.mode == 'RGBA':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1])
                    img = rgb_img
                
                # 保存图片
                img.save(output_path, 'JPEG', quality=90)
                return str(output_path)
                
        except Exception as e:
            raise Exception(f"处理图片 {image_path} 时出错: {str(e)}")
    
    def process_images(self):
        """处理所有选中的图片"""
        if not self.selected_files:
            messagebox.showwarning("警告", "请先选择要处理的图片")
            return
            
        if self.watermark_image is None:
            messagebox.showerror("错误", "豆包AI水印图片加载失败")
            return
            
        if self.is_processing:
            return
            
        def process_thread():
            try:
                self.is_processing = True
                
                # 更新UI状态
                self.root.after(0, lambda: self.process_btn.config(state=tk.DISABLED, text="处理中..."))
                self.root.after(0, lambda: self.progress.pack(fill=tk.X, pady=(0, 10)))
                self.root.after(0, lambda: self.progress.start())
                self.root.after(0, lambda: self.status_label.config(
                    text="正在处理图片，请稍候...", 
                    fg=self.warning_color
                ))
                
                opacity = self.opacity_var.get()
                output_dir = self.output_directory.get()
                processed_files = []
                
                for i, file_path in enumerate(self.selected_files):
                    self.root.after(0, lambda i=i: self.status_label.config(
                        text=f"正在处理第 {i+1}/{len(self.selected_files)} 张图片...",
                        fg=self.warning_color
                    ))
                    
                    try:
                        # 确定输出路径
                        file_path_obj = Path(file_path)
                        if output_dir == "与原图相同目录":
                            output_path = file_path_obj.parent / f"{file_path_obj.stem}_watermarked{file_path_obj.suffix}"
                        else:
                            output_path = Path(output_dir) / f"{file_path_obj.stem}_watermarked{file_path_obj.suffix}"
                            
                        result_path = self.add_watermark(file_path, str(output_path), opacity, None)
                        processed_files.append(result_path)
                    except Exception as e:
                        error_msg = f"处理文件 {Path(file_path).name} 时出错: {str(e)}"
                        self.root.after(0, lambda msg=error_msg: messagebox.showerror("处理错误", msg))
                
                # 处理完成
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.progress.pack_forget())
                self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL, text="🚀 开始处理"))
                
                if processed_files:
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"✅ 成功处理 {len(processed_files)} 张图片！",
                        fg=self.primary_color
                    ))
                    
                    success_msg = f"成功处理 {len(processed_files)} 张图片！\n\n"
                    if output_dir == "与原图相同目录":
                        success_msg += "文件已保存在原图片同目录下，文件名添加了 '_watermarked' 后缀。"
                    else:
                        success_msg += f"文件已保存到: {output_dir}"
                    
                    self.root.after(0, lambda: messagebox.showinfo("处理完成", success_msg))
                else:
                    self.root.after(0, lambda: self.status_label.config(
                        text="❌ 处理失败，请检查文件和设置",
                        fg="#dc3545"
                    ))
                    
            except Exception as e:
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.progress.pack_forget())
                self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL, text="🚀 开始处理"))
                self.root.after(0, lambda e=e: messagebox.showerror("错误", f"处理过程中出现错误: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(
                    text="❌ 处理过程中出现错误",
                    fg="#dc3545"
                ))
            finally:
                self.is_processing = False
        
        # 在后台线程中处理图片
        thread = threading.Thread(target=process_thread, daemon=True)
        thread.start()


def main():
    """主函数"""
    root = tk.Tk()
    app = AIWatermarkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main() 