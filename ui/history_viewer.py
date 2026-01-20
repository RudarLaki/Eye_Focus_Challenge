import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class HistoryViewer:
    def __init__(self, root, leaderboard_entry, back_callback):
        """
        Initialize History Viewer.
        
        Args:
            root: tkinter root window
            leaderboard_entry: The leaderboard entry to show history for
            back_callback: Function to call when returning to leaderboard
        """
        self.root = root
        self.entry = leaderboard_entry
        self.back_callback = back_callback
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI for history viewer."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title(f"Challenge History - {self.entry['username']}")
        self.root.geometry("1200x700")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Header
        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Leaderboard",
                  command=self.back_callback).pack(side="left")
        
        ttk.Label(header_frame, text="📋 Challenge History", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Summary info
        summary_frame = ttk.LabelFrame(main, text="Challenge Summary", padding=15)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        # Create grid for summary
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack()
        
        # Row 1
        ttk.Label(summary_grid, text=f"Player: {self.entry['username']}", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5, padx=(0, 30))
        ttk.Label(summary_grid, text=f"Accuracy: {self.entry['accuracy']:.1f}%", 
                 font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="w", pady=5, padx=(0, 30))
        ttk.Label(summary_grid, text=f"Avg Time: {self.entry['avg_time']:.0f} ms", 
                 font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="w", pady=5)
        
        # Row 2 - Date
        if 'timestamp' in self.entry:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(self.entry['timestamp'].replace('Z', '+00:00'))
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                ttk.Label(summary_grid, text=f"Date: {date_str}", 
                         font=("Arial", 10)).grid(row=1, column=0, columnspan=3, 
                                                sticky="w", pady=(10, 0))
            except:
                pass
        
        # Check if we have detailed results
        if not self.entry.get('detailed_results'):
            messagebox.showinfo("No Detailed Data", 
                              "No detailed results available for this entry.")
            self.back_callback()
            return
        
        # Create scrollable frame for results
        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(fill="both", expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Create headers for the table
        headers_frame = ttk.Frame(scrollable_frame)
        headers_frame.pack(fill="x", pady=(0, 10))
        
        headers = ["#", "Level", "Original", "Second", "Your Guess", "Result", "Time"]
        col_widths = [5, 15, 65, 65, 15, 15, 15]
        
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            ttk.Label(headers_frame, text=header, font=("Arial", 10, "bold"),
                     width=width, anchor="center", relief="solid", padding=5).pack(side="left", padx=1)
        
        # Add each question result
        for idx, result in enumerate(self.entry['detailed_results']):
            self.create_result_row(scrollable_frame, idx, result)
    
    def create_result_row(self, parent, question_num, result):
        """Create a row displaying a single question result."""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill="x", pady=2)
        
        # Question number
        ttk.Label(row_frame, text=str(question_num + 1), width=5, anchor="center",
                 relief="solid", padding=7).pack(side="left", padx=1)
        
        # Level
        level_text = f"Level: {question_num // 5}"
        ttk.Label(row_frame, text=level_text, width=18, anchor="center",
                 relief="solid", padding=5).pack(side="left", padx=1)
        
        # Original Sequence
        seq_a = result.get('seq_a', '')
        seq_a_label = ttk.Label(row_frame, text=seq_a, font=("Courier", 11),
                               width=50, anchor="center", relief="solid", 
                               padding=5, background="white")
        seq_a_label.pack(side="left", padx=1)
        
        # Second Sequence with highlighting
        seq_b = result.get('seq_b', '')
        changed_index = result.get('changed_index')

        label_font = tkfont.Font(family="Courier", size=11)

        # Create container frame with fixed width
        container = tk.Frame(row_frame, bg="white", relief="solid", borderwidth=1, width=470, height=35)
        container.pack(side="left", padx=1)
        container.pack_propagate(False)  # Prevent frame from resizing

        # Inner frame to center content
        inner_frame = tk.Frame(container, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")  # Use place, not pack!

        # Build the text with highlighting
        if changed_index is not None and changed_index < len(seq_b):
            # Split sequence into parts: before, highlighted char, after
            before = seq_b[:changed_index]
            highlight_char = seq_b[changed_index]
            after = seq_b[changed_index + 1:]
            
            # Before text
            if before:
                tk.Label(inner_frame, text=before, font=label_font, bg="white").pack(side="left")
            
            # Highlighted character
            tk.Label(inner_frame, text=highlight_char, font=(label_font.actual("family"), 
                    label_font.actual("size"), "bold"), bg="yellow", fg="red").pack(side="left")
            
            # After text
            if after:
                tk.Label(inner_frame, text=after, font=label_font, bg="white").pack(side="left")
        else:
            # No highlighting - just show the sequence centered
            tk.Label(inner_frame, text=seq_b, font=label_font, bg="white").pack()
        # Your Guess
        user_guess = result.get('user_guess', False)
        correct_answer = result.get('correct_answer', False)
        guess_text = "NO (Diff)" if user_guess else "YES (Same)"
        guess_color = "red" if user_guess else "green"
        ttk.Label(row_frame, text=guess_text, width=18, anchor="center",
                 relief="solid", padding=5, foreground=guess_color).pack(side="left", padx=1)
        
        # Result (Correct/Wrong)
        was_correct = result.get('was_correct', False)
        if was_correct:
            result_text = "✅ Correct"
            result_color = "green"
        else:
            result_text = "❌ Wrong"
            result_color = "red"
        ttk.Label(row_frame, text=result_text, width=18, anchor="center",
                 relief="solid", padding=5, foreground=result_color).pack(side="left", padx=1)
        
        # Time
        time_ms = result.get('response_time_ms', 0)
        time_text = f"{time_ms:.0f} ms"
        time_color = "green" if time_ms < 1000 else "orange" if time_ms < 2000 else "red"
        ttk.Label(row_frame, text=time_text, width=18, anchor="center",
                 relief="solid", padding=5, foreground=time_color).pack(side="left", padx=1)
        
        # Add separator line between rows
        separator = ttk.Separator(parent, orient="horizontal")
        separator.pack(fill="x", pady=2)