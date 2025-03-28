import streamlit as st
import matplotlib.pyplot as plt

# FIFO Algorithm
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        memory_states.append(memory.copy())  # Ensure a proper copy is stored
    
    return page_faults, memory_states

# LRU Algorithm
def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                if memory:
                    lru_page = min(memory, key=lambda p: page_indices.get(p, -1))  # Fix KeyError possibility
                    memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i
        memory_states.append(memory.copy())
    
    return page_faults, memory_states

# Optimal Algorithm
def optimal(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_indices = []
                for mem_page in memory:
                    if mem_page in pages[i:]:
                        future_indices.append(pages[i:].index(mem_page))
                    else:
                        future_indices.append(float('inf'))
                
                replace_index = future_indices.index(max(future_indices))
                memory[replace_index] = page
            page_faults += 1
        memory_states.append(memory.copy())
    
    return page_faults, memory_states

# Function to run the selected algorithm
def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# Streamlit Interface
st.title("Page Replacement Algorithm Simulator")
st.write("Simulate FIFO, LRU, and Optimal Page Replacement Algorithms.")

# Initialize session state
if "pages_input" not in st.session_state:
    st.session_state.pages_input = ""
if "frames" not in st.session_state:
    st.session_state.frames = 3

# User Inputs
pages_input = st.text_input("Enter page reference string (comma-separated):", value=st.session_state.pages_input)
frames = st.number_input("Enter number of frames:", min_value=1, max_value=10, value=st.session_state.frames)

# Select Algorithm
algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    run_clicked = st.button("Run Simulation")
with col2:
    clear_clicked = st.button("Clear")

# Clear input
if clear_clicked:
    st.session_state.pages_input = ""
    st.session_state.frames = 3
    st.experimental_rerun()

# Run Simulation
if run_clicked:
    if pages_input:
        try:
            pages = list(map(int, pages_input.split(",")))
        except ValueError:
            st.error("Invalid input. Please enter a comma-separated list of integers.")
            st.stop()

        page_faults, memory_states = run_algorithm(algorithm, pages, frames)
        st.write(f"**Number of Page Faults:** {page_faults}")
        st.write("### Memory State Changes:")
        for i, state in enumerate(memory_states):
            st.write(f"Step {i+1}: {state}")

        # Bar Graph for Algorithm Comparison
        fig, ax = plt.subplots(figsize=(8, 6))
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults = [fifo(pages, frames)[0], lru(pages, frames)[0], optimal(pages, frames)[0]]
        colors = ["#4C72B0", "#55A868", "#C44E52"]
        ax.bar(algorithms, faults, color=colors, width=0.6, edgecolor="black")

        ax.set_ylabel("Page Faults", fontsize=12, fontweight="bold")
        ax.set_xlabel("Algorithm", fontsize=12, fontweight="bold")
        ax.set_title("Comparison of Page Faults", fontsize=14, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)

        # Finding best and worst algorithms
        min_faults = min(faults)
        max_faults = max(faults)
        best_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == min_faults]
        worst_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == max_faults]

        # Display Insights
        st.write("### Insights from the Simulation")
        st.write(f"**Best Algorithm(s):** {', '.join(best_algorithms)} with the least page faults.")
        st.write(f"**Worst Algorithm(s):** {', '.join(worst_algorithms)} with the highest page faults.")

        if min_faults == faults[0]:
            st.write("**FIFO works well** when the page reference order is predictable but can suffer from Belady's anomaly.")
        if min_faults == faults[1]:
            st.write("**LRU is efficient** when recent pages are likely to be used again soon.")
        if min_faults == faults[2]:
            st.write("**Optimal is the best** but impractical as it requires future knowledge.")

        if max_faults == faults[0]:
            st.write("**FIFO's limitation:** It does not consider page usage frequency, leading to high faults.")
        if max_faults == faults[1]:
            st.write("**LRU's limitation:** High overhead due to maintaining page usage history.")
        if max_faults == faults[2]:
            st.write("**Optimal's limitation:** It is theoretical and cannot be used in real-world applications.")



                
