import tkinter as tk
from tkinter import ttk, messagebox
import time
from logic.sequence import get_alphabet, generate_sequence, maybe_mutate_sequence
from data.leaderboard_store import add_to_leaderboard
from game_manager import StatisticsManager



class ChallengeMode:
    def __init__(self, root, username, back_callback):
        self.root = root
        self.username = username
        self.back_callback = back_callback
        self.stats_manager = StatisticsManager()  # Add this line
        self.setup_gui()
        self.reset_game()

    def reset_game(self):
        """Reset all game variables to initial state."""
        self.levels = [10, 15, 20]
        self.level_index = 0
        self.questions_per_level = 5
        self.current_question = 0
        self.sequence_a = []
        self.sequence_b = []
        self.changed_index = None
        self.correct_answer = False
        self.results = []
        self.probability = 0.5
        self.start_time = 0
        self.total_correct = 0
        self.total_time = 0
        self.correct1 = 0
        self.correct2 = 0
        self.correct3 = 0


    def setup_gui(self):
        """Set up the GUI for challenge mode."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Challenge Mode - Sequence Challenge")
        self.root.geometry("700x650")

        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 20))

        ttk.Button(
            header_frame, text="← Back to Menu", command=self.back_callback
        ).pack(side="left")

        ttk.Label(
            header_frame, text="🏆 Challenge Mode", font=("Arial", 18, "bold")
        ).pack(side="right")

        # Progress Frame
        progress_frame = ttk.LabelFrame(main, text="Progress", padding=15)
        progress_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 20))

        self.username_label = ttk.Label(
            progress_frame, text=f"Player: {self.username}", font=("Arial", 11, "bold")
        )
        self.username_label.pack(pady=(0, 5))

        self.progress_label = ttk.Label(
            progress_frame,
            text="Level 1/3 (Length: 10) - Question 1/5",
            font=("Arial", 12, "bold"),
        )
        self.progress_label.pack()

        self.stats_label = ttk.Label(
            progress_frame, text="Correct: 0/0 | Avg Time: 0 ms", font=("Arial", 10)
        )
        self.stats_label.pack(pady=(5, 0))

        # Display sequences
        seq_frame = ttk.Frame(main)
        seq_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 20))

        ttk.Label(
            seq_frame, text="Original Sequence:", font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.original_label = ttk.Label(
            seq_frame,
            font=("Courier", 18),
            relief="solid",
            padding=10,
            background="white",
        )
        self.original_label.pack(fill="x", pady=(5, 20))

        ttk.Label(seq_frame, text="Second Sequence:", font=("Arial", 12, "bold")).pack(
            anchor="w"
        )
        self.seq_text = tk.Text(
            seq_frame,
            height=1,
            font=("Courier", 18),
            borderwidth=2,
            relief="solid",
            background="white",
            padx=10,  # Add this
            pady=10,  # Add this
        )
        self.seq_text.pack(fill="x", pady=(5, 0))
        self.seq_text.tag_config("changed", background="yellow", foreground="red")
        # Guess Buttons
        guess_frame = ttk.Frame(main)
        guess_frame.grid(row=3, column=0, columnspan=4, pady=20)

        self.yes_btn = ttk.Button(
            guess_frame,
            text="✅ YES (Same) [A]",
            command=lambda: self.make_guess(False),
            width=20,
        )
        self.yes_btn.grid(row=0, column=0, padx=10)

        self.no_btn = ttk.Button(
            guess_frame,
            text="❌ NO (Different) [D]",
            command=lambda: self.make_guess(True),
            width=20,
        )
        self.no_btn.grid(row=0, column=1, padx=10)

        # Keyboard shortcuts label
        shortcut_frame = ttk.Frame(main)
        shortcut_frame.grid(row=4, column=0, columnspan=4, pady=(0, 10))

        ttk.Label(
            shortcut_frame, text="Keyboard Shortcuts:", font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)
        ttk.Label(shortcut_frame, text="[Y] = YES (Same)", font=("Arial", 10)).pack(
            side="left", padx=10
        )
        ttk.Label(shortcut_frame, text="[N] = NO (Different)", font=("Arial", 10)).pack(
            side="left", padx=10
        )

        # Timer and Result
        self.timer_label = ttk.Label(
            main, text="Time: 0 ms", font=("Arial", 14, "bold")
        )
        self.timer_label.grid(row=5, column=0, columnspan=4, pady=5)

        self.result_label = ttk.Label(
            main, text="Are the sequences the same?", font=("Arial", 14)
        )
        self.result_label.grid(row=6, column=0, columnspan=4, pady=10)

        # Bind keyboard shortcuts
        self.root.bind("<a>", lambda e: self.make_guess(False))
        self.root.bind("<A>", lambda e: self.make_guess(False))
        self.root.bind("<d>", lambda e: self.make_guess(True))
        self.root.bind("<D>", lambda e: self.make_guess(True))

        # Start the challenge
        self.root.after(100, self.start_next_question)

    def start_timer(self):
        """Start the timer for the current question."""
        self.start_time = time.perf_counter()
        self.update_challenge_timer()

    def update_challenge_timer(self):
        """Update the timer display every 50ms."""
        if self.start_time > 0:
            elapsed = time.perf_counter() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed * 1000:.0f} ms")
            self.root.after(50, self.update_challenge_timer)

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

    def start_next_question(self):
        """Generate and display the next question."""
        if self.current_question >= self.questions_per_level:
            self.level_index += 1
            if self.level_index >= len(self.levels):
                self.show_summary()
                return
            else:
                self.current_question = 0

        length = self.levels[self.level_index]
        alphabet = get_alphabet("Alphanumeric")
        seq1 = generate_sequence(length, alphabet)
        seq2, self.changed_index = maybe_mutate_sequence(
            seq1, self.probability, alphabet
        )

        self.sequence_a = seq1
        self.sequence_b = seq2
        self.correct_answer = self.changed_index is not None

        self.original_label.config(text="".join(seq1))
        self.draw_second_sequence(seq2, None)

        self.progress_label.config(
            text=f"Level {self.level_index + 1}/3 (Length: {length}) - Question {self.current_question + 1}/{self.questions_per_level}"
        )

        # Calculate stats
        total_questions = len(self.results)
        if total_questions > 0:
            avg_time = sum(r[4] for r in self.results) / total_questions
            self.stats_label.config(
                text=f"Correct: {self.total_correct}/{total_questions} | Avg Time: {avg_time * 1000:.0f} ms"
            )

        self.result_label.config(text="Are the sequences the same?", foreground="black")

        # Enable buttons
        self.yes_btn.config(state="normal")
        self.no_btn.config(state="normal")

        self.start_timer()

    def make_guess(self, user_guess):
        """
        Process the user's guess.

        Args:
            user_guess: True for "different", False for "same"
        """
        # Prevent double-clicking during timeout
        if self.start_time == 0:
            return

        elapsed = time.perf_counter() - self.start_time
        self.start_time = 0  # Stop timer updates

        self.results.append(
            (
                "".join(self.sequence_a),
                "".join(self.sequence_b),
                self.correct_answer,
                user_guess,
                elapsed,
            )
        )

        if user_guess == self.correct_answer:
            self.result_label.config(
                text=f"✅ Correct — {elapsed * 1000:.0f} ms", foreground="green"
            )
            self.total_correct += 1
            if self.level_index == 0:
                self.correct1 += 1

            elif self.level_index == 1:
                self.correct2 += 1

            elif self.level_index == 2:
                self.correct3 += 1

        else:
            self.result_label.config(
                text=f"❌ Wrong — {'Different' if self.correct_answer else 'Same'}",
                foreground="red",
            )
            if self.changed_index is not None:
                self.draw_second_sequence(self.sequence_b, self.changed_index)

        self.total_time += elapsed

        # Disable buttons
        self.yes_btn.config(state="disabled")
        self.no_btn.config(state="disabled")

        # Update stats immediately
        total_questions = len(self.results)
        avg_time = self.total_time / total_questions if total_questions > 0 else 0
        self.stats_label.config(
            text=f"Correct: {self.total_correct}/{total_questions} | Avg Time: {avg_time * 1000:.0f} ms"
        )

        self.current_question += 1
        self.root.after(1500, self.start_next_question)

    def show_summary(self):
        """Display the challenge summary and save results."""
        total_questions = len(self.results)
        accuracy = (self.total_correct / total_questions * 100) if total_questions > 0 else 0
        avg_time = (self.total_time / total_questions * 1000) if total_questions > 0 else 0
        
        detailed_results = []
        for seq_a, seq_b, correct_answer, user_guess, elapsed in self.results:
            # Find the changed character if sequences are different
            changed_index = None
            changed_char = None
            if correct_answer:  # Sequences are different
                for i, (a, b) in enumerate(zip(seq_a, seq_b)):
                    if a != b:
                        changed_index = i
                        changed_char = b
                        break
            
            detailed_results.append({
                'seq_a': seq_a,
                'seq_b': seq_b,
                'correct_answer': correct_answer,  # True = different, False = same
                'user_guess': user_guess,  # True = different, False = same
                'response_time_ms': elapsed * 1000,
                'was_correct': user_guess == correct_answer,
                'changed_index': changed_index,
                'changed_char': changed_char
            })

        # Save to leaderboard
        add_to_leaderboard(self.username, round(accuracy, 1), round(avg_time), detailed_results)
        
        # Record statistics
        self.stats_manager.record_challenge_result(self.results)
        
        summary = (
            f"🏆 Challenge Complete! 🏆\n\n"
            f"Player: {self.username}\n"
            f"Total Questions: {total_questions}\n"
            f"Correct Answers: {self.total_correct}\n"
            f"Accuracy: {accuracy:.1f}%\n"
            f"Average Time: {avg_time:.0f} ms\n\n"
            f"Your score has been saved to the leaderboard!\n\n"
            f"Congratulations! 🎉"
        )
        
        messagebox.showinfo("Challenge Summary", summary)
        self.back_callback()