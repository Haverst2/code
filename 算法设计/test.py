def partition(arr, low, high):
    pivot = arr[high]  # 选择最后一个元素作为主元素
    i = low - 1  # 初始化较小元素的索引

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def linear_time_select(arr, low, high, k):
    if low == high:
        return arr[low]

    # 获取主元素的位置
    pivot_index = partition(arr, low, high)

    # 计算主元素在有序数组中的位置
    rank = pivot_index - low + 1

    if k == rank:
        return arr[pivot_index]
    elif k < rank:
        return linear_time_select(arr, low, pivot_index - 1, k)
    else:
        return linear_time_select(arr, pivot_index + 1, high, k - rank)

# 测试线性时间选择算法
arr = [3, 2, 1, 5, 4]
k = 3
result = linear_time_select(arr, 0, len(arr) - 1, arr[0])
print(f"The {k}-th smallest element is {result}")
