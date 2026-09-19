"""Phase 1 smoke tests for the project skeleton."""

from config.config import DATA_DIRECTORY, INDEX_FILE, KNOWLEDGE_DIRECTORY, RAW_DIRECTORY
from main import build_parser


def test_project_data_paths_are_consistent() -> None:
    """Configured data paths must be rooted in the project data directory."""
    assert RAW_DIRECTORY.parent == DATA_DIRECTORY
    assert KNOWLEDGE_DIRECTORY.parent == DATA_DIRECTORY
    assert INDEX_FILE.parent == DATA_DIRECTORY


def test_cli_parser_can_be_constructed_without_a_command() -> None:
    """The CLI remains constructible when no optional command is supplied."""
    arguments = build_parser().parse_args([])
    assert arguments.command is None
