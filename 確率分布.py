# -*- coding: utf-8 -*-
"""確率分布.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SudJxsGMX3vANaPlDJN-fsgV_CZ8bPf4

Pythonによる確率分布シミュレーション
"""

# Commented out IPython magic to ensure Python compatibility.
# 数値計算に使うライブラリ
import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats

# グラフを描画するライブラリ
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

# 表示桁数の指定
# %precision 3
# グラフをjupyter Notebook内に表示させるための指定
# %matplotlib inline

"""100,000個のカプセルが入っているガチャガチャの全数調査のデータ

 ▪ 母集団をすべて観測できたという(通常はあり得ない)理想的な状況
"""

gacha_100000=pd.read_csv("gachagacha.csv")
gacha_100000.head()

"""ガチャガチャの全数調査のデータから5個のデータをランダムに抽出"""

# sampleメソッド：pandasの行・列をランダムサンプリング（抽出）する
# 引数nで抽出する行数・列数を指定できる。
# 引数replace：重複を許可する（Falseで重複を許可しない）
gacha_sample=gacha_100000.sample(n=5,replace=False)
gacha_sample

"""標本平均は以下の通り"""

# meanメソッドで平均を出す
gacha_sample["value(\)"].mean()

"""母集団の平均"""

gacha_100000["value(\)"].mean()

"""母集団の標準偏差"""

gacha_100000["value(\)"].std()

"""母集団の分散"""

gacha_100000["value(\)"].var()

"""母集団のヒストグラムは以下の通り

カプセルの価値の平均(250円相当)を中心として左右対称な度数分布
"""

# distplotメソッド：ヒストグラムを作る
# kde引数：カーネル密度推定の線を表示させる（Falseで非表示にする）
sns.distplot(gacha_100000["value(\)"],kde=False,color="black")

# 補足：山形のようになれば正規分布と予想できる

"""ガチャガチャの母集団(100,000個のカプセル)の確率分布は「**平均250**、**分散2500**の正規分布」として表現できると予想

▪  母集団のヒストグラムと正規分布の確率密度を比較

▪ 「平均250、分散2500の正規分布」の確率密度を可視化
（２５０回調べれば、全数把握と同じ、分散２５００（５０の２乗）で誤差５０を表す）

 ▪ 100~400までを0.1区切りで分けた等差数列を用意
"""

# arangeメソッド：numpyで間隔（公差）を指定し、引数の個数によって以下のように等差数列を配列ndarrayとして生成する。
# start引数：配列の開始数
# stop引数：配列の終了数
# step引数：配列の間隔を指定
x=np.arange(start=100,stop=400.1,step=0.1)
x

# stats.norm.pdf関数：確率密度を表示
# loc引数：平均値
# scale引数：標準偏差
stats.norm.pdf(x=x,loc=250,scale=50)

# 出力における『e-05』などは、10のマイナス5乗であることを意味

"""正規分布の確率密度を図示"""

plt.plot(x,
         stats.norm.pdf(x=x, loc=250, scale=50),
         color='black')

"""正規分布の確率密度と、母集団のヒストグラムのグラフを重ねて表示"""

# sns.distplotにおいて『norm_hist = True』と指定することで、面積 が1であるヒストグラムとなる
sns.distplot(gacha_100000["value(\)"],kde=False,norm_hist=True,color="black")
plt.plot(x,stats.norm.pdf(x=x,loc=250,scale=50),color="black")

"""▪ 正規分布の確率密度と、母集団のヒストグラムが極めてよく一致する

▪ 母集団分布は「平均250、分散2500の正規分布」とみなせる
"""

# stats.norm.rvs関数:正規分布に従う乱数を発生させる
# loc引数：平均値
# scale引数：標準偏差
# size引数：取得するサンプル数
sampling_norm=stats.norm.rvs(loc=250,scale=50,size=10)
sampling_norm

"""Pythonによる大数の法則のシミュレーション

母集団の平均は以下の通り
"""

gacha_100000["value(\)"].mean()

"""サンプル数に応じた標本平均は以下の通り"""

# 10回の平均
gacha_sample_10=gacha_100000.sample(n=10,replace=False)
gacha_sample_10["value(\)"].mean()

# 10０回の平均
gacha_sample_100=gacha_100000.sample(n=100,replace=False)
gacha_sample_100["value(\)"].mean()

# 10００回の平均
gacha_sample_1000=gacha_100000.sample(n=1000,replace=False)
gacha_sample_1000["value(\)"].mean()

# 10０００回の平均
gacha_sample_10000=gacha_100000.sample(n=10000,replace=False)
gacha_sample_10000["value(\)"].mean()

"""Pythonによる中心極限定理のシミュレーション"""

#サンプルサイズと試行回数
n_size=10000
n_trial=50000
# サイコロの目
dice=np.array([1,2,3,4,5,6])
# サイコロの目を記録する変数
# np.zeros関数:shapeとdtype（要素の型）を指定して、0で埋められた配列を返します。
count_dice=np.zeros(n_trial)
# サイコロをn_size回投げる試行をn_trai回行う
for i in range(0,n_trial):
  # np.random.choice関数：配列やリストから、ランダムに要素を取り出す関数
  count_dice[i]=np.sum(np.random.choice(dice,size=n_size,replace=True))
# ヒストグラムを描く
sns.distplot(count_dice,color='black')

"""Pythonによる不偏分散のシミュレーション

標本分散の場合
"""

sample_var_array=np.zeros(10000)

for i in range(0,10000):
  gacha_sample=gacha_100000.sample(n=10,replace=False)
  # np.var：NumPyで分散を求める関数
  # ddof引数：標本分散か不偏分散をする。ddof=0で標準分散
  sample_var_array[i]=np.var(gacha_sample["value(\)"],ddof=0)

# 母分散
print("母分散："+str(gacha_sample["value(\)"].var()))
# 標本分散
print("標本分散："+str(np.mean(sample_var_array)))

"""不偏分散の場合"""

sample_var_array=np.zeros(10000)

for i in range(0,10000):
  gacha_sample=gacha_100000.sample(n=10,replace=False)
  # ddof=1で不偏分散
  sample_var_array[i]=np.var(gacha_sample["value(\)"],ddof=1)

# 母分散
print("母分散："+str(gacha_100000["value(\)"].var()))
# 標本分散
print("標本分散："+str(np.mean(sample_var_array)))