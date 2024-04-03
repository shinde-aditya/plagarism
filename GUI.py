import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Function to add a single file for comparison
def add_file():
    file = filedialog.askopenfilename(title="Select a file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file:
        selected_file_entry.delete(0, tk.END)
        selected_file_entry.insert(0, os.path.basename(file))
        update_file_list()

# Function to update the list of files for comparison
def update_file_list():
    file_list.delete(0, tk.END)
    files = filedialog.askopenfilenames(title="Select files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    for file in files:
        file_list.insert(tk.END, os.path.basename(file))

# Function to check plagiarism
def check_plagiarism():
    folder_path = os.getcwd()  # Store current directory path for file selection
    
    sample_file = selected_file_entry.get()
    if not sample_file:
        messagebox.showerror("Error", "Please select a file for comparison.")
        return

    sample_path = os.path.join(folder_path, sample_file)
    sample_content = open(sample_path).read()

    vectorizer = TfidfVectorizer()
    sample_vector = vectorizer.fit_transform([sample_content])

    results = []

    for index in range(file_list.size()):
        file = file_list.get(index)
        file_path = os.path.join(folder_path, file)
        file_content = open(file_path).read()

        file_vector = vectorizer.transform([file_content])
        similarity = cosine_similarity(sample_vector, file_vector)[0][0]
        similarity_percentage = round(similarity * 100, 2)

        results.append((sample_file, file, similarity_percentage))

    display_results(results)
    create_bar_graph(results)

# Function to display plagiarism results
def display_results(results):
    result_text.delete(1.0, tk.END)
    for data in results:
        result_text.insert(tk.END, f"Plagiarism detected between {data[0]} and {data[1]}: {data[2]}% similar\n")

# Function to create a bar graph
def create_bar_graph(results):
    files = [f"{data[1]}: {data[2]}%" for data in results]
    similarities = [data[2] for data in results]

    plt.figure(figsize=(10, 6))
    plt.barh(files, similarities, color='skyblue')
    plt.xlabel('Similarity (%)')
    plt.ylabel('Files')
    plt.title('Plagiarism Similarity')
    plt.tight_layout()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Plagiarism Checker")

# Set background color
root.configure(bg="#FFCCCC")

# Style for buttons
style = ttk.Style()
style.configure("TButton", background="#007BFF", foreground="black", padding=5)

frame = tk.Frame(root, bg="#FFCCCC")
frame.pack(padx=10, pady=10)

selected_file_label = tk.Label(frame, text="Selected File:", bg="#FFCCCC")
selected_file_label.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)

selected_file_entry = tk.Entry(frame, width=35, relief="solid", borderwidth=2, bg="#FFFFFF", fg="gray")
selected_file_entry.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)

add_file_button = ttk.Button(frame, text="Add File", command=add_file, style="TButton")
add_file_button.grid(row=0, column=2, padx=5, pady=3, sticky=tk.W)

file_list_label = tk.Label(root, text="Files for Comparison:", bg="#FFCCCC")
file_list_label.pack(pady=3, fill=tk.X)

file_list_frame = tk.Frame(root, bg="#FFCCCC")
file_list_frame.pack(fill=tk.BOTH, expand=True)

file_list_scrollbar = tk.Scrollbar(file_list_frame, orient=tk.VERTICAL, bg="#FFCCCC")
file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
file_list = tk.Listbox(file_list_frame, selectmode=tk.MULTIPLE, yscrollcommand=file_list_scrollbar.set, width=5, height=5, bg="#FFFFFF", fg="gray")
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
file_list_scrollbar.config(command=file_list.yview)

check_button = ttk.Button(root, text="Check Plagiarism", command=check_plagiarism, style="TButton")
check_button.pack(pady=5, fill=tk.X)

result_text = tk.Text(root, width=50, height=10, bg="#FFFFFF", fg="gray")
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
