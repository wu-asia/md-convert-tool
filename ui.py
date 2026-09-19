"""Tkinter desktop interface for KnowledgeSync imports."""

from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
import tkinter as tk
from tkinter import filedialog, ttk

from main import add_source, import_notion_export, list_notes


class KnowledgeSyncApp(ttk.Frame):
    """A small desktop interface around the existing import pipeline."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=20)
        self.master = master
        self.result_queue: Queue[str] = Queue()
        self.source = tk.StringVar()
        self._build_layout()

    def _build_layout(self) -> None:
        self.master.title("KnowledgeSync")
        self.master.minsize(720, 460)
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="KnowledgeSync", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            self,
            text="Import a public URL, local Markdown/HTML file, or Notion export directory.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        source_frame = ttk.Frame(self)
        source_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        source_frame.columnconfigure(0, weight=1)
        ttk.Entry(source_frame, textvariable=self.source).grid(row=0, column=0, sticky="ew")
        ttk.Button(source_frame, text="Choose File", command=self._choose_file).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Button(source_frame, text="Choose Notion Folder", command=self._choose_folder).grid(
            row=0, column=2, padx=(8, 0)
        )

        actions = ttk.Frame(self)
        actions.grid(row=3, column=0, sticky="new")
        self.import_button = ttk.Button(actions, text="Import and Convert", command=self._import)
        self.import_button.grid(row=0, column=0, sticky="w")
        self.list_button = ttk.Button(actions, text="List Notes", command=self._list_notes)
        self.list_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.output = tk.Text(self, height=16, wrap="word", state="disabled")
        self.output.grid(row=4, column=0, sticky="nsew", pady=(14, 0))
        self.rowconfigure(4, weight=1)

    def _choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Choose a knowledge source",
            filetypes=[
                ("Supported files", "*.md *.markdown *.html *.htm"),
                ("Markdown", "*.md *.markdown"),
                ("HTML", "*.html *.htm"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.source.set(path)

    def _choose_folder(self) -> None:
        path = filedialog.askdirectory(title="Choose a Notion export directory")
        if path:
            self.source.set(path)

    def _import(self) -> None:
        source = self.source.get().strip()
        if not source:
            self._write_output("Enter a public URL or choose a local file/folder first.\n")
            return
        action = import_notion_export if Path(source).is_dir() else add_source
        self._run_in_background(action, source)

    def _list_notes(self) -> None:
        self._run_in_background(list_notes)

    def _run_in_background(self, action, *arguments: str) -> None:
        self.import_button.state(["disabled"])
        self.list_button.state(["disabled"])
        self._write_output("\n--- Running ---\n")

        def worker() -> None:
            captured = io.StringIO()
            with redirect_stdout(captured):
                status = action(*arguments)
            self.result_queue.put(captured.getvalue() + f"Exit status: {status}\n")

        Thread(target=worker, daemon=True).start()
        self.after(100, self._poll_result)

    def _poll_result(self) -> None:
        try:
            message = self.result_queue.get_nowait()
        except Empty:
            self.after(100, self._poll_result)
            return
        self._write_output(message)
        self.import_button.state(["!disabled"])
        self.list_button.state(["!disabled"])

    def _write_output(self, message: str) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", message)
        self.output.see("end")
        self.output.configure(state="disabled")


def main() -> None:
    """Launch the KnowledgeSync desktop interface."""
    root = tk.Tk()
    KnowledgeSyncApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
