
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import sys
import io
import benchmark

class BenchmarkGUI:
    def __init__(self, root):
        self.root = root
        root.title("Benchmark GUI")

        # Model selection
        tk.Label(root, text="Select Model:").grid(row=0, column=0, sticky='w')
        self.model_var = tk.StringVar(value="llama3.1:8b")
        tk.OptionMenu(root, self.model_var, 'llama3.1:8b', 'llama').grid(row=0, column=1)

        # Token entry
        tk.Label(root, text="Token:").grid(row=1, column=0, sticky='w')
        self.token_entry = tk.Entry(root, width=60)
        self.token_entry.grid(row=1, column=1)

        # URL entry
        tk.Label(root, text="Base URL:").grid(row=2, column=0, sticky='w')
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.insert(0, "http://127.0.0.1:42004")
        self.url_entry.grid(row=2, column=1)

        # Timeout slider
        tk.Label(root, text="Timeout (seconds):").grid(row=3, column=0, sticky='w')
        self.timeout_var = tk.IntVar(value=30)
        tk.Scale(root, from_=10, to=120, orient=tk.HORIZONTAL, variable=self.timeout_var).grid(row=3, column=1)

        # Rounds slider
        tk.Label(root, text="Rounds:").grid(row=4, column=0, sticky='w')
        self.rounds_var = tk.IntVar(value=5)
        tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.rounds_var).grid(row=4, column=1)

        # Prompt file selector
        tk.Label(root, text="Prompt file:").grid(row=5, column=0, sticky='w')
        self.prompt_file_path = tk.StringVar()
        tk.Entry(root, textvariable=self.prompt_file_path, width=50).grid(row=5, column=1)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=5, column=2)

        # Run button
        tk.Button(root, text="Run Benchmark", command=self.run_benchmark_thread).grid(row=6, column=1, pady=10)

        # Output box
        self.output_box = scrolledtext.ScrolledText(root, width=80, height=30)
        self.output_box.grid(row=7, column=0, columnspan=3)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.prompt_file_path.set(filename)

    def run_benchmark_thread(self):
        thread = threading.Thread(target=self.run_benchmark)
        thread.start()

    def run_benchmark(self):
        self.output_box.delete('1.0', tk.END)

        
        benchmark.model = self.model_var.get()
        benchmark.token = self.token_entry.get()
        benchmark.base_url = self.url_entry.get()
        benchmark.timeout = self.timeout_var.get()
        benchmark.rounds = self.rounds_var.get()
        benchmark.prompt_file = self.prompt_file_path.get()

        if not benchmark.token or not benchmark.base_url or not benchmark.prompt_file:
            messagebox.showerror("Error", "Please fill all fields and select prompt file")
            return

        
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        try:
            benchmark.main()
        except Exception as e:
            print(f"Error running benchmark: {e}")

        sys.stdout = old_stdout
        output = mystdout.getvalue()
        self.output_box.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = BenchmarkGUI(root)
    root.mainloop()
