from argparse import ArgumentParser
from greengraph import Greengraph, Map
from matplotlib import pyplot as plt

def process():
    parser = ArgumentParser(description = "Generates a graph of the porportion of green pixels between two locations")
    #use "New York" (etc) for a longer name
    parser.add_argument('--start', help="Start Location")
    parser.add_argument('--end', help="End Location")
    parser.add_argument('--steps', help="Steps inbetween")
    parser.add_argument('--imageout', help="File name for output figure")


    arguments= parser.parse_args()

    mygraph = Greengraph(arguments.start, arguments.end)
    data = mygraph.green_between(arguments.steps)
    print(data)
    plt.title("Number of green pixels between " + arguments.start +" and " + arguments.end)
    plt.ylabel('Number of green pixels')
    plt.xlabel('Steps in-between')
    plt.plot(data)
    #plt.show()
    plt.savefig(arguments.imageout)
   
if __name__ == "__main__":
    process()