import matplotlib.pyplot as plt

epss = [0.1, 'decay']

maxStep = 2000

test_with_greedy = False

for eps in epss:
    if test_with_greedy:
        filepath = '../log/test_eps{}.txt'.format(eps)
    else:
        filepath = '../log/eps{}.txt'.format(eps)
    flog = open(filepath, 'r')
    
    rewards = []
    
    for step, line in enumerate(flog.readlines()):
        ## calculate average reward as moving average
        #avgReward = float(line.strip().split(' ')[-1])
        #rewards.append(avgReward)

        # calculate average reward as global average
        reward = float(line.strip().split(' ')[1])
        if step == 0:
            rewards.append(reward)
        else:
            rewards.append(rewards[-1] + (reward - rewards[-1])/(step+1))

        if step == maxStep:
            break

    steps = list(range(1, len(rewards) + 1))
    plt.plot(steps, rewards, label="ε={}".format(eps))
plt.xlabel('Steps')
plt.ylabel('AverageReward')
plt.legend(loc='upper right')
#plt.show()
if test_with_greedy:
    plt.savefig('../log/test_log_eps_decay.png')
else:
    plt.savefig('../log/log_eps_decay.png')
