



class GuressPwd(object):

    def case1(self, yuan: int, san: int, case_num: int):
        num1 = case_num
        num2 = case_num + 1
        num3 = case_num + 2
        if yuan == 3:
            print(f"Bingo--->{num1}{num2}{num3}")

        if yuan == 1 and san == 2:
            print(f"此时依次输入{num1}{num3}{num2}, {num3}{num2}{num1}, {num2}{num1}{num3}即可")

        if san == 3:
            print(f"此时依次输入{num2}{num3}{num1}, {num3}{num1}{num2}即可")

    def guess(self):
        over = 1
        while over:
            print("\n\n输入123时 ⭕，Δ的值：")

            X1, X2 = input().strip().split(" ")
            if not str(X1).isdigit() or not str(X2).isdigit():
                print("请输入正确格式的值")
                continue
            X1 = int(X1)
            X2 = int(X2)
            X = X1 + X2
            if X == 3:
                self.case1(yuan=X1, san=X2, case_num=1)
                continue
            # -----------------------------

            print("输入456时 ⭕，Δ的值：")
            Y1, Y2 = input().strip().split(" ")
            if not str(Y1).isdigit() and not str(Y2).isdigit():
                print("请输入正确格式的值")
                continue
            Y1 = int(Y1)
            Y2 = int(Y2)
            Y = Y1 + Y2
            if Y == 3:
                self.case1(yuan=Y1, san=Y2, case_num=4)
                continue
            # -----------------------------
            if X + Y == 3:
                if X == 2 and Y == 1:  # 2+1+0情形
                    if X1 == 2 and Y1 == 1:
                        print("输入124\n可能情况\t126\t153\t423\n⭕   Δ  \t20\t10\t11")
                    if X1 == 2 and Y2 == 1:
                        print(f"""输入564\n可能情况\t124\t125\t143\t163\t523\t623\n⭕   Δ  \t10\t01\t01\t10\t10\t01\n
        
        10
        可能情况    124    163    523
        ⭕    Δ    11      10     01
        264
                                
        01
        可能情况   125    143    623
        ⭕    Δ    02    00      11
        652
                                
                              """)
                    if X1 == 1 and X2 == 1 and Y1 == 1:
                        print(f"""
                        
                        可能情况    152     136     326     421     253     413
                        ⭕   Δ     30       10      01     02      11      01
                        152
                        """)
                continue

            # -----------------------------
            print("输入789时 ⭕，Δ的值：")
            Z1, Z2 = input().strip().split(" ")
            if not str(Z1).isdigit() and not str(Z2).isdigit():
                print("请输入正确格式的值")
                continue
            Z1 = int(Z1)
            Z2 = int(Z2)
            Z = Z1 + Z2
            if Z == 3:
                self.case1(yuan=Y1, san=Y2, case_num=7)
                continue



if __name__ == "__main__":
    g = GuressPwd()
    g.guess()