import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#/*******************/
#/* 単純GAの処理実装 */
#/*******************/

#8bitのbit列を10コ作成
def initial_values():
    bits = []
    for i in range(10): #個体数は一定でいいだろ()
        k = random.randint(0, 2**len(st.session_state.W)-1)
        k = bin(k)[2:].rjust(len(st.session_state.W), "0")
        bits.append(k)
    return bits

#適応度関数の評価の計算
def evalulate():
    total_eval = 0
    eval_li = []
    for bit in st.session_state.bits:
        rlt_v = 0
        rlt_w = 0
        for j in range(len(bit)):
            rlt_w += int(bit[j]) * st.session_state.W[j]
            rlt_v += int(bit[j]) * st.session_state.V[j]

        #評価値の決定
        if rlt_w <= st.session_state.limit: #1)
            rlt_v = rlt_v
        else: #2)
            rlt_v = 0
        
        #評価値を反映
        total_eval += rlt_v
        eval_li.append(rlt_v)

    st.session_state.cells.append(eval_li)
    st.session_state.Max_evals.append(max(eval_li))
    st.session_state.Avg_evals.append(total_eval / len(st.session_state.bits))

    st.session_state.eval_li = eval_li
    st.session_state.total_eval = total_eval

#選択を行う
def selection():
    acm = [0] + list(itertools.accumulate(st.session_state.eval_li))

    for i in range(len(st.session_state.bits)):
        x = random.randint(0, st.session_state.total_eval)
        for j in range(len(acm)-1):
            if acm[j] <= x < acm[j+1]:
                a = j+1 #j番目の個体を選択するということ
                break
        else:
            a = len(st.session_state.bits)

        st.session_state.bits[i] = st.session_state.bits[a-1]

#交叉を行う関数
def crossover():
    a, b = random.randint(0, len(st.session_state.bits)-1), random.randint(0, len(st.session_state.bits)-1)
    c = random.randint(1, len(st.session_state.bits[a])-2)

    temp_A = st.session_state.bits[a][c:]
    temp_B = st.session_state.bits[b][c:]
    st.session_state.bits[a] = st.session_state.bits[a][:c] + temp_B
    st.session_state.bits[b] = st.session_state.bits[b][:c] + temp_A

def mutation():
    chk = random.randint(0, 100)
    if chk > 5:
        return

    a = random.randint(0, len(st.session_state.bits)-1)
    c = random.randint(2, len(st.session_state.bits[a])-1)

    if st.session_state.bits[a][c] == "1":
        st.session_state.bits[a] = st.session_state.bits[a][:c-1] + "0" + st.session_state.bits[a][c:]
    else:
        st.session_state.bits[a] = st.session_state.bits[a][:c-1] + "1" + st.session_state.bits[a][c:]

#GAの処理を実行する関数
def solve():
    st.session_state.bits = initial_values()

    for _ in range(st.session_state.generations):
        evalulate()
        selection()
        crossover()
        mutation()

#/*******************/
#/* Streamlitの実装 */
#/*  UI, 入力部分   */
#/*******************/

#マークダウン記法での記述
st.write("""
# Simple GA Model

This model solves the Knapsack problem!
""")

st.subheader("Evaluation Function details")

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

# 重さの上限
st.session_state.limit = st.number_input("weight_total_limit", value=10)

# 物体の個数
st.session_state.numbers = st.number_input("numbers", value=5)

# 各物体の重さ, 価値の上限を設定
st.session_state.w_limit = st.number_input("weight_limit", value=10)
st.session_state.v_limit = st.number_input("value_limit", value=10)

# 実行する世代数を設定
st.session_state.generations = st.number_input("generations", value=10)

#乱数でリストを作成(W, Vの)
def initial_con():
    #空のW, Vリストを作成
    st.session_state.W = []
    st.session_state.V = []
    for i in range(st.session_state.numbers):
        st.session_state.W.append(random.randint(1, st.session_state.w_limit))
        st.session_state.V.append(random.randint(1, st.session_state.v_limit))

# 乱数で作成したリストを表示(ナップザックの物体を表示, 作成と表示同時に行う)
if st.button("Initial_value_Validation!"):
    if st.session_state.limit > 0 and st.session_state.numbers > 0 and st.session_state.w_limit > 0 and st.session_state.v_limit > 0:

        initial_con() #リスト作成

        sub_li = [[st.session_state.W[i], st.session_state.V[i]] for i in range(st.session_state.numbers)]
        sub_ary = np.array(sub_li)
        sub_col = ["weight", "value"]
        sub_idx = np.arange(1, st.session_state.numbers+1)
        sub_df = pd.DataFrame(data=sub_ary, index=sub_idx, columns=sub_col)
        st.subheader("object_list")
        st.write(sub_df)
    else:
        st.write("Input Error were occured!")

#if st.button("Weight, Value List Validation!"):
#    st.write(st.session_state.W)
#    st.write(st.session_state.V)

if st.button("Run the Simple GA!"):
    st.session_state.bits = []
    st.session_state.cells = []
    st.session_state.Max_evals = []
    st.session_state.Avg_evals = []
    st.session_state.eval_li = []
    st.session_state.total_eval = 0

    solve() #単純GAの実行

    st.write("# Simple GA implemented!")

if st.button("Max_Graph Plot"):
    st.session_state.generation_label = [(i+1) for i in range(st.session_state.generations)]

    #ボタンの中にボタンを入れると上手く動かない...

    plt.figure(figsize=(10, 5))
    plt.plot(st.session_state.generation_label, st.session_state.Max_evals, label='Max Evals')
    plt.xlabel("Generation")  # x軸にラベルが追加される
    plt.ylabel("Adaptive Values")  # y軸にラベルが追加される
    plt.title("Adaptive Values Over Generations")
    plt.legend()
    st.pyplot(plt)
    #ラベルを付ける癖は付けておいた方がよい

if st.button("Avg_Graph Plot"):
    st.session_state.generation_label = [(i+1) for i in range(st.session_state.generations)]

    #ボタンの中にボタンを入れると上手く動かない...

    plt.figure(figsize=(10, 5))
    plt.plot(st.session_state.generation_label, st.session_state.Avg_evals, label='Avg Evals')
    plt.xlabel("Generation")  # x軸にラベルが追加される
    plt.ylabel("Adaptive Values")  # y軸にラベルが追加される
    plt.title("Adaptive Values Over Generations")
    plt.legend()
    st.pyplot(plt)
    #ラベルを付ける癖は付けておいた方がよい