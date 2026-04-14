import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genres: List[str]
    favorite_moods: List[str]
    target_energy: float
    energy_tolerance: float
    preferred_danceability: float
    preferred_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file using csv.DictReader.
    Returns a list of dictionaries where numeric fields are converted to the right type.
    """
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row:
                continue

            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    favorite_genre = user_prefs.get("favorite_genre") or user_prefs.get("genre")
    favorite_mood = user_prefs.get("favorite_mood") or user_prefs.get("mood")
    target_energy = user_prefs.get("target_energy")
    if target_energy is None:
        target_energy = user_prefs.get("energy")

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = song.get("energy")

    if favorite_genre:
        favorite_genre = str(favorite_genre).strip().lower()
    if favorite_mood:
        favorite_mood = str(favorite_mood).strip().lower()

    if favorite_genre and song_genre == favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if favorite_mood and song_mood == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    try:
        energy_score = 1.0 - abs(float(song_energy) - float(target_energy))
    except (TypeError, ValueError):
        energy_score = 0.0

    if energy_score < 0.0:
        energy_score = 0.0

    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    sorted_songs = sorted(scored_songs, key=lambda item: item[1], reverse=True)

    recommendations: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in sorted_songs[:k]:
        explanation = "; ".join(reasons)
        recommendations.append((song, score, explanation))

    return recommendations
