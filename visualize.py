import matplotlib.pyplot as plt
def visualize_alpha():
    alphas = [0.01*(2**i) for i in range(1, 16)]
    rounds = [i for i in range(1, 16)]
    total_elections = 70720
    ties = [i/total_elections for i in [9724, 9694, 9567, 9180, 8201, 7226, 5992, 5242, 4878, 4670, 4631, 4615, 4614, 4614, 4614]]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))
    fig.suptitle("α Limits and Percentage Ties\nα = 0.01 * (2^n)")
    ax1.set_xticks(rounds, alphas)
    ax1.set_xlabel("Maximum α Value")
    ax1.set_ylabel("Tie Ratio")
    ax1.plot(rounds, ties, color="orange", linewidth=4)
    ax2.set_xticks(rounds)
    ax2.set_xlabel("Maximum Round")
    ax2.set_ylabel("Tie Ratio")
    ax2.plot(rounds, ties, color="blue", linewidth=4)
    plt.savefig('alpha.png')
    plt.show()
visualize_alpha()