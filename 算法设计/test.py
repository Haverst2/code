def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)

    # 创建一个(m+1) x (n+1)的二维数组，用于存储中间结果
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填充dp数组，根据字符匹配情况更新dp表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 从dp表格中回溯以构造最长公共子序列
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    # 最长公共子序列是逆序的，所以需要翻转
    lcs.reverse()

    return "".join(lcs)

# 示例用法
X = "ABCBDAB"
Y = "BDCAB"
result = longest_common_subsequence(X, Y)
print("最长公共子序列为:", result)
