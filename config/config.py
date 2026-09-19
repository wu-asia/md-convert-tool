"""Central paths used by KnowledgeSync."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
RAW_DIRECTORY = DATA_DIRECTORY / "raw"
KNOWLEDGE_DIRECTORY = DATA_DIRECTORY / "knowledge"
INDEX_FILE = DATA_DIRECTORY / "index.json"
REQUEST_TIMEOUT_SECONDS = 20
