import json
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Load leaderboard from file."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:  # noqa: E722
            return []
    return []

def save_leaderboard(leaderboard):
    """Save leaderboard to file."""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

def add_to_leaderboard(username, accuracy, avg_time, detailed_results=None):
    """
    Add a score to the leaderboard.
    
    Args:
        username: Player's username
        accuracy: Accuracy percentage
        avg_time: Average time in milliseconds
        detailed_results: List of detailed results for each question
    """
    leaderboard = load_leaderboard()
    
    entry = {
        'username': username,
        'accuracy': accuracy,
        'avg_time': avg_time,
        'timestamp': datetime.now().isoformat(),
        'detailed_results': detailed_results or []
    }
    
    leaderboard.append(entry)
    
    # Sort by accuracy (descending), then by avg_time (ascending - faster is better)
    leaderboard.sort(key=lambda x: (-x['accuracy'], x['avg_time']))
    
    # Keep only top 50 scores
    if len(leaderboard) > 50:
        leaderboard = leaderboard[:50]
    
    save_leaderboard(leaderboard)