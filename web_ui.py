"""Local browser interface for the KnowledgeSync conversion pipeline."""

from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from threading import Lock
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import webbrowser

from config.config import INDEX_FILE, PROJECT_ROOT
from ksync.deduplicator import load_index
from ksync.search import search_notes
from main import add_source, import_notion_export


HOST = "127.0.0.1"
PORT = 8765
ASSET_DIRECTORY = PROJECT_ROOT / "web"
IMPORT_LOCK = Lock()


def import_from_browser(source: str) -> dict[str, object]:
    """Run one local import and return its console progress for the browser UI."""
    if not source.strip():
        return {"status": 1, "log": "Error: a source URL or local path is required.\n"}
    source_path = Path(source)
    action = import_notion_export if source_path.is_dir() else add_source
    action_argument = source_path if source_path.is_dir() else source
    captured = io.StringIO()
    with IMPORT_LOCK, redirect_stdout(captured):
        status = action(action_argument)
    return {"status": status, "log": captured.getvalue()}


class KnowledgeSyncWebHandler(BaseHTTPRequestHandler):
    """Serve the local Web UI and a deliberately small JSON API."""

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/notes":
            query = parse_qs(parsed.query).get("query", [""])[0]
            entries = load_index(INDEX_FILE)
            notes = search_notes(query, entries) if query else sorted(
                entries.values(), key=lambda entry: entry["title"].casefold()
            )
            self._send_json(HTTPStatus.OK, {"notes": notes})
            return
        self._serve_asset(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/import":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > 16_384:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid request body."})
            return
        try:
            payload = json.loads(self.rfile.read(content_length))
            source = payload["source"]
        except (json.JSONDecodeError, KeyError, TypeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Expected a JSON source field."})
            return
        if not isinstance(source, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Source must be text."})
            return
        self._send_json(HTTPStatus.OK, import_from_browser(source))

    def _serve_asset(self, request_path: str) -> None:
        relative_path = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        asset_path = (ASSET_DIRECTORY / relative_path).resolve()
        try:
            asset_path.relative_to(ASSET_DIRECTORY.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not asset_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        mime_type = {
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".html": "text/html; charset=utf-8",
        }.get(asset_path.suffix, "application/octet-stream")
        body = asset_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        """Keep routine local browser requests out of the terminal."""


def main() -> None:
    """Start the local browser UI and open it once."""
    server = ThreadingHTTPServer((HOST, PORT), KnowledgeSyncWebHandler)
    url = f"http://{HOST}:{PORT}"
    print(f"KnowledgeSync Web UI is running at {url}")
    print("Press Ctrl+C to stop the server.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKnowledgeSync Web UI stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
