from argparse import ArgumentParser
from .greengraph import Greengraph, Map

def process():
    parser = ArgumentParser(description = "Generates a graph of the porportion of green pixels between two locations")
 
    parser.add_argument('start')
    parser.add_argument('end')
    parser.add_argument('steps')

    arguments= parser.parse_args()

    mygraph = Greengraph(arguments.start,arguments.end)
	data = mygraph.green_between(arguments.steps)
	plt.plot(data)
   
if __name__ == "__main__":
    process()