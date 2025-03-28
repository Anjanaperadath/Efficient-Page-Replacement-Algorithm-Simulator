import matplotlib.pyplot as plt
from algorithms import PageReplacement

def compare_algorithms(reference_string, frame_size):
    sim = PageReplacement(frame_size, reference_string)

    results = {
        "FIFO": sim.fifo(),
        "LRU": sim.lru(),
        "Optimal": sim.optimal()
    }

    plt.bar(results.keys(), results.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Algorithm")
    plt.ylabel("Page Faults")
    plt.title("Page Replacement Algorithm Comparison")
    plt.show()

if _name_ == "_main_":
    reference_string = [7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2]
    frame_size = 3
    compare_algorithms(reference_string, frame_size)
