
if __name__ == "__main__":
    import os
    # 将旧内容一并继承 在旧内容下在书写内容
    line_params = []
    # os.chdir(r"D:\TestPy\gitProjects")
    dir_list = os.listdir(r"D:\TestPy\webDesignProjects")
    f = open(r"D:\TestPy\webDesignProjects\项目注释.txt", "r+", encoding="utf-8")
    # 复制原文件内容
    for i in f:
        # file.write(i+"\n")
        if not i.endswith("\n"):
            i = i+"\n"
        line_params.append(i)
        # print(i)
    for i in dir_list:
        j = 0
        if ".zip" in i:
            i = i.replace(".zip", "", 1)
        for k in line_params:
            if i in k:
                j = 1
                break
        if j == 1:
            continue
        line_params.append(i+"\n")

    # 将指针定位至头部 从头开始写文件
    f.seek(0, 0)
    f.writelines(line_params)
    f.close()
