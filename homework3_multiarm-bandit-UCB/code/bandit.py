import random
import os
from math import log, sqrt

stg = input('choose a exploration strategy from:\n1. epsilon-greedy\n2. UCB\n')
assert stg in ['1', '2'], "input '1' or '2'"

if not os.path.exists('../log/'):
    os.makedirs('../log/')

# parameters of epsilon-greedy
eps = 0.1

# parameters of UCB
c = 2

# settings of bandit
K = 15
mu = [k for k in range(1, K + 1)]

Q = [0.0 for _ in range(K)]
N = [0 for _ in range(K)]
t = 0

if stg == '1':
    fout = open('../log/eps{}.txt'.format(eps), 'w')
else:
    fout = open('../log/UCB{}.txt'.format(c), 'w')

maxStep = 10000
for step in range(maxStep):
    # epsilon greedy
    if stg == '1':
        p = random.random()
        if p >= eps:
            a = Q.index(max(Q))
        else:
            a = random.randint(0, K-1)
    # UCB
    else:
        max_upper_bound = 0
        a = -1
        for choice in range(K):
            if N[choice] == 0:
                a = choice
                break
            else:
                upper_bound = Q[choice] + c * sqrt(log(t)/N[choice])
                if upper_bound > max_upper_bound:
                    max_upper_bound = upper_bound
                    a = choice

    r = random.gauss(mu[a], 1)

    N[a] += 1
    t += 1
    Q[a] += (r-Q[a])/N[a]

    print(a, r, file=fout)
