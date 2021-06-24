



if __name__ == "__main__":
    f = open("test.txt", "r+")
    for i in f:
        print(i)
        if "b" in i:
            i = "bb"

    f.close()