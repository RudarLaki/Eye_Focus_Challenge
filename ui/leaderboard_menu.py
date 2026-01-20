from tkinter import ttk, messagebox
from data.leaderboard_store import load_leaderboard, save_leaderboard
from ui.history_viewer import HistoryViewer


class Leaderboard:
    def __init__(self, root, back_callback):
        """
        Initialize Leaderboard.
        
        Args:
            root: tkinter root window
            back_callback: Function to call when returning to main menu
        """
        self.root = root
        self.back_callback = back_callback
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI for leaderboard."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Leaderboard - Sequence Challenge")
        self.root.geometry("800x600")  # Increased width for delete button
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_callback).pack(side="left")
        
        ttk.Label(header_frame, text="🏅 Leaderboard", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Load leaderboard data
        leaderboard = load_leaderboard()
        
        if not leaderboard:
            # Empty state
            empty_frame = ttk.Frame(main)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="🏆", font=("Arial", 48)).pack(pady=10)
            ttk.Label(empty_frame, text="No scores yet!", 
                     font=("Arial", 16)).pack(pady=10)
            ttk.Label(empty_frame, text="Complete a challenge to appear here!", 
                     font=("Arial", 12), foreground="gray").pack()
        else:
            # Create table frame with scrollbar
            table_frame = ttk.Frame(main)
            table_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Create scrollbar
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Create treeview
            columns = ("Rank", "Username", "Accuracy", "Avg Time", "Delete")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                               yscrollcommand=scrollbar.set, height=15)
            
            # Configure scrollbar
            scrollbar.config(command=tree.yview)
            
            # Define headings
            tree.heading("Rank", text="Rank")
            tree.heading("Username", text="Username")
            tree.heading("Accuracy", text="Accuracy (%)")
            tree.heading("Avg Time", text="Avg Time (ms)")
            tree.heading("Delete", text="")
            
            # Configure column widths
            tree.column("Rank", width=80, anchor="center")
            tree.column("Username", width=200, anchor="w")
            tree.column("Accuracy", width=150, anchor="center")
            tree.column("Avg Time", width=150, anchor="center")
            tree.column("Delete", width=80, anchor="center")
            
            # Add data
            for i, entry in enumerate(leaderboard, 1):
                rank_text = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else str(i)
                tree.insert("", "end", values=(
                    rank_text,
                    entry['username'],
                    f"{entry['accuracy']:.1f}%",
                    f"{entry['avg_time']:.0f} ms",
                    "❌"  # Delete icon
                ))
            
            # Bind click event on the Delete column
            tree.bind("<Button-1>", lambda e: self.on_treeview_click(e, tree, leaderboard))
            
            tree.pack(side="left", fill="both", expand=True)
            
        # Button frame at the bottom
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=10, fill="x")
        
        # Clear all button (left side)
        ttk.Button(button_frame, text="🗑️ Clear All",
                  command=self.clear_leaderboard).pack(side="left", padx=5)
        
        # Refresh button (right side)
        ttk.Button(button_frame, text="🔄 Refresh",
                  command=self.setup_gui).pack(side="right", padx=5)
    
    def on_treeview_click(self, event, tree, leaderboard):
        """Handle clicks on the treeview."""
        # Identify the region that was clicked
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            # Get the column and item
            column = tree.identify_column(event.x)
            item = tree.identify_row(event.y)
            
            # If delete column (column 5) was clicked
            if column == "#5" and item:
                # Get the item values
                values = tree.item(item, "values")
                username = values[1]  # Username is in the second column
                
                # Confirm deletion
                if messagebox.askyesno("Delete Record", 
                                    f"Delete record for '{username}'?"):
                    # Remove the record from leaderboard
                    leaderboard = load_leaderboard()
                    leaderboard = [entry for entry in leaderboard if entry['username'] != username]
                    save_leaderboard(leaderboard)
                    
                    # Refresh the display
                    self.setup_gui()
            
            # If any other column was clicked (show history)
            elif item and column != "#5":
                # Get the rank from the first column
                values = tree.item(item, "values")
                rank_text = values[0]
                
                # Extract rank number (remove medal emoji)
                rank_num = 0
                if "🥇" in rank_text:
                    rank_num = 1
                elif "🥈" in rank_text:
                    rank_num = 2
                elif "🥉" in rank_text:
                    rank_num = 3
                else:
                    try:
                        rank_num = int(rank_text)
                    except:  # noqa: E722
                        rank_num = 0
                
                # Find the corresponding leaderboard entry
                leaderboard = load_leaderboard()
                if 0 < rank_num <= len(leaderboard):
                    entry = leaderboard[rank_num - 1]
                    
                    # Check if we have detailed results
                    if entry.get('detailed_results'):
                        # Show history viewer
                        HistoryViewer(self.root, entry, self.setup_gui)
                    else:
                        messagebox.showinfo("No Detailed Data", 
                                        "No detailed results available for this entry.")

    def clear_leaderboard(self):
        """Clear all leaderboard entries."""
        if messagebox.askyesno("Clear Leaderboard", 
                              "Are you sure you want to clear all leaderboard entries?\nThis action cannot be undone."):
            save_leaderboard([])
            # Refresh the display
            self.setup_gui()