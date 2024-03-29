import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores, plot_title, save = False):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title(plot_title)
    plt.xlabel('Number of Episodes')
    plt.ylabel('Average Score')
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)
    if save :
        plot_file_name = plot_title
        plot_file_name.replace(" ", "-")
        plt.savefig("results/Train-"+plot_file_name+".png") 

def plot_test_results(accuracey_scores, plot_title, save = False):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title(plot_title)
    plt.xlabel('Number of Packages')
    plt.ylabel('Accuracy Score')
    plt.plot(accuracey_scores)
    plt.ylim(ymin=0)
    plt.text(len(accuracey_scores)-1, accuracey_scores[-1], str(accuracey_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)
    if save :
        plt.savefig("results/Test-"+plot_title+".png") 