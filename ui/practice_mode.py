import tkinter as tk
from tkinter import ttk
import time
from logic.sequence import get_alphabet, generate_sequence, maybe_mutate_sequence


class PracticeMode:
    def __init__(self, root, back_callback):
        """
        Initialize Practice Mode.
        
        Args:
            root: tkinter root window
            back_callback: Function to call when returning to main menu
        """
        self.root = root
        self.back_callback = back_callback
        self.setup_gui()
        self.reset_state()
        
    def reset_state(self):
        """Reset game state variables."""
        self.second_sequence = []
        self.correct_answer = False
        self.changed_index = None
        self.timer_running = False
        self.start_time = 0
        
    def setup_gui(self):
        """Set up the GUI for practice mode."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Practice Mode - Sequence Challenge")
        self.root.geometry("700x600")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_callback).pack(side="left")
        
        ttk.Label(header_frame, text="🎮 Practice Mode", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Controls Frame
        controls_frame = ttk.LabelFrame(main, text="Settings", padding=15)
        controls_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        # Row 1 — Length
        ttk.Label(controls_frame, text="Length:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.length_var = tk.StringVar(value="10")
        ttk.Combobox(
            controls_frame,
            textvariable=self.length_var,
            values=["5", "10", "15", "20"],
            state="readonly",
            width=10
        ).grid(row=0, column=1, sticky="w", padx=5)
        
        # Row 2 — Charset
        ttk.Label(controls_frame, text="Charset:").grid(row=0, column=2, sticky="w", pady=5, padx=(20,5))
        self.charset_var = tk.StringVar(value="Alphanumeric")
        ttk.Combobox(
            controls_frame,
            textvariable=self.charset_var,
            values=["Letters", "Numbers", "Alphanumeric"],
            state="readonly",
            width=15
        ).grid(row=0, column=3, sticky="w", padx=5)
        
        # Row 3 — Mutation probability
        ttk.Label(controls_frame, text="Mutation %:").grid(row=1, column=0, sticky="w", pady=15, padx=5)
        self.prob_var = tk.IntVar(value=50)
        prob_scale = ttk.Scale(
            controls_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.prob_var,
            length=200
        )
        prob_scale.grid(row=1, column=1, sticky="w", padx=5)
        
        self.prob_label = ttk.Label(controls_frame, text="50%")
        self.prob_label.grid(row=1, column=2, sticky="w", padx=5)
        self.prob_var.trace("w", lambda *_: self.prob_label.config(text=f"{self.prob_var.get()}%"))
        
        # Generate button
        ttk.Button(controls_frame, text="🔄 Generate New", 
                  command=self.generate, width=15).grid(row=1, column=3, padx=20)
        
        # Timer
        self.timer_label = ttk.Label(controls_frame, text="Time: 0 ms", font=("Arial", 12, "bold"))
        self.timer_label.grid(row=0, column=4, rowspan=2, padx=20)
        
        # Display sequences
        seq_frame = ttk.Frame(main)
        seq_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Label(seq_frame, text="Original Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.original_label = ttk.Label(seq_frame, font=("Courier", 18), relief="solid", 
                                       padding=10, background="white")
        self.original_label.pack(fill="x", pady=(5, 20))
        
        ttk.Label(seq_frame, text="Second Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.seq_text = tk.Text(seq_frame, height=1, font=("Courier", 18), borderwidth=2,
                               relief="solid", bg="white")
        self.seq_text.pack(fill="x", pady=(5, 0))
        self.seq_text.tag_config("changed", background="yellow", foreground="red")
        
        # Guess Buttons
        guess_frame = ttk.Frame(main)
        guess_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        self.yes_btn = ttk.Button(guess_frame, text="✅ YES (Same)",
                                 command=lambda: self.guess(False), 
                                 width=20)
        self.yes_btn.grid(row=0, column=0, padx=10)
        
        self.no_btn = ttk.Button(guess_frame, text="❌ NO (Different)",
                                command=lambda: self.guess(True), 
                                width=20)
        self.no_btn.grid(row=0, column=1, padx=10)
        
        # Result
        self.result_label = ttk.Label(main, text="Click 'Generate New' to start", 
                                     font=("Arial", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=4, pady=10)
        
        # Utilities
        util_frame = ttk.Frame(main)
        util_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ttk.Button(util_frame, text="📋 Copy Sequence",
                  command=self.copy_to_clipboard, width=15).grid(row=0, column=0, padx=5)
        
        # Generate initial sequence
        self.root.after(100, self.generate)
        
    def start_timer(self):
        """Start the timer for the current sequence."""
        self.start_time = time.perf_counter()
        self.timer_running = True
        self.update_timer()
        
    def stop_timer(self):
        """Stop the timer."""
        self.timer_running = False
        
    def update_timer(self):
        """Update the timer display every 50ms."""
        if self.timer_running:
            elapsed = time.perf_counter() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed*1000:.0f} ms")
            self.root.after(50, self.update_timer)
            
    def generate(self):
        """Generate new sequences based on current settings."""
        self.reset_state()
        length = int(self.length_var.get())
        probability = self.prob_var.get() / 100
        alphabet = get_alphabet(self.charset_var.get())
        
        seq1 = generate_sequence(length, alphabet)
        seq2, self.changed_index = maybe_mutate_sequence(seq1, probability, alphabet)
        self.second_sequence = seq2
        self.correct_answer = self.changed_index is not None
        
        self.original_label.config(text="".join(seq1))
        self.draw_second_sequence(seq2, None)
        self.result_label.config(text="Make your guess", foreground="black")
        self.start_timer()
        
        # Enable buttons
        self.yes_btn.config(state="normal")
        self.no_btn.config(state="normal")
        
    def draw_second_sequence(self, sequence, highlight_index):
        """
        Display the second sequence with optional highlighting.
        
        Args:
            sequence: The sequence to display
            highlight_index: Index to highlight, or None for no highlighting
        """
        self.seq_text.config(state="normal")
        self.seq_text.delete("1.0", tk.END)
        
        for i, char in enumerate(sequence):
            if i == highlight_index:
                self.seq_text.insert(tk.END, char, "changed")
            else:
                self.seq_text.insert(tk.END, char)
                
        self.seq_text.config(state="disabled")
        
    def guess(self, user_guess):
        """
        Process the user's guess.
        
        Args:
            user_guess: True for "different", False for "same"
        """
        if not self.timer_running:
            return
            
        self.stop_timer()
        elapsed = time.perf_counter() - self.start_time
        
        if user_guess == self.correct_answer:
            self.result_label.config(
                text=f"✅ CORRECT — {elapsed*1000:.0f} ms",
                foreground="green"
            )
        else:
            self.result_label.config(
                text=f"❌ WRONG — {'DIFFERENT' if self.correct_answer else 'SAME'} — {elapsed*1000:.0f} ms",
                foreground="red"
            )
            
        # Reveal difference AFTER guess
        if self.changed_index is not None:
            self.draw_second_sequence(self.second_sequence, self.changed_index)
            
        # Disable buttons until next generate
        self.yes_btn.config(state="disabled")
        self.no_btn.config(state="disabled")
            
    def copy_to_clipboard(self):
        """Copy the current second sequence to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.seq_text.get("1.0", tk.END).strip())