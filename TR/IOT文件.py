"""
生成螺旋矩阵工具模块
"""

import numpy as np


def generate_spiral_matrix(start_number=1, size=4):
    """
    生成一个螺旋矩阵，从给定的起始数字开始，按顺时针方向填充
    
    Args:
        start_number (int): 起始数字，默认为1
        size (int): 矩阵大小，默认为4 (生成4x4矩阵)
    
    Returns:
        numpy.ndarray: 填充完成的螺旋矩阵
    """
    matrix = np.zeros((size, size), dtype=int)
    num = start_number
    top, bottom, left, right = 0, size - 1, 0, size - 1

    while top <= bottom and left <= right:
        # 从左到右填充上边
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1

        # 从上到下填充右边
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1

        # 从右到左填充下边
        if top <= bottom:
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = num
                num += 1
            bottom -= 1

        # 从下到上填充左边
        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1

    return matrix


def print_matrix_with_directions(matrix):
    """
    打印带方向箭头提示的螺旋矩阵
    
    Args:
        matrix (numpy.ndarray): 螺旋矩阵
    """
    size = matrix.shape[0]
    
    # 创建一个字符矩阵用于显示箭头
    direction_chars = np.full((size, size), ' ', dtype=object)
    
    # 定义方向箭头
    right_arrow = '→'
    down_arrow = '↓'
    left_arrow = '←'
    up_arrow = '↑'
    down_right_corner = '↘'
    down_left_corner = '↙'
    up_left_corner = '↖'
    up_right_corner = '↗'
    
    # 模拟螺旋路径并放置箭头
    top, bottom, left, right = 0, size - 1, 0, size - 1
    num = 1  # 用于跟踪当前位置
    
    while top <= bottom and left <= right:
        # 从左到右填充上边
        for i in range(left, right + 1):
            if i < right:  # 不是最后一个元素
                direction_chars[top][i] = right_arrow
            elif top+1 <= bottom:  # 是最后一个但不是最后一行
                direction_chars[top][i] = down_right_corner  # 转弯处
            num += 1
        top += 1

        # 从上到下填充右边
        for i in range(top, bottom + 1):
            if i < bottom:  # 不是最后一个元素
                direction_chars[i][right] = down_arrow
            elif right-1 >= left:  # 是最后一个但不是最后一列
                direction_chars[i][right] = down_left_corner  # 转弯处
            num += 1
        right -= 1

        # 从右到左填充下边
        if top <= bottom:
            for i in range(right, left - 1, -1):
                if i > left:  # 不是最后一个元素
                    direction_chars[bottom][i] = left_arrow
                elif bottom-1 >= top:  # 是最后一个但不是最后一行
                    direction_chars[bottom][i] = up_left_corner  # 转弯处
                num += 1
            bottom -= 1

        # 从下到上填充左边
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if i > top:  # 不是最后一个元素
                    direction_chars[i][left] = up_arrow
                elif left+1 <= right:  # 是最后一个但不是最后一列
                    direction_chars[i][left] = up_right_corner  # 转弯处
                num += 1
            left += 1
    
    # 打印带箭头的矩阵
    print("螺旋矩阵 (带方向箭头):")
    for i in range(size):
        row_str = ""
        for j in range(size):
            row_str += f"{matrix[i][j]:>3} {direction_chars[i][j]} "
        print(row_str)
    print()


def main():
    """主函数，演示螺旋矩阵的生成"""
    while True:
        try:
            user_input = input("请输入矩阵大小 (输入'exit'退出程序): ")
            if user_input.lower() == 'exit':
                print("程序已退出。")
                break
            
            size = int(user_input)
            if size <= 0:
                print("请输入一个正整数！")
                continue
                
            start_number = 1
            spiral_matrix = generate_spiral_matrix(start_number, size)
            print_matrix_with_directions(spiral_matrix)
        except ValueError:
            print("请输入一个有效的整数或'exit'！")
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()