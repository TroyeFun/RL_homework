import numpy as np
import math
from datetime import datetime as dt
import os

np.set_printoptions(precision=1, linewidth=200)

def possion(n, lam):
    return lam**n / math.factorial(n) * math.exp(-lam)

lam_rent = [3, 4]
lam_return = [3, 2]
gamma = 0.9
errorThrd = 1

resume = -1  # -1 by default, or set to specific number to resume checkpoint of corresponding iter

def main():

    # pre-calculate possion prob
    prob_rent1 = np.zeros(21)
    prob_rent2 = np.zeros(21)
    prob_return1 = np.zeros(21)
    prob_return2 = np.zeros(21)

    prob_ge_rent1 = np.ones(21) # prob_ge[n] = prob[n] + prob[n+1] + prob[n+2] + ...
    prob_ge_rent2 = np.ones(21)
    prob_ge_return1  = np.ones(21)
    prob_ge_return2 = np.ones(21)

    for i in range(21):
        prob_rent1[i] = possion(i, lam_rent[0])
        prob_rent2[i] = possion(i, lam_rent[1])
        prob_return1[i] = possion(i, lam_return[0])
        prob_return2[i] = possion(i, lam_return[1])

        if i == 0:
            continue
        prob_ge_rent1[i] = prob_ge_rent1[i-1] - prob_rent1[i-1]
        prob_ge_rent2[i] = prob_ge_rent2[i-1] - prob_rent2[i-1]
        prob_ge_return1[i] = prob_ge_return1[i-1] - prob_return1[i-1]
        prob_ge_return2[i] = prob_ge_return2[i-1] - prob_return2[i-1]


    V = np.zeros((21, 21))
    pi = np.zeros((21, 21), dtype=np.int)
    iter_count = -1

    if resume >= 0:
        print('resume iter {}'.format(resume))
        assert os.path.exists('pi-{}.npy'.format(resume)) and os.path.exists('pi-{}.npy'.format(resume)), \
            'file pi-{} or V-{} not exists.'.format(resume, resume)
        pi = np.load('log/pi-{}.npy'.format(resume))
        V = np.load('log/V-{}.npy'.format(resume))
        iter_count = resume

    def Q(s, a):
        i, j = s
        value = 0

        newi = i - a
        newj = j + a
        
        for rent1 in range(newi + 1):
            p1 = prob_rent1[rent1] if rent1 < newi else prob_ge_rent1[rent1]
            car_left1 = newi - rent1
            max_return1 = 20 - car_left1
            for rent2 in range(newj + 1):
                p2 = prob_rent2[rent2] if rent2 < newj else prob_ge_rent2[rent2]
                car_left2 = newj - rent2
                max_return2 = 20 - car_left2

                reward = -2 * abs(a) + 10 * (rent1 + rent2)

                for return1 in range(max_return1 + 1):
                    p3 = prob_return1[return1] if return1 < max_return1 else prob_ge_return1[return1]
                    for return2 in range(max_return2 + 1):
                        p4 = prob_return2[return2] if return2 < max_return2 else prob_ge_return2[return2]


                        nexti = car_left1 + return1
                        nextj = car_left2 + return2

                        p = p1*p2*p3*p4
                        value += p * (reward + gamma * V[nexti, nextj])
        return value

    while True:
        iter_count += 1

        # V = np.zeros((21, 21))  # reset V, or it will diverge (I don't know why)

        # evaluation
        eval_iter = 0
        while True:
            error = 0
            for i in range(21):
                for j in range(21):
                    # at state (i, j)
                    a = pi[i, j]
                    new_value = Q((i, j), a)
                    error = max([error, abs(V[i, j] - new_value)])
                    V[i, j] = new_value
            print('Debug {}: iteration {}-{}: error {}'.format(dt.now().strftime('%c'), iter_count, eval_iter, error))

            if eval_iter % 10 == 0:
                print(V)
            eval_iter += 1
            if error < errorThrd:
                break
        print('evaluation', iter_count, 'done.')
        print(V)

        # improvement
        stable = True
        for i in range(21):
            for j in range(21):
                max_v = -1e10
                for a in range(-5, 6):
                    if a > i or -a > j or a > (20 - j) or -a > (20 - i):
                        continue
                    value = Q((i, j), a)
                    if value > max_v:
                        max_v = value
                        best_a = a
                if not pi[i, j] == best_a:
                    stable = False
                    pi[i, j] = best_a
        print('improvement', iter_count, 'done.')
        print(pi)

        if not os.path.exists('log'):
            os.makedirs('log')

        np.save('log/pi-{}.npy'.format(iter_count), pi)
        np.save('log/V-{}.npy'.format(iter_count), V)

        if stable:
            break

    print(V)
    print(pi)


if __name__ == '__main__':
    main()


                    
