from argparse import ArgumentParser
from greengraph import Greengraph, Map
from matplotlib import pyplot as plt
import csv

def process():
    parser = ArgumentParser(description = "Generates a graph of the porportion of green pixels between two locations")
    #use "New York" (etc) for a longer name
    parser.add_argument('--start', help="Start Location")
    parser.add_argument('--end', help="End Location")
    parser.add_argument('--steps', help="Steps inbetween")
    parser.add_argument('--imageout', help="File name for output figure (PNG)")
    parser.add_argument('--dataout', help="File name for data output (list of numbers of green pixels) (CSV)")

    arguments= parser.parse_args()

    if arguments.start and arguments.end and arguments.steps:
        mygraph = Greengraph(arguments.start, arguments.end)
        data = mygraph.green_between(arguments.steps)
    else:
        print("Need start, end, and steps inputs")
        exit()

    if arguments.imageout:
        plt.title("Number of green pixels between " + arguments.start +" and " + arguments.end)
        plt.ylabel('Number of green pixels')
        plt.xlabel('Steps in-between')
        plt.plot(data)
        plt.savefig(arguments.imageout)

    if arguments.dataout:
        with open(arguments.dataout, "w") as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            for num in data:
                writer.writerow([num])



if __name__ == "__main__":
    process()