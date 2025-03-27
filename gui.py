import tkinter as tk
from tkinter import messagebox
from algorithms import PageReplacement

def run_simulation():
    ref_string = entry_ref.get().split()
    ref_string = list(map(int, ref_string))  # Convert to integers
    frame_size = int(entry_frames.get())
    algo = algo_var.get()

    sim = PageReplacement(frame_size, ref_string)

    if algo == "FIFO":
        result = sim.fifo()
    elif algo == "LRU":
        result = sim.lru()
    elif algo == "Optimal":
        result = sim.optimal()
    else:
        messagebox.showerror("Error", "Invalid Algorithm")
        return

    messagebox.showinfo("Result", f"Page Faults using {algo}: {result}")

# GUI Setup
root = tk.Tk()
root.title("Page Replacement Simulator")

tk.Label(root, text="Reference String:").grid(row=0, column=0)
entry_ref = tk.Entry(root)
entry_ref.grid(row=0, column=1)

tk.Label(root, text="Frame Size:").grid(row=1, column=0)
entry_frames = tk.Entry(root)
entry_frames.grid(row=1, column=1)

tk.Label(root, text="Algorithm:").grid(row=2, column=0)
algo_var = tk.StringVar(value="FIFO")
tk.OptionMenu(root, algo_var, "FIFO", "LRU", "Optimal").grid(row=2, column=1)

tk.Button(root, text="Run", command=run_simulation).grid(row=3, column=0, columnspan=2)

root.mainloop()