######################
# Import libraries
######################

import pandas as pd
import streamlit as st

#altairライブラリ: データ可視化のためのライブラリ
#matplotlibでも基本的には代用可能と思われる
import altair as alt

from PIL import Image

######################
# Page Title
######################

#相対パスは".\..."の形であるので注意
#これは慣れよう
image = Image.open('.\\class\\streamlit\\dna-logo.jpg')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")


######################
# Input Text Box
######################

#st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skips the sequence name (first line)
sequence = ''.join(sequence) # Concatenates list to string


#区切りの線を表示する(-------, こんなやつ)
#sequenceのボックスの下側に引いてある
st.write("""
***
""")

## Prints the input DNA sequence
st.header('INPUT (DNA Query)')

#これによってsequenceの内容を表示している
#ただ入力を更新すると反映されないときがある(なぜ?)
sequence

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
  d = dict([
            ('A',seq.count('A')),
            ('T',seq.count('T')),
            ('G',seq.count('G')),
            ('C',seq.count('C'))
            ])
  return d

X = DNA_nucleotide_count(sequence)

#こちらも同様にこれでXに格納された内容を表示する
#Google Colabで1+1と打てば2と出るようなもの, print()を使う必要がない
X

### 2. Print text
st.subheader('2. Print text')

#基本的にstreamlitで文字を表示したいときはwrite()を使う
st.write('There are  ' + str(X['A']) + ' adenine (A)')
st.write('There are  ' + str(X['T']) + ' thymine (T)')
st.write('There are  ' + str(X['G']) + ' guanine (G)')
st.write('There are  ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame

#サブのヘッダーを表示(マジでそのまま)
st.subheader('3. Display DataFrame')

#Xは辞書型(dictionary)で.from_dictにより辞書型からDataFrameを作成できる
df = pd.DataFrame.from_dict(X, orient='index')
#st.write(df)

#ラベル名の変更
df = df.rename({0: 'count'}, axis='columns')
#st.write(df)

#辞書のラベル(A, B, C, D)を表に入れたいのでインデックスをリセットすることにより
#A, B, C, Dのラベルを入れる(インデックスは0, 1, 2, 3となる)
df.reset_index(inplace=True)
st.write(df)

#indexと名がついたcolumnsをnucletideに名前を変更する
df = df.rename(columns = {'index':'nucleotide'})
#st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)

#widthは横の長さを変更できる(altairライブラリ)
p = p.properties(
    width=alt.Step(100)  # controls width of bar.
)
st.write(p)
