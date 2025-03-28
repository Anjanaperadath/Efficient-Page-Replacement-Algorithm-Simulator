import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function for FIFO Page Replacement Algorithm
def fifo_page_replacement(pages, frames):
    frame_list = []
    page_faults = 0
    page_fault_steps = []

    for page in pages:
        if page not in frame_list:
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                frame_list.pop(0)
                frame_list.append(page)
            page_faults += 1
        page_fault_steps.append(frame_list.copy())

    return page_faults, page_fault_steps

# Function for LRU Page Replacement Algorithm
def lru_page_replacement(pages, frames):
    frame_list = []
    page_faults = 0
    page_fault_steps = []
    recent_usage = {}

    for i, page in enumerate(pages):
        if page not in frame_list:
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                lru_page = min(recent_usage, key=recent_usage.get)
                frame_list.remove(lru_page)
                frame_list.append(page)
            page_faults += 1
        recent_usage[page] = i
        page_fault_steps.append(frame_list.copy())

    return page_faults, page_fault_steps

# Function for Optimal Page Replacement Algorithm
def optimal_page_replacement(pages, frames):
    frame_list = []
    page_faults = 0
    page_fault_steps = []

    for i, page in enumerate(pages):
        if page not in frame_list:
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                future_uses = {p: (pages[i+1:].index(p) if p in pages[i+1:] else float('inf')) for p in frame_list}
                page_to_remove = max(future_uses, key=future_uses.get)
                frame_list.remove(page_to_remove)
                frame_list.append(page)
            page_faults += 1
        page_fault_steps.append(frame_list.copy())

    return page_faults, page_fault_steps

# Streamlit UI
st.title("📊 Efficient Page Replacement Algorithm Simulator")

st.sidebar.header("🛠 Settings")
num_frames = st.sidebar.number_input("Number of Frames", min_value=1, max_value=10, value=3, step=1)
ref_string = st.sidebar.text_input("Enter Reference String (comma-separated)", "7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2")

if st.sidebar.button("Run Simulation"):
    pages = list(map(int, ref_string.split(',')))
    
    # Run Algorithms
    fifo_faults, _ = fifo_page_replacement(pages, num_frames)
    lru_faults, _ = lru_page_replacement(pages, num_frames)
    optimal_faults, _ = optimal_page_replacement(pages, num_frames)

    # Display Results
    st.subheader("📌 Page Replacement Results")
    st.write(f"**FIFO Page Faults:** {fifo_faults}")
    st.write(f"**LRU Page Faults:** {lru_faults}")
    st.write(f"**Optimal Page Faults:** {optimal_faults}")

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(["FIFO", "LRU", "Optimal"], [fifo_faults, lru_faults, optimal_faults], color=['blue', 'green', 'red'])
    ax.set_ylabel("Number of Page Faults")
    ax.set_title("Comparison of FIFO, LRU, and Optimal Page Replacement")

    st.pyplot(fig)

st.markdown("👨‍💻 **Built with Python, Streamlit & Matplotlib**"
