import json
import os
from datetime import datetime
from collections import Counter
import statistics
import config

class StatisticsManager:
    def __init__(self):
        self.stats_file = "statistics.json"
        self.load_statistics()
    
    def load_statistics(self):
        """Load statistics from file or create default structure."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.data = json.load(f)
            except:  # noqa: E722
                self.data = self._create_default_stats()
        else:
            self.data = self._create_default_stats()
        self.save_statistics()
    
    def _create_default_stats(self):
        """Create default statistics structure."""
        return {
            "total_games": 0,
            "total_questions": 0,
            "total_correct": 0,
            "challenge_completions": 0,
            "practice_sessions": 0,
            "by_level": {
                "level_1": {"questions": 0, "correct": 0},
                "level_2": {"questions": 0, "correct": 0},
                "level_3": {"questions": 0, "correct": 0}
            },
            "by_type": {
                "same": {"questions": 0, "correct": 0},
                "different": {"questions": 0, "correct": 0}
            },
            "mistakes": {},
            "response_times": [],
            "last_played": None
        }
    
    def save_statistics(self):
        """Save statistics to file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    

    def record_challenge_result(self, results):
        """Record results from a challenge mode session."""
        self.data["total_games"] += 1
        self.data["challenge_completions"] += 1
        
        for idx, (seq_a, seq_b, correct_answer, user_guess, elapsed) in enumerate(results):
            self.data["total_questions"] += 1
            
            # Calculate level based on question index (0-4: level 1, 5-9: level 2, 10-14: level 3)
            question_number = idx  # 0-based
            level_index = min(question_number // config.QUESTIONS_PER_LEVEL, 2)  # Max level 2 (0,1,2)
            level_key = f"level_{level_index + 1}"
            
            # Record by level
            if level_key in self.data["by_level"]:
                self.data["by_level"][level_key]["questions"] += 1
                if user_guess == correct_answer:
                    self.data["by_level"][level_key]["correct"] += 1
                # Record by type
                type_key = "different" if correct_answer else "same"
                self.data["by_type"][type_key]["questions"] += 1

                # Record mistake
                if correct_answer:  # Different sequences
                    changed_index = None
                    # Find the changed character
                    for i, (a, b) in enumerate(zip(seq_a, seq_b)):
                        if a != b:
                            changed_index = i  # noqa: F841
                            mistake_key = f"{a}→{b}"
                            self.data["mistakes"][mistake_key] = self.data["mistakes"].get(mistake_key, 0) + 1
                            break
            
            # Record response time for correct answers
            if user_guess == correct_answer:
                self.data["response_times"].append(elapsed)
        
        self.data["last_played"] = datetime.now().isoformat()
        self.save_statistics()
    
    def record_practice_result(self, was_correct, seq_a=None, seq_b=None, elapsed=None):
        """Record results from practice mode."""
        self.data["practice_sessions"] += 1
        self.data["total_questions"] += 1
        
        if was_correct:
            self.data["total_correct"] += 1
            if elapsed:
                self.data["response_times"].append(elapsed)
        
        self.data["last_played"] = datetime.now().isoformat()
        self.save_statistics()
    
    def record_mistake(self, seq_a, seq_b, user_guess, correct_answer):
        """Record a specific mistake."""
        if user_guess != correct_answer and correct_answer:  # Different sequences
            for i, (a, b) in enumerate(zip(seq_a, seq_b)):
                if a != b:
                    mistake_key = f"{a}→{b}"
                    self.data["mistakes"][mistake_key] = self.data["mistakes"].get(mistake_key, 0) + 1
                    break
    
    def get_statistics(self):
        """Get formatted statistics."""
        stats = self.data.copy()
        
        # Calculate percentages
        if stats["total_questions"] > 0:
            stats["overall_accuracy"] = (stats["total_correct"] / stats["total_questions"]) * 100
        else:
            stats["overall_accuracy"] = 0
        
        # Level accuracy
        for level in stats["by_level"]:
            level_data = stats["by_level"][level]
            if level_data["questions"] > 0:
                level_data["accuracy"] = (level_data["correct"] / level_data["questions"]) * 100
            else:
                level_data["accuracy"] = 0
        
        # Type accuracy
        for type_key in stats["by_type"]:
            type_data = stats["by_type"][type_key]
            if type_data["questions"] > 0:
                type_data["accuracy"] = (type_data["correct"] / type_data["questions"]) * 100
            else:
                type_data["accuracy"] = 0
        
        # Average response time
        if stats["response_times"]:
            stats["avg_response_time"] = statistics.mean(stats["response_times"]) * 1000  # Convert to ms
        else:
            stats["avg_response_time"] = 0
        
        # Top 5 most common mistakes
        if stats["mistakes"]:
            top_mistakes = Counter(stats["mistakes"]).most_common(5)
            stats["top_mistakes"] = [(mistake, count) for mistake, count in top_mistakes]
        else:
            stats["top_mistakes"] = []
        
        return stats
    
    def clear_statistics(self):
        """Clear all statistics."""
        self.data = self._create_default_stats()
        self.save_statistics()


# Create a global instance
stats_manager = StatisticsManager()