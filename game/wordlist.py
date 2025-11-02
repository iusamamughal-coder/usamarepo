"""Loading and selecting words; ensure categories and large wordlist exist."""
from pathlib import Path
import random
import json
from datetime import datetime


class WordList:
    def __init__(self, words_dir: Path):
        self.words_dir = Path(words_dir)
        self.words_dir.mkdir(parents=True, exist_ok=True)
        (self.words_dir / "categories").mkdir(exist_ok=True)
        self.words_file = self.words_dir / "words.txt"
        self.categories_dir = self.words_dir / "categories"
        self.default_categories = {
            'Animals': ['cat', 'dog', 'elephant', 'giraffe', 'lion', 'tiger', 'zebra'],
            'Countries': ['canada', 'brazil', 'india', 'pakistan', 'germany', 'france'],
            'Programming': ['python', 'java', 'ruby', 'javascript', 'golang', 'rust'],
            'Science': ['atom', 'molecule', 'gravity', 'neutron', 'electron']
        }
        self._ensure_words()

    def _ensure_words(self):
        if not self.words_file.exists():
            words = set()
            for cat_words in self.default_categories.values():
                words.update([w.lower() for w in cat_words])

            syllables = ['an', 'or', 'en', 'ta', 'ri', 'lo', 'me', 'sa', 'fi', 'do', 'py', 'pro']
            i = 0
            while len(words) < 1000:
                w = ''.join(random.choice(syllables) for _ in range(2 + (i % 3)))
                words.add(w)
                i += 1

            with self.words_file.open('w', encoding='utf-8') as f:
                for w in sorted(words):
                    f.write(w + '\n')

        for cat, words in self.default_categories.items():
            fpath = self.categories_dir / f"{cat}.txt"
            if not fpath.exists():
                with fpath.open('w', encoding='utf-8') as f:
                    for w in words:
                        f.write(w.lower() + '\n')

    def available_categories(self):
        cats = [f.stem for f in self.categories_dir.glob('*.txt')]
        return sorted(cats)

    def pick_word(self, category: str | None):
        if category:
            file = self.categories_dir / f"{category}.txt"
            if file.exists():
                lines = [l.strip() for l in file.read_text(encoding='utf-8').splitlines() if l.strip()]
                return random.choice(lines)
        lines = [l.strip() for l in self.words_file.read_text(encoding='utf-8').splitlines() if l.strip()]
        return random.choice(lines)

    def create_new_game_log_folder(self, logs_dir: Path):
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
        stats_file = logs_dir / 'stats.json'
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        stats_file.write_text(json.dumps(stats, indent=2))

    def load_or_init_stats(self, logs_dir: Path):
        stats_file = logs_dir / 'stats.json'
        if stats_file.exists():
            return json.loads(stats_file.read_text())
        else:
            stats = {'games_played': 0, 'wins': 0, 'losses': 0, 'total_score': 0}
            self.save_stats(stats, logs_dir)
            return stats
