import matplotlib.pyplot as plt

maxStep = 2000

# parameters of epsilon-greedy
eps = 0.1

# parameters of UCB
c = 2

for stg in ['1', '2']:
    if stg == '1':
        filepath = '../log/eps{}.txt'.format(eps)
    else:
        filepath = '../log/UCB{}.txt'.format(c)
    flog = open(filepath, 'r')
    
    rewards = []
    
    for step, line in enumerate(flog.readlines()):
        # calculate average reward as global average
        reward = float(line.strip().split(' ')[1])
        if step == 0:
            rewards.append(reward)
        else:
            rewards.append(rewards[-1] + (reward - rewards[-1])/(step+1))

        if step == maxStep:
            break

    steps = list(range(1, len(rewards) + 1))
    if stg == '1':
        plt.plot(steps, rewards, label="ε-greedy: ε={}".format(eps))
    else:
        plt.plot(steps, rewards, label="UCB: c={}".format(c))
plt.xlabel('Steps')
plt.ylabel('AverageReward')
plt.legend(loc='lower right')
#plt.show()
plt.savefig('../log/log_averageReward.png')
