import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import copy


# 动态曲线实验带子图


def SEIR():
    N = 985 + 10 + 5  #假设所在区域总人数
    T = 150 #传染时长，单位为天

    s = np.zeros([T]) #每一天易感人群占总人数比例
    e = np.zeros([T]) #每一天潜伏人数占总人数比例
    i = np.zeros([T]) #每一天感染发病占总人数比例
    r = np.zeros([T]) #每一天治愈移除占总人数比例

    lam = 0.5 #易感人群到潜伏的概率
    sigma = 1 / 14  # 潜伏到发病概率
    gamma = 0.0821 #发病到治愈的概率

    s[0] = 985 / N
    e[0] = 10 / N
    i[0] = 5 / N
    for t in range(T - 1):
        s[t + 1] = s[t] - lam * s[t] * i[t]
        e[t + 1] = e[t] + lam * s[t] * i[t] - sigma * e[t]
        i[t + 1] = i[t] + sigma * e[t] - gamma * i[t]
        r[t + 1] = r[t] + gamma * i[t]
    return s,e,i,r
s,e,i,r = SEIR()

fig,ax = plt.subplots(1,2,figsize=(10,5),facecolor='lightgrey')

t = np.arange(150)
def animate(frame):
    ax[1].plot(t[:frame+1], s[:frame+1], c='b')
    ax[1].plot(t[:frame+1], e[:frame+1], c='y')
    ax[1].plot(t[:frame+1], i[:frame+1], c='r')
    ax[1].plot(t[:frame+1], r[:frame+1], c='g')

def init():
    ax[1].set_xlim(0,150)
    ax[1].set_ylim(-0.05,1.05)
    ax[1].set_xlabel('day')
    ax[1].set_ylabel('ratio')


ani = animation.FuncAnimation(fig, animate, init_func=init,frames=150,interval=10)

plt.show()