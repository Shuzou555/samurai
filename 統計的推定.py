# -*- coding: utf-8 -*-
"""統計的推定.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YOy-BPCK1jOr4GAamLaBi03Or-Dixrw9

SciPy のcomb関数を用いて組み合わせ数を計算可能
"""

from scipy.special import comb
print(comb(6,2))

"""# Pythonによる母平均の点推定"""

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

"""データの読み込み"""

health=pd.read_excel("health.xlsx")
health.head()

# 母平均の点推定
mu=np.mean(health["年齢"])
mu

"""# Pythonによる母平均の区間推定

自由度(n-1)の算出
"""

# 自由度
df=len(health)-1
df

"""不偏標準偏差 と 標準誤差 の算出"""

# 不偏標準偏差
sigma=np.std(health["年齢"],ddof=1)
# 標準誤差
se=sigma/np.sqrt(len(health["年齢"]))
se

"""95%信頼区間の算出"""

# 区間推定
interval=stats.t.interval(alpha=0.95,df=df,loc=mu,scale=se)
interval

"""# Pythonによる母分散の点推定"""

sigma_2=np.var(health["年齢"],ddof=1)
sigma_2

"""# Pythonによる母分散の区間推定"""

# 母分散の点推定

# カイ二乗分布を求めるには scipy の stats.chi2.interval を使用
# alpha：95%信頼係数
# df：自由度
chi2_025,chi2_975=stats.chi2.interval(alpha=0.95,df=df)
interal=[df*sigma_2/round(chi2_975,2),df*sigma_2/round(chi2_025,2)]
interal

"""# Pythonによる母比率の点推定"""

men=(health["性別"]==1).sum()
women=(health["性別"]==2).sum()
ratio=women/(men+women)
ratio

"""# Pythonによる母比率の区間推定"""

z=stats.norm.ppf(q=0.975)
lower_bound=ratio-z*np.sqrt(ratio*(1-ratio)/len(health["性別"]))
upper_bound=ratio+z*np.sqrt(ratio*(1-ratio)/len(health["性別"]))
interval=[lower_bound,upper_bound]
interval

"""健康調査データの「年齢」の95%信頼区間"""

mu=np.mean(health["年齢"])
df=len(health["年齢"])-1
sigma=np.std(health["年齢"],ddof=1)
se=sigma/np.sqrt(len(health["年齢"]))
interval=stats.t.interval(alpha=0.95,df=df,loc=mu,scale=se)
print(interval)

# 標本における分散が大きい場合
# 「データが平均値から離れている→平均値をあまり信頼できない」ことに なるため、信頼区間の幅は広くなる
# 不偏標準偏差を10倍に増やしてから95%信頼区間を計算
se2=(sigma*10)/np.sqrt(len(health["年齢"]))
interval2=stats.t.interval(alpha=0.95,df=df,loc=mu,scale=se2)
print(interval2)

"""サンプル数が大きい場合"""

# サンプルサイズが大きくなれば、標本平均を信頼できるようになるため、 信頼区間は狭くなる
# サンプルサイズを10倍に増やしてから95%信頼区間を計算
# ▪ サンプルサイズが大きくなると、自由度が大きくなり、標準誤差が小さくなる

df2=(len(health["年齢"])*10)-1
se3=sigma/np.sqrt(len(health["年齢"])*10)
stats.t.interval(alpha=0.95,df=df2,loc=mu,scale=se3)

"""信頼係数が大きい場合"""

# 99%信頼区間
stats.t.interval(alpha=0.99,df=df,loc=mu,scale=se)

"""# Pythonによる信頼区間の解釈"""

# 信頼区間が母平均(4)を含んでいればTrue

# 試行回数は20000回のため配列の要素数20000
# TrueかFalseしかとらないので『dtype = "bool"』
be_included_array=np.zeros(20000,dtype="bool")
be_included_array

#  「データを10個選んで95%信頼区間を求める」試行を20000回繰り 返す(信頼区間が母平均(4)を含んでいればTrue)
np.random.seed(1)
norm_dist=stats.norm(loc=4,scale=0.8)
for i in range(0,20000):
  sample=norm_dist.rvs(size=10)
  df=len(sample)-1
  mu=np.mean(sample)
  std=np.std(sample,ddof=1)
  se=std/np.sqrt(len(sample))
  interval=stats.t.interval(0.95,df,mu,se)
  if(interval[0]<=4 and interval[1]>=4):
    be_included_array[i]=True

sum(be_included_array)/len(be_included_array)