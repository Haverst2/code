# 打开文件
with open('example.txt', 'r') as file:
    # 逐行读取文件内容
    lines = file.readlines()

    # 新建一个列表来存储删除前两个字母后的每行内容
    new_lines = []

    i = 1
    # 遍历每行内容
    for line in lines:
        if(i<10):
            # 删除前两个字母
            new_line = line[1:]
        if(i>=10 & i<100):
            new_line = line[2:]
        if(i>=100 & i<1000):
            new_line = line[3:]
        
        # 添加到新的列表中
        new_lines.append(new_line)
        i = i+1

# 将删除前两个字母后的内容写回文件
with open('example1.txt', 'w') as file:
    file.writelines(new_lines)