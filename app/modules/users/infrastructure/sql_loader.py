from pathlib import Path

def load_query(filename: str) -> str:
    path = Path(__file__).parent / "queries" / filename
    return path.read_text(encoding="utf-8")
