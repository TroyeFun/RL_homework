import matplotlib.pyplot as plt

maxStep = 2000
best_action = 14

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
    
    best_action_rates = []
    best_action_cnt = 0
    
    for step, line in enumerate(flog.readlines()):
        # calculate average reward as global average
        action = int(line.strip().split(' ')[0])
        if action == best_action:
            best_action_cnt += 1
        best_action_rates.append(best_action_cnt/(step+1))

        if step == maxStep:
            break

    steps = list(range(1, len(best_action_rates) + 1))
    if stg == '1':
        plt.plot(steps, best_action_rates, label="ε-greedy: ε={}".format(eps))
    else:
        plt.plot(steps, best_action_rates, label="UCB: c={}".format(c))
plt.xlabel('Steps')
plt.ylabel('BestActionRate')
plt.legend(loc='lower right')
#plt.show()
plt.savefig('../log/log_bestActionRate.png')
