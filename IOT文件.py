import numpy as np

def generate_spiral_matrix(start_number):
    size = 4
    matrix = np.zeros((size, size), dtype=int)
    num = start_number
    top, bottom, left, right = 0, size - 1, 0, size - 1

    while top <= bottom and left <= right:
        # 从左到右填充一行
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1

        # 从上到下填充一列
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1

        # 从右到左填充一行
        if top <= bottom:
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = num
                num += 1
            bottom -= 1

        # 从下到上填充一列
        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1

    return matrix

# 使用示例
start_number = 1
spiral_matrix = generate_spiral_matrix(start_number)
print(spiral_matrix)
