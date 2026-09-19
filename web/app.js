const source = document.querySelector("#source");
const activity = document.querySelector("#activity");
const convertButton = document.querySelector("#convert");
const notesElement = document.querySelector("#notes");
const noteCount = document.querySelector("#note-count");
const search = document.querySelector("#search");
const modeLabel = document.querySelector("#mode-label");
const sourceHelp = document.querySelector("#source-help");

const modes = {
  url: { label: "Web article", placeholder: "https://example.com/article", help: "Paste a public HTTP(S) article URL." },
  file: { label: "Local file", placeholder: "C:\\notes\\git-rebase.md", help: "Enter a local Markdown or HTML file path visible to this computer." },
  notion: { label: "Notion export", placeholder: "C:\\exports\\notion", help: "Enter a local Notion export directory or Markdown/HTML file path." },
};

document.querySelectorAll(".mode").forEach((button) => button.addEventListener("click", () => {
  document.querySelector(".mode.active").classList.remove("active");
  button.classList.add("active");
  const mode = modes[button.dataset.mode];
  modeLabel.textContent = mode.label; source.placeholder = mode.placeholder; sourceHelp.textContent = mode.help; source.focus();
}));

async function loadNotes(query = "") {
  const response = await fetch(`/api/notes?query=${encodeURIComponent(query)}`);
  const { notes } = await response.json();
  noteCount.textContent = notes.length;
  notesElement.innerHTML = notes.length ? notes.map((note) => `<div class="note"><strong>${escapeHtml(note.title)}</strong><span>${escapeHtml(note.path)}</span></div>`).join("") : '<div class="empty">No matching notes yet.</div>';
}

convertButton.addEventListener("click", async () => {
  const value = source.value.trim();
  if (!value) { activity.textContent = "Enter a source before converting."; source.focus(); return; }
  convertButton.disabled = true; activity.textContent = "Starting conversion...";
  try {
    const response = await fetch("/api/import", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ source: value }) });
    const result = await response.json(); activity.textContent = result.log || result.error || "No output returned.";
    await loadNotes(search.value.trim());
  } catch (error) { activity.textContent = `Connection error: ${error.message}`; }
  finally { convertButton.disabled = false; }
});

let searchTimer;
search.addEventListener("input", () => { clearTimeout(searchTimer); searchTimer = setTimeout(() => loadNotes(search.value.trim()), 180); });
function escapeHtml(value) { const node = document.createElement("span"); node.textContent = value; return node.innerHTML; }
loadNotes();
