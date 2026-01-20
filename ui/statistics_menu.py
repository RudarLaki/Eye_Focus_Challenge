import tkinter as tk
from tkinter import ttk, messagebox
from game_manager import StatisticsManager

class StatisticsMenu:
    def __init__(self, root, back_callback):
        """
        Initialize Statistics Menu.
        
        Args:
            root: tkinter root window
            back_callback: Function to call when returning to main menu
        """
        self.root = root
        self.back_callback = back_callback
        self.stats_manager = StatisticsManager()
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI for statistics."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Statistics - Sequence Challenge")
        self.root.geometry("800x650")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_callback).pack(side="left")
        
        ttk.Label(header_frame, text="📊 Statistics", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Create Notebook (Tabs)
        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # Tab 1: Overview
        overview_frame = ttk.Frame(notebook)
        notebook.add(overview_frame, text="📈 Overview")
        self.create_overview_tab(overview_frame)
        
        # Tab 2: Level Performance
        level_frame = ttk.Frame(notebook)
        notebook.add(level_frame, text="🎯 Level Performance")
        self.create_level_tab(level_frame)
        
        # Tab 3: Sequence Type
        type_frame = ttk.Frame(notebook)
        notebook.add(type_frame, text="🔄 Sequence Type")
        self.create_type_tab(type_frame)
        
        # Tab 4: Common Mistakes
        mistakes_frame = ttk.Frame(notebook)
        notebook.add(mistakes_frame, text="❌ Common Mistakes")
        self.create_mistakes_tab(mistakes_frame)
        
        # Refresh and Clear buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="🔄 Refresh Statistics",
                  command=self.setup_gui).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="🗑️ Clear All Statistics",
                  command=self.clear_statistics,
                  style="Danger.TButton").pack(side="left", padx=5)
    
    def create_overview_tab(self, parent):
        """Create the overview tab."""
        stats = self.stats_manager.get_statistics()
        
        # General Stats Frame
        general_frame = ttk.LabelFrame(parent, text="General Statistics", padding=15)
        general_frame.pack(fill="x", pady=10, padx=5)
        
        stats_grid = ttk.Frame(general_frame)
        stats_grid.pack()
        
        # Row 1
        ttk.Label(stats_grid, text="Total Games:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=5, padx=(0, 20))
        ttk.Label(stats_grid, text=f"{stats['total_games']}", 
                 font=("Arial", 10)).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(stats_grid, text="Challenge Completions:", 
                 font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", pady=5, padx=(20, 20))
        ttk.Label(stats_grid, text=f"{stats['challenge_completions']}", 
                 font=("Arial", 10)).grid(row=0, column=3, sticky="w", pady=5)
        
        # Row 2
        ttk.Label(stats_grid, text="Practice Sessions:", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5, padx=(0, 20))
        ttk.Label(stats_grid, text=f"{stats['practice_sessions']}", 
                 font=("Arial", 10)).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(stats_grid, text="Total Questions:", 
                 font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", pady=5, padx=(20, 20))
        ttk.Label(stats_grid, text=f"{stats['total_questions']}", 
                 font=("Arial", 10)).grid(row=1, column=3, sticky="w", pady=5)
        
        # Row 3 - Accuracy
        accuracy_frame = ttk.Frame(general_frame)
        accuracy_frame.pack(pady=15, fill="x")
        
        accuracy_percent = stats['overall_accuracy']
        color = "green" if accuracy_percent >= 80 else "orange" if accuracy_percent >= 60 else "red"
        
        ttk.Label(accuracy_frame, text="Overall Accuracy:", 
                 font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))
        ttk.Label(accuracy_frame, text=f"{accuracy_percent:.1f}%", 
                 font=("Arial", 14, "bold"), foreground=color).pack(side="left")
        
        # Row 4 - Response Time
        time_frame = ttk.Frame(general_frame)
        time_frame.pack(pady=10, fill="x")
        
        ttk.Label(time_frame, text="Average Response Time:", 
                 font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))
        ttk.Label(time_frame, text=f"{stats['avg_response_time']:.0f} ms", 
                 font=("Arial", 14, "bold")).pack(side="left")
        
        # Progress bar for overall accuracy
        if stats['total_questions'] > 0:
            progress_frame = ttk.Frame(general_frame)
            progress_frame.pack(pady=15, fill="x")
            
            ttk.Label(progress_frame, text="Accuracy Progress:").pack(anchor="w", pady=(0, 5))
            
            # Create custom progress bar
            canvas = tk.Canvas(progress_frame, width=400, height=25, bg="white", highlightthickness=0)
            canvas.pack(fill="x")
            
            # Draw progress bar
            width = 400
            fill_width = (accuracy_percent / 100) * width
            
            canvas.create_rectangle(0, 0, width, 25, fill="#e0e0e0", outline="")
            canvas.create_rectangle(0, 0, fill_width, 25, fill=color, outline="")
            canvas.create_text(width/2, 12.5, text=f"{accuracy_percent:.1f}%", 
                             font=("Arial", 10, "bold"))
    
    def create_level_tab(self, parent):
        """Create the level performance tab."""
        stats = self.stats_manager.get_statistics()
        
        level_frame = ttk.Frame(parent)
        level_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        headers = ["Level", "Questions", "Correct", "Accuracy"]
        for col, header in enumerate(headers):
            ttk.Label(level_frame, text=header, font=("Arial", 10, "bold"), 
                     borderwidth=1, relief="solid", padding=5).grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1)
        
        levels = [
            ("Level 1 (Length: 10)", "level_1"),
            ("Level 2 (Length: 15)", "level_2"),
            ("Level 3 (Length: 20)", "level_3")
        ]
        
        for row, (display_name, level_key) in enumerate(levels, 1):
            level_data = stats['by_level'].get(level_key, {"questions": 0, "correct": 0, "accuracy": 0})
            
            # Level name
            ttk.Label(level_frame, text=display_name, padding=5).grid(
                row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Questions
            ttk.Label(level_frame, text=str(level_data["questions"]), 
                     padding=5).grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            
            # Correct
            ttk.Label(level_frame, text=str(level_data["correct"]), 
                     padding=5).grid(row=row, column=2, sticky="nsew", padx=1, pady=1)
            
            # Accuracy with color coding
            accuracy = level_data.get("accuracy", 0)
            color = "green" if accuracy >= 80 else "orange" if accuracy >= 60 else "red"
            ttk.Label(level_frame, text=f"{accuracy:.1f}%", 
                     foreground=color, padding=5).grid(
                row=row, column=3, sticky="nsew", padx=1, pady=1)
        
        # Configure grid weights
        for i in range(4):
            level_frame.columnconfigure(i, weight=1)
    
    def create_type_tab(self, parent):
        """Create the sequence type analysis tab."""
        stats = self.stats_manager.get_statistics()
        
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        headers = ["Sequence Type", "Questions", "Correct", "Accuracy"]
        for col, header in enumerate(headers):
            ttk.Label(type_frame, text=header, font=("Arial", 10, "bold"), 
                     borderwidth=1, relief="solid", padding=5).grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1)
        
        types = [
            ("✅ Same Sequences", "same"),
            ("❌ Different Sequences", "different")
        ]
        
        for row, (display_name, type_key) in enumerate(types, 1):
            type_data = stats['by_type'].get(type_key, {"questions": 0, "correct": 0, "accuracy": 0})
            
            # Type name
            ttk.Label(type_frame, text=display_name, padding=5).grid(
                row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Questions
            ttk.Label(type_frame, text=str(type_data["questions"]), 
                     padding=5).grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            
            # Correct
            ttk.Label(type_frame, text=str(type_data["correct"]), 
                     padding=5).grid(row=row, column=2, sticky="nsew", padx=1, pady=1)
            
            # Accuracy with color coding
            accuracy = type_data.get("accuracy", 0)
            color = "green" if accuracy >= 80 else "orange" if accuracy >= 60 else "red"
            ttk.Label(type_frame, text=f"{accuracy:.1f}%", 
                     foreground=color, padding=5).grid(
                row=row, column=3, sticky="nsew", padx=1, pady=1)
        
        # Configure grid weights
        for i in range(4):
            type_frame.columnconfigure(i, weight=1)
        
        # Add insights
        insights_frame = ttk.LabelFrame(parent, text="Insights", padding=15)
        insights_frame.pack(fill="x", pady=20, padx=5)
        
        same_accuracy = stats['by_type']['same'].get('accuracy', 0)
        diff_accuracy = stats['by_type']['different'].get('accuracy', 0)
        
        if same_accuracy > 0 and diff_accuracy > 0:
            if same_accuracy > diff_accuracy:
                insight = "You're better at identifying SAME sequences!"
                tip = "Try to slow down and look more carefully for differences."
            elif diff_accuracy > same_accuracy:
                insight = "You're better at spotting DIFFERENCES!"
                tip = "Good attention to detail!"
            else:
                insight = "You're equally good at both types!"
                tip = "Excellent balanced performance!"
            
            ttk.Label(insights_frame, text=insight, 
                     font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
            ttk.Label(insights_frame, text=f"💡 {tip}", 
                     font=("Arial", 9)).pack(anchor="w", pady=2)
    
    def create_mistakes_tab(self, parent):
        """Create the common mistakes tab."""
        stats = self.stats_manager.get_statistics()
        
        if not stats.get('top_mistakes'):
            # Empty state
            empty_frame = ttk.Frame(parent)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="🎯", font=("Arial", 48)).pack(pady=10)
            ttk.Label(empty_frame, text="No mistakes recorded yet!", 
                     font=("Arial", 16)).pack(pady=10)
            ttk.Label(empty_frame, 
                     text="Keep playing - statistics will appear here as you make mistakes.", 
                     font=("Arial", 10), foreground="gray").pack()
            return
        
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="Top 5 Most Confusing Character Pairs:", 
                 font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(header_frame, 
                 text="These are the characters you most often mistake for each other.", 
                 font=("Arial", 9)).pack(anchor="w")
        
        # Create table
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)
        
        # Table headers
        headers = ["Rank", "Characters", "Times Confused", "Difficulty Level"]
        for col, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=("Arial", 10, "bold"), 
                     borderwidth=1, relief="solid", padding=5).grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1)
        
        # Add data rows
        for row, (mistake, count) in enumerate(stats['top_mistakes'], 1):
            # Rank with medal emojis
            rank_emoji = "🥇" if row == 1 else "🥈" if row == 2 else "🥉" if row == 3 else f"{row}"
            
            # Split mistake (e.g., "O→0" becomes "O" and "0")
            if "→" in mistake:
                char1, char2 = mistake.split("→")
                display_mistake = f"{char1} ⇄ {char2}"
            else:
                display_mistake = mistake
            
            # Difficulty level based on count
            if count >= 10:
                difficulty = "⚠️ Very Difficult"
                color = "red"
            elif count >= 5:
                difficulty = "⚠️ Difficult"
                color = "orange"
            else:
                difficulty = "Normal"
                color = "black"
            
            # Rank
            ttk.Label(table_frame, text=rank_emoji, padding=5, 
                     font=("Arial", 10)).grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Characters
            char_frame = ttk.Frame(table_frame)
            char_frame.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            
            if "→" in mistake:
                char1, char2 = mistake.split("→")
                ttk.Label(char_frame, text=char1, font=("Courier", 12, "bold"), 
                         foreground="red").pack(side="left", padx=2)
                ttk.Label(char_frame, text="→", font=("Arial", 10)).pack(side="left", padx=2)
                ttk.Label(char_frame, text=char2, font=("Courier", 12, "bold"), 
                         foreground="blue").pack(side="left", padx=2)
            
            # Times confused
            ttk.Label(table_frame, text=str(count), padding=5).grid(
                row=row, column=2, sticky="nsew", padx=1, pady=1)
            
            # Difficulty
            ttk.Label(table_frame, text=difficulty, padding=5, 
                     foreground=color).grid(row=row, column=3, sticky="nsew", padx=1, pady=1)
        
        # Configure grid weights
        for i in range(4):
            table_frame.columnconfigure(i, weight=1)
        
        # Add practice tip
        tip_frame = ttk.LabelFrame(parent, text="💡 Practice Tip", padding=15)
        tip_frame.pack(fill="x", pady=20, padx=5)
        
        tip_text = (
            "Focus on the character pairs you confuse most often. "
            "In Practice Mode, try using the 'Letters' or 'Alphanumeric' "
            "charsets to encounter these tricky pairs more frequently."
        )
        ttk.Label(tip_frame, text=tip_text, font=("Arial", 9), 
                 wraplength=600).pack(anchor="w")
    
    def clear_statistics(self):
        """Clear all statistics with confirmation."""
        if messagebox.askyesno("Clear Statistics", 
                              "Are you sure you want to clear all statistics?\nThis action cannot be undone."):
            self.stats_manager.clear_statistics()
            messagebox.showinfo("Statistics Cleared", 
                              "All statistics have been cleared.")
            self.setup_gui()