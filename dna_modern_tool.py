import os
import sys
import subprocess
import shutil

# ==========================================
# 现代 UI 版 DNA 处理程序源码
# ==========================================
APP_SOURCE_CODE = r"""
import customtkinter as ctk
from tkinter import messagebox
import sys

# 设置外观模式 (System 会自动跟随 Mac 的深色/浅色模式)
ctk.set_appearance_mode("System") 
# 设置颜色主题 (蓝色系，符合现代软件审美)
ctk.set_default_color_theme("blue") 

class ModernDNATool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 窗口基础设置 ---
        self.title("DNA Sequence Pro")
        self.geometry("800x650")

        # 配置 grid 布局权重，让界面自适应拉伸
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # 输入框区域
        self.grid_rowconfigure(4, weight=1) # 输出框区域

        # --- 1. 顶部：批量插入工具栏 (Card 样式) ---
        self.frame_tools = ctk.CTkFrame(self, corner_radius=10)
        self.frame_tools.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.lbl_tool_title = ctk.CTkLabel(self.frame_tools, text="⚡️ 快速插入 (Batch Insert)", font=("System", 14, "bold"))
        self.lbl_tool_title.pack(side="left", padx=15, pady=10)

        # 字符输入
        self.entry_char = ctk.CTkEntry(self.frame_tools, width=60, placeholder_text="Seq")
        self.entry_char.insert(0, "T")
        self.entry_char.pack(side="left", padx=5)

        self.lbl_x = ctk.CTkLabel(self.frame_tools, text="×", font=("System", 14))
        self.lbl_x.pack(side="left", padx=2)

        # 数量输入
        self.entry_count = ctk.CTkEntry(self.frame_tools, width=60, placeholder_text="Num")
        self.entry_count.insert(0, "10")
        self.entry_count.pack(side="left", padx=5)

        # 插入按钮
        self.btn_insert = ctk.CTkButton(self.frame_tools, text="插入", width=80, 
                                      fg_color="#3B8ED0", hover_color="#36719F",
                                      command=self.insert_sequence)
        self.btn_insert.pack(side="left", padx=15)

        # --- 2. 输入区域 ---
        self.lbl_input = ctk.CTkLabel(self, text="输入原始序列 (Input Sequence)", font=("System", 13))
        self.lbl_input.grid(row=1, column=0, padx=25, pady=(10, 0), sticky="w")

        self.input_text = ctk.CTkTextbox(self, font=("Menlo", 14), corner_radius=10, height=150)
        self.input_text.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.input_text.insert("0.0", "GTCA") # 默认文本

        # --- 3. 核心操作按钮 (大按钮) ---
        self.btn_convert = ctk.CTkButton(self, text="执行：反转 + 互补替换 (Run Reverse Complement)", 
                                       font=("System", 16, "bold"),
                                       height=50,
                                       fg_color="#2CC985", hover_color="#26A46E", # 现代绿色
                                       command=self.process_sequence)
        self.btn_convert.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # --- 4. 输出区域 ---
        self.lbl_output = ctk.CTkLabel(self, text="处理结果 (Result)", font=("System", 13))
        self.lbl_output.grid(row=4, column=0, padx=25, pady=(10, 0), sticky="w")

        self.output_text = ctk.CTkTextbox(self, font=("Menlo", 14), corner_radius=10, height=150, fg_color=("gray90", "gray20"))
        self.output_text.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="nsew")

    def insert_sequence(self):
        char = self.entry_char.get()
        count_str = self.entry_count.get()

        if not char or not count_str.isdigit():
            # 这里的 messagebox 还是用 tkinter 原生的，因为 ctk 没有自带弹窗，或者可以用 print
            # 为了美观，我们直接在输出框提示错误，或者忽略
            return

        full_str = char * int(count_str)
        self.input_text.insert("insert", full_str)
        self.input_text.focus()

    def process_sequence(self):
        # 1. 获取输入
        raw_seq = self.input_text.get("1.0", "end").strip().replace("\n", "").replace(" ", "").upper()

        if not raw_seq:
            return

        try:
            # 2. 核心逻辑：反转
            reversed_seq = raw_seq[::-1]

            # 3. 核心逻辑：互补
            # A->T, T->A, C->G, G->C
            trans_table = str.maketrans("ATCGN", "TAGCN")
            final_seq = reversed_seq.translate(trans_table)

            # 4. 输出
            self.output_text.delete("1.0", "end")
            self.output_text.insert("0.0", final_seq)

        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("0.0", f"Error: {str(e)}")

if __name__ == "__main__":
    app = ModernDNATool()
    app.mainloop()
"""


# ==========================================
# 自动构建工具逻辑
# ==========================================

def install_package(package):
    print(f"--> 正在检查/安装依赖: {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except:
        print(f"!!! 无法安装 {package}。请检查网络。")
        sys.exit(1)


def build_app():
    # 1. 检查并安装依赖
    try:
        import PyInstaller
    except ImportError:
        install_package("pyinstaller")

    try:
        import customtkinter
    except ImportError:
        install_package("customtkinter")

    print("\n=== 开始构建现代版 macOS 应用程序 ===")

    # 2. 写入源码文件
    source_filename = "dna_modern_tool.py"
    with open(source_filename, "w", encoding="utf-8") as f:
        f.write(APP_SOURCE_CODE)

    # 3. 运行 PyInstaller
    # --collect-all customtkinter: 这一点至关重要，因为 ctk 包含 json 和图片资源文件
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "DNA_Pro_Modern",
        "--collect-all", "customtkinter",  # 关键参数：打包 UI 库的所有资源
        source_filename
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ 构建成功！(Build Success)")
        print("📂 请打开 dist 文件夹，双击 DNA_Pro_Modern.app 运行")
        print("=" * 50 + "\n")
    except subprocess.CalledProcessError:
        print("❌ 构建失败，请查看上方错误信息。")
    finally:
        # 清理
        if os.path.exists(source_filename):
            os.remove(source_filename)
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("DNA_Pro_Modern.spec"):
            os.remove("DNA_Pro_Modern.spec")


if __name__ == "__main__":
    build_app()
# python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/18 12:30
# @Author  : KevinGZY
# @File    : build_modern_app.py
