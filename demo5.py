import matplotlib.pyplot as plt
import numpy as np
import random
import copy
# plt.rcParams['savefig.dpi'] = 300#图片像素
plt.rcParams['figure.dpi'] = 100 #分辨率

# 在demo4的基础上，加上曲线图


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

def rand_row(P_list, n):
    rows = len(P_list)
    if rows >= n:
        random.shuffle(P_list)
        choice_rows = P_list[:n]
        return choice_rows
    else:
        n = rows
        random.shuffle(P_list)
        choice_rows = P_list[:n]
        return choice_rows

def remove(a,b):
    for i in b:
        a.remove(i)
    return a

def init_P():
    N = 1000
    P = {'S':[],
         'E':[],
         'I':[],
         'R':[]}
    points = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 1000).tolist()

    S0 = rand_row(points,int(s[0]*N))
    remove(points,S0)
    P['S'] = S0
    E0 = rand_row(points,int(e[0]*N))
    remove(points,E0)
    P['E'] = E0
    I0 = rand_row(points,int(i[0]*N))
    remove(points,I0)
    P['I'] = I0
    R0 = points
    P['R'] = R0

    return P

def total_P():
    P_list = []
    P = init_P()
    P_list.append(copy.deepcopy(P))
    N = 1000
    frames = 150
    for frame in range(frames - 1):
        #     s[t + 1] = s[t] - lam * s[t] * i[t]
        #     e[t + 1] = e[t] + lam * s[t] * i[t] - sigma * e[t]
        #     i[t + 1] = i[t] + sigma * e[t] - gamma * i[t]
        #     r[t + 1] = r[t] + gamma * i[t]

        # lam_s_i = abs(s[frame + 1] - s[frame])
        # e_delta = abs(e[frame + 1] - e[frame])
        # sigma_e = lam_s_i - e_delta
        # i_delta = abs(i[frame + 1] - i[frame])
        # gamma_i = abs(sigma_e - i_delta)

        lam_s_i = abs(s[frame + 1] - s[frame])
        sigma_e = abs(e[frame + 1] - e[frame] - lam_s_i)
        gamma_i = abs(r[frame + 1] - r[frame])

        S_delta = rand_row(P['S'], int(lam_s_i * N))
        remove(P['S'], S_delta)

        P['E'].extend(S_delta)
        SIGMA_E = rand_row(P['E'], int(sigma_e * N))
        remove(P['E'], SIGMA_E)

        P['I'].extend(SIGMA_E)
        GAMMA_I = rand_row(P['I'], int(gamma_i * N))
        remove(P['I'], GAMMA_I)

        P['R'].extend(GAMMA_I)

        P_list.append(copy.deepcopy(P))  ###列表append字典覆盖问题https://blog.csdn.net/Sheldomcooper/article/details/82258006

    return P_list


if __name__ == "__main__":

    s, e, i, r = SEIR()

    fig, ax = plt.subplots(1,2,figsize=(10,5),facecolor='lightgrey')

    t = np.arange(150)
    P_list = total_P()
    frames = 150
    plt.ion()
    for frame in range(frames):
        P = P_list[frame]

        ax[0].set_xlim(-5,5)
        ax[0].set_ylim(-5,5)

        ax[1].set_xlim(0,150)
        ax[1].set_ylim(-0.05,1.05)
        ax[1].set_xlabel('day')
        ax[1].set_ylabel('ratio')

        if P['S'] != []:
            ax[0].scatter(np.array(P['S'])[:, 0], np.array(P['S'])[:, 1], c='b', s=5)

        if P['E'] != []:
            ax[0].scatter(np.array(P['E'])[:, 0], np.array(P['E'])[:, 1], c='y', s=5)

        if P['I'] != []:
            ax[0].scatter(np.array(P['I'])[:, 0], np.array(P['I'])[:, 1], c='r', s=5)

        if P['R'] != []:
            ax[0].scatter(np.array(P['R'])[:, 0], np.array(P['R'])[:, 1], c='g', s=5)


        ax[1].plot(t[:frame+1], s[:frame+1], c='b')
        ax[1].plot(t[:frame+1], e[:frame+1], c='y')
        ax[1].plot(t[:frame+1], i[:frame+1], c='r')
        ax[1].plot(t[:frame+1], r[:frame+1], c='g')


        plt.pause(0.01)


    plt.show()