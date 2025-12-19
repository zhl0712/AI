import tkinter as tk
from tkinter import messagebox

def button_clicked():
    """按钮点击事件处理函数"""
    messagebox.showinfo("提示", "按钮被点击了！")

def main():
    """主函数，创建窗口和按钮"""
    # 创建主窗口
    root = tk.Tk()
    root.title("Python 按钮窗口")
    root.geometry("300x200")
    
    # 创建按钮
    button = tk.Button(
        root, 
        text="点击我", 
        command=button_clicked,
        font=("Arial", 12),
        width=10,
        height=2
    )
    
    # 将按钮放置在窗口中央
    button.pack(expand=True)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()