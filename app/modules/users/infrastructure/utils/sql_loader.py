from pathlib import Path

def load_query(filename: str) -> str:
    base_path = Path(__file__).parent.parent / "queries"
    file_path = base_path / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo SQL: {file_path}")

    return file_path.read_text(encoding="utf-8")
