import streamlit as st
import itertools
import matplotlib
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#/*******************/
#/* 単純GAの処理実装 */
#/*******************/

#8bitのbit列を10コ作成
def initial_values():
    global bits
    global W #len(W)を取得するために宣言
    
    for i in range(10): #個体数は一定でいいだろ()
        k = random.randint(0, 2**len(W)-1)
        k = bin(k)[2:].rjust(8, "0")
        bits.append(k)


#適応度関数の評価の計算
#条件検証に使うのは"重さ", 返り値は"価値"であることに注意する

#def evalulate_calculate(bit, lim, w, v):
#    rlt_v = 0
#    rlt_w = 0
#    for i in range(len(bit)):
#        rlt_w += int(bit[i]) * w[i]
#        rlt_v += int(bit[i]) * v[i]
#
#    if rlt_w <= lim: #1)
#        return rlt_v
#    else: #2)
#        return 0

#評価関数を返す
def evalulate():
    global bits
    global limit
    global W
    global V
    global cells
    global Max_evals
    global Avg_evals
    global eval_li
    global total_eval

    total_eval = 0
    eval_li = []
    for i in range(len(bits)):
        rlt_v = 0
        rlt_w = 0
        for j in range(len(bits[i])):
            rlt_w += int(bits[i][j]) * W[j]
            rlt_v += int(bits[i][j]) * V[j]

        #評価値の決定
        if rlt_w <= limit: #1)
            rlt_v = rlt_v
        else: #2)
            rlt_v = 0
        
        #評価値を反映
        total_eval += rlt_v
        eval_li.append(rlt_v)

        #total_eval += evalulate_calculate(bits[i], lim, w, v)
        #eval_li.append(evalulate_calculate(bits[i], lim, w, v))
        #print(evalulate_calculate(bits[i]))


    cells.append(eval_li)
    Max_evals.append(max(eval_li))
    Avg_evals.append(total_eval / len(bits))

    #print("total_eval is", total_eval)
    #print("eval_Avg is",total_eval / len(bits))
    #print("eval_li is", eval_li)

    #print("all_bit is")
    #all_bit()

#選択を行う
def selection():

    global bits
    global eval_li
    global total_eval

    #累積和でその値の範囲であれば選択するということを行う
    acm = [0] + list(itertools.accumulate(eval_li))

    #print("acm is", acm)

    for i in range(len(bits)):
        x = random.randint(0, total_eval)

        #print("x is", x)

        for j in range(len(acm)-1):
            if acm[j] <= x < acm[j+1]:
                a = j+1 #j番目の個体を選択するということ
                
                #print(a)

                break
        else:
            #x = total_evalのときだけ別途で処理
            a = len(bits)
            #print(a)

        #bit列の置き換えを行う
        bits[i] = bits[a-1]

        #return bits

#交叉を行う関数
def crossover():

    global bits

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

    #return bits

def mutation():

    global bits

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

    #return bits

#GAの処理を実行する関数
#W, V: それぞれの物体の重さ, 価値, limit: 重さの総和の上限
def solve():

    global bits
    global limit
    global W
    global V
    global cells
    global Max_evals
    global Avg_evals
    global eval_li
    global total_eval
    global generations

    #必要な変数は事前に宣言しておく

    #cells: 各世代ごとの各個体の適応度
    #Max_evals: 各世代ごとの最大適応度
    #Avg_evals: 各世代ごとの平均適応度
    
    
    #cells = []
    #Max_evals = []
    #Avg_evals = []

    #eval_li = []
    #total_eval = 0

    #bit列を乱数により作成(globalで宣言しているんので引数は不要)
    initial_values()

    #print(bits)

    for i in range(generations):
        #各種処理を実行(globalで宣言しているので引数は不要)
        evalulate()
        selection()
        crossover()
        mutation()

        #print(bits)

    #return cells, Max_evals, Avg_evals

#/*******************/
#/* Streamlitの実装 */
#/*  UI, 入力部分   */
#/*******************/

#マークダウン記法での記述
st.write("""
# Simple GA Model

This model sloves the Knapsack problem!
""")

st.subheader("Evalulation Function details")

st.write("""
i) if f(x) <= limit: f(x) , 
""")

st.write("""
ii) if f(x) > limit: 0
""")

st.subheader("Cautions")

st.write("""
These values are Natural Numbers.
""")

st.write("""
weight_total_limit, numbers, weight_limit, value_limit > 0
""")


#重さの上限
limit = st.number_input("weight_total_limit", value=10)

#物体の個数
numbers = st.number_input("numbers", value=5)

#各物体の重さ, 価値の上限を設定
w_limit = st.number_input("weight_limit", value=10)
v_limit = st.number_input("value_limit", value=10)

#実行する世代数を設定
generations = st.number_input("generations", value=10)

#物体の重さ, 価値のリストを宣言しておく
W, V = [], []

def initial_con(lim_w, lim_v, nums):
    w_li, v_li = [], []
    for i in range(nums):
        w_li.append(random.randint(1, lim_w))
        v_li.append(random.randint(1, lim_v))
    
    return w_li, v_li


#なんでW, Vのリストが更新されないの...???(ChatGPTに聞こう)

#重さと価値のリストを乱数によって生成する
if st.button("Initial_value_update"):
    if limit > 0 and numbers > 0 and w_limit > 0 and v_limit > 0:
        W, V = initial_con(w_limit, v_limit, numbers)
    else:
        st.write("Input Error were occured!")

#作成したリストを表示(ナップザックの物体を表示)
if st.button("Initial_value_Validation!"):
    if limit > 0 and numbers > 0 and w_limit > 0 and v_limit > 0:

        #pd.DataFrameを作成して物体一覧を表示する
        sub_li = [[W[i], V[i]] for i in range(numbers)]
        sub_ary = np.array(sub_li)
        sub_col = ["weight", "value"]
        sub_idx = np.arange(1, numbers+1)
        sub_df = pd.DataFrame(data=sub_ary, index=sub_idx, columns=sub_col)
        #上記で作成したDataFrameを表示
        st.subheader("object_list")
        st.write(sub_df)

    else:
        st.write("Input Error were occured!")

if st.button("Weight, Value List Validation!"):
    #デバッグ用
    st.write(W)
    st.write(V)

if st.button("Run the Simple GA!"):
    #W, V, limit, genrationsは事前に作成されている
    bits = []

    cells = []
    Max_evals = []
    Avg_evals = []

    eval_li = []
    total_eval = 0

    solve() #単純GAの実行

    st.write("# Simple GA implemented!")