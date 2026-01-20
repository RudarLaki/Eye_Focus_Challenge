from tkinter import ttk, simpledialog
from ui.practice_mode import PracticeMode
from ui.challenge_mode import ChallengeMode
from ui.leaderboard_menu import Leaderboard
from ui.statistics_menu import StatisticsMenu  

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        
    def setup_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Sequence Challenge Game")
        self.root.geometry("700x550")
        
        main = ttk.Frame(self.root, padding=40)
        main.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(main, text="🎯 Sequence Challenge Game", 
                 font=("Arial", 24, "bold")).pack(pady=(0, 20))
        
        # Mode selection buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=30)
        
        # Challenge Mode button
        challenge_btn = ttk.Button(button_frame, text="🏆 Challenge Mode", 
                                  command=self.start_challenge_mode,
                                  width=25)
        challenge_btn.pack(pady=10)
        
        # Practice Mode button
        practice_btn = ttk.Button(button_frame, text="🎮 Practice Mode", 
                                 command=self.start_practice_mode,
                                 width=25)
        practice_btn.pack(pady=10)
        
        # Statistics button (NEW!)
        stats_btn = ttk.Button(button_frame, text="📊 Statistics", 
                               command=self.start_statistics,
                               width=25)
        stats_btn.pack(pady=10)
        
        # Leaderboard button
        leaderboard_btn = ttk.Button(button_frame, text="🏅 Leaderboard", 
                                     command=self.start_leaderboard,
                                     width=25)
        leaderboard_btn.pack(pady=10)
        
        # Instructions
        inst_frame = ttk.LabelFrame(main, text="📝 How to Play", padding=20)
        inst_frame.pack(pady=30, fill="x")
        
        instructions = [
            "• Two sequences will be displayed side by side",
            "• Determine if they are IDENTICAL or DIFFERENT",
            "• Click 'YES' or press A on keyboard if they are exactly the SAME",
            "• Click 'NO or press D on keyboard if they have ANY difference",
            "• Try to be both FAST and ACCURATE!",
            "",
            "🏆 Challenge Mode: Timed challenge with increasing difficulty",
            "🎮 Practice Mode: Customize settings and practice freely",
            "📊 Statistics: View your performance analytics",
            "🏅 Leaderboard: View top performers"
        ]
        
        for i, inst in enumerate(instructions):
            ttk.Label(inst_frame, text=inst, font=("Arial", 10)).pack(anchor="w", pady=2)
            
        # Footer
        ttk.Label(main, text="Test your visual perception skills! 👁️", 
                 font=("Arial", 11, "italic")).pack(pady=(20, 0))
    
    def start_challenge_mode(self):
        """Prompt for username and start challenge mode"""
        username = simpledialog.askstring(
            "Enter Username", 
            "Enter your username for the leaderboard:",
            parent=self.root
        )
        
        if username and username.strip():
            ChallengeMode(self.root, username.strip(), self.show)
    
    def start_practice_mode(self):
        """Start practice mode with callback to return to main menu"""
        PracticeMode(self.root, self.show)
    
    def start_leaderboard(self):
        """Start leaderboard with callback to return to main menu"""
        Leaderboard(self.root, self.show)
    
    def start_statistics(self):
        """Start statistics view with callback to return to main menu"""
        StatisticsMenu(self.root, self.show)
    
    def show(self):
        """Show the main menu (used as callback from other modes)"""
        # Reinitialize the main menu
        self.__init__(self.root)