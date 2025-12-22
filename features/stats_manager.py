"""
KrishiMitra Persistent Stats Storage
Stores user predictions, points, streaks, and badges in Firebase/Local Storage
"""

import datetime
import json
import os

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except Exception as e:
    FIREBASE_AVAILABLE = False
    print(f"Firebase not available: {e}")


class StatsManager:
    """Manages user stats persistence"""
    
    def __init__(self, user_id: str = "farmer_default"):
        """
        Initialize stats manager
        
        Args:
            user_id: Unique identifier for the farmer user
        """
        self.user_id = user_id
        self.db = None
        self.use_firebase = False
        self.local_stats_file = f".stats_{user_id}.json"
        
        # Try to initialize Firebase
        if FIREBASE_AVAILABLE:
            try:
                if not firebase_admin.get_app():
                    # Try to initialize if no app exists
                    pass
                self.db = firestore.client()
                self.use_firebase = True
                print("✅ Using Firebase for stats storage")
            except Exception as e:
                print(f"⚠️ Firebase initialization failed, using local storage: {e}")
                self.use_firebase = False
        
        # Initialize local stats if not using Firebase
        if not self.use_firebase:
            self._init_local_stats()
    
    def _init_local_stats(self):
        """Initialize local stats file"""
        if not os.path.exists(self.local_stats_file):
            default_stats = {
                "user_id": self.user_id,
                "created_at": datetime.datetime.now().isoformat(),
                "predictions_made": 0,
                "current_streak": 0,
                "max_streak": 0,
                "total_points": 0,
                "badges": [],
                "disease_predictions": [],
                "last_prediction": None
            }
            self._save_local_stats(default_stats)
    
    def _save_local_stats(self, stats: dict):
        """Save stats to local JSON file"""
        try:
            with open(self.local_stats_file, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving local stats: {e}")
    
    def _load_local_stats(self) -> dict:
        """Load stats from local JSON file"""
        try:
            if os.path.exists(self.local_stats_file):
                with open(self.local_stats_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading local stats: {e}")
        
        return {
            "user_id": self.user_id,
            "predictions_made": 0,
            "current_streak": 0,
            "max_streak": 0,
            "total_points": 0,
            "badges": [],
            "disease_predictions": []
        }
    
    def get_stats(self) -> dict:
        """Get user stats"""
        if self.use_firebase and self.db:
            try:
                doc = self.db.collection('farmers').document(self.user_id).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                print(f"Error fetching from Firebase: {e}")
        
        # Fallback to local storage
        return self._load_local_stats()
    
    def update_prediction(self, disease: str, confidence: float = 0.0):
        """Record a new prediction"""
        stats = self.get_stats()
        
        # Update counters
        stats['predictions_made'] = stats.get('predictions_made', 0) + 1
        stats['current_streak'] = stats.get('current_streak', 0) + 1
        stats['total_points'] = stats.get('total_points', 0) + 10
        
        # Update max streak
        if stats['current_streak'] > stats.get('max_streak', 0):
            stats['max_streak'] = stats['current_streak']
        
        # Record disease prediction
        prediction_record = {
            "disease": disease,
            "timestamp": datetime.datetime.now().isoformat(),
            "confidence": confidence,
            "points_earned": 10
        }
        
        if 'disease_predictions' not in stats:
            stats['disease_predictions'] = []
        stats['disease_predictions'].append(prediction_record)
        
        # Keep only last 100 predictions
        stats['disease_predictions'] = stats['disease_predictions'][-100:]
        
        stats['last_prediction'] = datetime.datetime.now().isoformat()
        
        # Check and award badges
        stats = self._check_badges(stats)
        
        # Save stats
        self._save_stats(stats)
        
        return stats
    
    def _check_badges(self, stats: dict) -> dict:
        """Check and award badges based on achievements"""
        if 'badges' not in stats:
            stats['badges'] = []
        
        predictions = stats.get('predictions_made', 0)
        badges = stats['badges']
        badge_thresholds = {
            "first_prediction": 1,
            "10_predictions": 10,
            "25_predictions": 25,
            "50_predictions": 50,
            "100_predictions": 100,
            "250_predictions": 250,
            "500_predictions": 500
        }
        
        for badge_name, threshold in badge_thresholds.items():
            if predictions >= threshold and badge_name not in badges:
                badges.append(badge_name)
                print(f"🏆 Badge unlocked: {badge_name}")
        
        # Streak badges
        streak = stats.get('current_streak', 0)
        streak_badges = {
            "5_streak": 5,
            "10_streak": 10,
            "25_streak": 25,
            "50_streak": 50
        }
        
        for badge_name, threshold in streak_badges.items():
            if streak >= threshold and badge_name not in badges:
                badges.append(badge_name)
                print(f"🔥 Badge unlocked: {badge_name}")
        
        stats['badges'] = badges
        return stats
    
    def _save_stats(self, stats: dict):
        """Save stats to database"""
        if self.use_firebase and self.db:
            try:
                self.db.collection('farmers').document(self.user_id).set(stats)
            except Exception as e:
                print(f"Error saving to Firebase: {e}")
                # Fallback to local
                self._save_local_stats(stats)
        else:
            # Use local storage
            self._save_local_stats(stats)
    
    def reset_streak(self):
        """Reset current streak (called if user doesn't use app for a day)"""
        stats = self.get_stats()
        if stats.get('current_streak', 0) > 0:
            stats['current_streak'] = 0
            self._save_stats(stats)
    
    def get_leaderboard(self, limit: int = 10) -> list:
        """Get top farmers by points (for leaderboard)"""
        if self.use_firebase and self.db:
            try:
                query = self.db.collection('farmers').order_by(
                    'total_points', direction=firestore.Query.DESCENDING
                ).limit(limit)
                docs = query.stream()
                leaderboard = []
                for rank, doc in enumerate(docs, 1):
                    farmer_data = doc.to_dict()
                    leaderboard.append({
                        "rank": rank,
                        "user_id": farmer_data.get('user_id', 'Unknown'),
                        "points": farmer_data.get('total_points', 0),
                        "predictions": farmer_data.get('predictions_made', 0),
                        "badges": len(farmer_data.get('badges', []))
                    })
                return leaderboard
            except Exception as e:
                print(f"Error fetching leaderboard: {e}")
        
        return []
    
    def get_user_profile(self) -> dict:
        """Get detailed user profile"""
        stats = self.get_stats()
        
        profile = {
            "user_id": self.user_id,
            "predictions_made": stats.get('predictions_made', 0),
            "current_streak": stats.get('current_streak', 0),
            "max_streak": stats.get('max_streak', 0),
            "total_points": stats.get('total_points', 0),
            "badges_count": len(stats.get('badges', [])),
            "badges": stats.get('badges', []),
            "total_diseases_identified": len(set(
                p['disease'] for p in stats.get('disease_predictions', [])
            ))
        }
        
        # Calculate accuracy if predictions have confidence scores
        predictions = stats.get('disease_predictions', [])
        if predictions:
            avg_confidence = sum(p.get('confidence', 0) for p in predictions) / len(predictions)
            profile['avg_confidence'] = round(avg_confidence * 100, 1)
        
        return profile
    
    def get_disease_history(self) -> list:
        """Get history of disease predictions"""
        stats = self.get_stats()
        predictions = stats.get('disease_predictions', [])
        
        # Group by disease and count
        disease_count = {}
        for pred in predictions:
            disease = pred.get('disease', 'Unknown')
            disease_count[disease] = disease_count.get(disease, 0) + 1
        
        return sorted(disease_count.items(), key=lambda x: x[1], reverse=True)


def format_badge_display(badge_name: str) -> str:
    """Format badge name for display"""
    badge_displays = {
        "first_prediction": "🎯 First Step",
        "10_predictions": "🌱 Growing Knowledge",
        "25_predictions": "🌳 Expert Observer",
        "50_predictions": "👨‍🌾 Farmer Pro",
        "100_predictions": "🏆 Century Champion",
        "250_predictions": "💎 Quarter Master",
        "500_predictions": "👑 Master Farmer",
        "5_streak": "🔥 On Fire",
        "10_streak": "⚡ Unstoppable",
        "25_streak": "🌟 Legend",
        "50_streak": "🚀 SuperFarmer"
    }
    return badge_displays.get(badge_name, badge_name.replace('_', ' '))


def format_badge_description(badge_name: str, lang: str = 'en') -> str:
    """Get badge description in multiple languages"""
    descriptions = {
        "en": {
            "first_prediction": "Made your first disease prediction!",
            "10_predictions": "Identified 10 plant diseases!",
            "25_predictions": "Becoming an expert with 25 predictions!",
            "50_predictions": "Professional farmer status - 50 predictions!",
            "100_predictions": "Century achievement - 100 predictions!",
            "5_streak": "5-day prediction streak!",
            "10_streak": "10-day prediction streak - unstoppable!",
        },
        "hi": {
            "first_prediction": "आपने अपनी पहली बीमारी की भविष्यवाणी की!",
            "10_predictions": "10 पौधों की बीमारियों की पहचान की!",
            "25_predictions": "25 भविष्यवाणियों के साथ विशेषज्ञ बन रहे हैं!",
        },
        "kn": {
            "first_prediction": "ನಿಮ್ಮ ಮೊದಲ ರೋಗ ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿದ್ದೀರಿ!",
            "10_predictions": "10 ಸಸ್ಯ ರೋಗಗಳನ್ನು ಗುರುತುಮಾಡಿದ್ದೀರಿ!",
        }
    }
    
    lang_dict = descriptions.get(lang, descriptions.get('en', {}))
    return lang_dict.get(badge_name, badge_name.replace('_', ' '))
