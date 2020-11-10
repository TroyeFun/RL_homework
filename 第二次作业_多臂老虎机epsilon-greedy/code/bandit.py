import random
import os

if not os.path.exists('../log/'):
    os.makedirs('../log/')

epss = [0, 0.01, 0.1, 0.2]

for epsilon in epss:

    K = 15
    mu = [k for k in range(1, K + 1)]
    Q = [0.0 for _ in range(K)]
    N = [0 for _ in range(K)]

    queueSize = 50
    rewardQueue = []
    testRewardQueue = []

    fout = open('../log/eps{}.txt'.format(epsilon), 'w')
    fout_test = open('../log/test_eps{}.txt'.format(epsilon), 'w')

    maxStep = 10000
    for step in range(maxStep):
        p = random.random()
        if p >= epsilon:
            a = Q.index(max(Q))
        else:
            a = random.randint(0, K-1)
        a_test = Q.index(max(Q))

        r = random.gauss(mu[a], 1)
        r_test = random.gauss(mu[a_test], 1)

        N[a] += 1
        Q[a] += (r-Q[a])/N[a]

        if len(rewardQueue) < queueSize:
            rewardQueue.append(r)
            testRewardQueue.append(r)
        else:
            rewardQueue = rewardQueue[1:] + [r]
            testRewardQueue = testRewardQueue[1:] + [r_test]

        print(a, r, sum(rewardQueue)/len(rewardQueue), file=fout)
        print(a_test, r_test, sum(testRewardQueue)/len(testRewardQueue), file=fout_test)



