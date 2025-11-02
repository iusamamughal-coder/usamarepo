"""WordList manager that only loads words from existing category .txt files."""

from pathlib import Path
import random
import json
from datetime import datetime


class WordList:
    def __init__(self, words_dir: Path):
        self.words_dir = Path(words_dir)
        self.categories_dir = self.words_dir / "categories"
        self.words_file = self.words_dir / "words.txt"

        # Ensure that the categories folder exists
        if not self.categories_dir.exists():
            raise FileNotFoundError(
                f"Missing 'categories' folder in {self.words_dir}. "
                "Please create it and add category .txt files (e.g., Animals.txt, Countries.txt, etc.)."
            )

        # Ensure that category files are present
        category_files = list(self.categories_dir.glob("*.txt"))
        if not category_files:
            raise FileNotFoundError(
                f"No category .txt files found in {self.categories_dir}. "
                "Please add at least one category file with words."
            )

        # Optional: create master word list (only if missing)
        if not self.words_file.exists():
            all_words = set()
            for cat_file in category_files:
                for line in cat_file.read_text(encoding="utf-8").splitlines():
                    word = line.strip().lower()
                    if word:
                        all_words.add(word)

            if not all_words:
                raise ValueError("No words found in category files. Please add words first.")

            with self.words_file.open("w", encoding="utf-8") as f:
                for w in sorted(all_words):
                    f.write(w + "\n")

    def available_categories(self):
        """Return the names of available categories (from .txt files)."""
        return sorted([f.stem for f in self.categories_dir.glob("*.txt")])

    def pick_word(self, category: str | None):
        """Pick a random word from a category, or from the combined words.txt file."""
        if category:
            file = self.categories_dir / f"{category}.txt"
            if file.exists():
                lines = [l.strip() for l in file.read_text(encoding='utf-8').splitlines() if l.strip()]
                if lines:
                    return random.choice(lines)
                else:
                    raise ValueError(f"The category '{category}' file is empty.")
            else:
                raise FileNotFoundError(f"Category file '{category}.txt' not found in {self.categories_dir}.")

        # Pick from the combined list
        if not self.words_file.exists():
            raise FileNotFoundError(f"Missing words.txt in {self.words_dir}. Please add it manually or recreate it.")

        lines = [l.strip() for l in self.words_file.read_text(encoding='utf-8').splitlines() if l.strip()]
        if not lines:
            raise ValueError("The words.txt file is empty.")
        return random.choice(lines)

    def create_new_game_log_folder(self, logs_dir: Path):
        """Create a new folder for game logs (e.g., logs/game1/)."""
        logs_dir.mkdir(parents=True, exist_ok=True)
        existing = [p for p in logs_dir.iterdir() if p.is_dir() and p.name.startswith('game')]
        nums = [int(p.name.replace('game', '')) for p in existing if p.name.replace('game', '').isdigit()]
        next_n = max(nums) + 1 if nums else 1
        folder = logs_dir / f'game{next_n}'
        folder.mkdir(parents=True, exist_ok=False)
        log_file = folder / 'log.txt'
        log_file.write_text(f"Game {next_n} Log\n\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        return folder, log_file

    def save_stats(self, stats: dict, logs_dir: Path):
        """Save stats (games played, wins, etc.) to stats.json."""
        stats_file = logs_dir / 'stats.json'
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        stats_file.write_text(json.dumps(stats, indent=2))

    def load_or_init_stats(self, logs_dir: Path):
        """Load existing stats, or initialize new ones if missing."""
        stats_file = logs_dir / 'stats.json'
        if stats_file.exists():
            return json.loads(stats_file.read_text())
        else:
            stats = {'games_played': 0, 'wins': 0, 'losses': 0, 'total_score': 0}
            self.save_stats(stats, logs_dir)
            return stats