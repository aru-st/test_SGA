#/*******************/
#/* 単純GAの処理実装 */
#/*******************/

#8bitのbit列を10コ作成
def initial_values():
    a = []
    for i in range(10):
        k = random.randint(0, 2**8-1)
        k = bin(k)[2:].rjust(8, "0")
        a.append(k)   
    return a

#適応度関数の評価の計算
#条件検証に使うのは"重さ", 返り値は"価値"であることに注意する
def evalulate_calculate(bit, lim, w, v):
    rlt_v = 0
    rlt_w = 0
    for i in range(len(bit)):
        rlt_w += int(bit[i]) * w[i]
        rlt_v += int(bit[i]) * v[i]

    if rlt_w <= lim: #1)
        return rlt_v
    else: #2)
        return 0

#評価関数を返す
def evalulate(bits, lim, w, v, cells, Max_evals, Avg_evals):

    total_eval = 0
    eval_li = []
    for i in range(len(bits)):
        total_eval += evalulate_calculate(bits[i], lim, w, v)
        eval_li.append(evalulate_calculate(bits[i], lim, w, v))
        #print(evalulate_calculate(bits[i]))

    cells.append(eval_li)
    Max_evals.append(max(eval_li))
    Avg_evals.append(total_eval / len(bits))

    #print("total_eval is", total_eval)
    #print("eval_Avg is",total_eval / len(bits))
    #print("eval_li is", eval_li)

    #print("all_bit is")
    #all_bit()

    #順に(平均), (最大適応度), (各個体の適応度) が返り値
    return total_eval, total_eval / len(bits) ,max(eval_li), eval_li

#選択を行う
def selection(bits, tol_eva, eva_li):

    #累積和でその値の範囲であれば選択するということを行う
    acm = [0] + list(itertools.accumulate(eva_li))

    #print("acm is", acm)

    for i in range(len(bits)):
        x = random.randint(0, tol_eva)

        #print("x is", x)

        for j in range(len(acm)-1):
            if acm[j] <= x < acm[j+1]:
                a = j+1 #j番目の個体を選択するということ
                print(a)
                break
        else:
            #x = total_evalのときだけ別途で処理
            a = len(bits)
            #print(a)

        #bit列の置き換えを行う
        bits[i] = bits[a-1]
        return bits

#交叉を行う関数
def crossover(bits):
    #交叉を行う親個体, どこで交叉させるかの分離点決める
    #親個体: a, b 分離点: c
    a, b = random.randint(0, len(bits)-1), random.randint(0, len(bits)-1)
    c = random.randint(1, len(bits[a])-2) #必ず1bit以上は行えるように上限を7にしておく

    #1-indexedにここだけしている
    #print("親個体のペア is", a+1, b+1)
    #print("分離点 is", c+1)

    #print(bits[a])
    #print(bits[b])

    #交叉の実行
    temp_A = bits[a][c:]
    temp_B = bits[b][c:]
    bits[a] = bits[a][:c] + temp_B
    bits[b] = bits[b][:c] + temp_A

    return bits

def mutation(bits):
    chk = random.randint(0, 100)
    if chk > 5: #発生確率は5%
        #print("mutation failed")
        return

    #突然変異を行う親個体(1つ)とどのbitを変化させるかをチェック
    #親個体: a 行うbit位置: c
    a = random.randint(0, len(bits)-1)
    c = random.randint(2, len(bits[a])-1)

    #print("何番目の数値が変わるのか", a+1)
    #print("何bit目か", c+1)
    #print(bits[a])

    #対立遺伝子にする(bitを反転)
    if bits[a][c] == "1":
        bits[a] = bits[a][:c-1] + "0" + bits[a][c:]
    else:
        bits[a] = bits[a][:c-1] + "1" + bits[a][c:]

    #print("mutation conducted")

    return bits

#GAの処理を実行する関数
def solve(lim):

    #v[i]: 物体iの価値, w[i]: 物体iの重さ
    v = [3, 4, 5, 8, 8, 3, 5, 15]
    w = [6, 6, 6, 7, 7, 9, 11, 13]

    #cells: 各世代ごとの各個体の適応度
    #Max_evals: 各世代ごとの最大適応度
    #Avg_evals: 各世代ごとの平均適応度
    #limit: 重さの制限
    cells = []
    Max_evals = []
    Avg_evals = []
    limit = lim

    bits = initial_values()

    for i in range(10):
        T, p, q, r = evalulate(bits, limit, w, v)
        cells.append(r)
        Max_evals.append(q)
        Avg_evals.append(p)

        bits = selection(bits, T, r)

        bits = crossover(bits)
        bits = mutation(bits)

    return cells, Max_evals, Avg_evals