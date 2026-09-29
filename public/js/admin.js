/**
 * public/js/admin.js
 * ==================
 * Admin panel — manages the movies table and the add/edit modal.
 * Demonstrates:
 *   - Listing all movies with genre/director info
 *   - Creating movies transactionally (genres + actors in one POST)
 *   - Editing movies with pre-populated form fields
 *   - Deleting movies (cascades to junction tables + ratings)
 */

const API = "/api";

// ── State ──────────────────────────────────────────────────────────────────
let allDirectors = [];
let allActors    = [];
let allGenres    = [];
let selectedGenreIds = [];
let editingMovieId   = null;

// ── DOM references ─────────────────────────────────────────────────────────
const tableBody    = document.getElementById("admin-table-body");
const modal        = document.getElementById("movie-modal-overlay");
const modalTitle   = document.getElementById("modal-title");
const addMovieBtn  = document.getElementById("add-movie-btn");
const closeBtn     = document.getElementById("modal-close-btn");
const cancelBtn    = document.getElementById("cancel-btn");
const saveBtn      = document.getElementById("save-movie-btn");
const genrePills   = document.getElementById("genre-pills");
const actorsCont   = document.getElementById("actors-container");
const addActorBtn  = document.getElementById("add-actor-row-btn");

// ══════════════════════════════════════════════════════════════════════════════
//  INITIALISE
// ══════════════════════════════════════════════════════════════════════════════
async function init() {
  // Fetch reference data in parallel
  const [dirs, acts, gens] = await Promise.all([
    apiFetch("/directors/"),
    apiFetch("/actors/"),
    apiFetch("/genres/"),
  ]);

  allDirectors = dirs.data || [];
  allActors    = acts.data || [];
  allGenres    = gens.data || [];

  populateDirectorSelect();
  renderGenrePills();

  await loadMoviesTable();
  bindEvents();

  // Check if URL has ?edit=<id> (navigated from detail page)
  const editId = new URLSearchParams(window.location.search).get("edit");
  if (editId) openEditModal(parseInt(editId));
}

// ══════════════════════════════════════════════════════════════════════════════
//  LOAD MOVIES TABLE
// ══════════════════════════════════════════════════════════════════════════════
async function loadMoviesTable() {
  try {
    const data   = await apiFetch("/movies/");
    const movies = data.data || [];

    if (!movies.length) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:3rem;color:var(--text-faint);">No movies yet. Add one!</td></tr>`;
      return;
    }

    tableBody.innerHTML = movies.map(m => {
      const genres = (m.genres || []).map(g => `<span class="genre-tag">${escapeHtml(g.name)}</span>`).join("");
      const rating = m.avg_rating ? `★ ${parseFloat(m.avg_rating).toFixed(1)}` : "—";
      return `
        <tr>
          <td>
            ${m.poster_url
              ? `<img class="table-poster" src="${escapeHtml(m.poster_url)}" alt="${escapeHtml(m.title)}" onerror="this.style.display='none'" />`
              : `<div class="table-poster" style="background:var(--surface-2);display:flex;align-items:center;justify-content:center;">🎬</div>`
            }
          </td>
          <td style="font-weight:600;">${escapeHtml(m.title)}</td>
          <td>${m.release_year || "—"}</td>
          <td>${escapeHtml(m.director_name || "—")}</td>
          <td><div style="display:flex;flex-wrap:wrap;gap:4px;">${genres || "—"}</div></td>
          <td style="color:var(--gold);font-weight:700;">${rating}</td>
          <td>
            <div class="table-actions">
              <button class="btn btn-secondary btn-sm" onclick="openEditModal(${m.id})" aria-label="Edit ${escapeHtml(m.title)}">✏️ Edit</button>
              <button class="btn btn-danger btn-sm" onclick="deleteMovie(${m.id}, '${escapeHtml(m.title)}')" aria-label="Delete ${escapeHtml(m.title)}">🗑️</button>
              <a href="/movie?id=${m.id}" class="btn btn-secondary btn-sm">👁️</a>
            </div>
          </td>
        </tr>
      `;
    }).join("");

  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="7" style="color:var(--error);padding:2rem;text-align:center;">Failed to load movies.</td></tr>`;
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  POPULATE DIRECTOR DROPDOWN
// ══════════════════════════════════════════════════════════════════════════════
function populateDirectorSelect() {
  const sel = document.getElementById("form-director");
  allDirectors.forEach(d => {
    const opt = document.createElement("option");
    opt.value = d.id;
    opt.textContent = d.name;
    sel.appendChild(opt);
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  RENDER GENRE PILLS  (clickable toggle — M:N genre selection)
// ══════════════════════════════════════════════════════════════════════════════
function renderGenrePills(selectedIds = []) {
  selectedGenreIds = [...selectedIds];
  genrePills.innerHTML = allGenres.map(g => `
    <button
      type="button"
      class="genre-pill ${selectedIds.includes(g.id) ? "selected" : ""}"
      data-genre-id="${g.id}"
      aria-pressed="${selectedIds.includes(g.id)}"
    >${escapeHtml(g.name)}</button>
  `).join("");

  genrePills.querySelectorAll(".genre-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      const id = parseInt(pill.dataset.genreId);
      if (selectedGenreIds.includes(id)) {
        selectedGenreIds = selectedGenreIds.filter(x => x !== id);
        pill.classList.remove("selected");
        pill.setAttribute("aria-pressed", "false");
      } else {
        selectedGenreIds.push(id);
        pill.classList.add("selected");
        pill.setAttribute("aria-pressed", "true");
      }
    });
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  DYNAMIC ACTOR ROWS  (for movie_actors junction table)
// ══════════════════════════════════════════════════════════════════════════════
function addActorRow(actorId = "", characterName = "") {
  const row = document.createElement("div");
  row.className = "actor-row";

  // Actor dropdown
  const actorSel = document.createElement("select");
  actorSel.className = "form-select actor-select";
  actorSel.innerHTML = `<option value="">Select actor…</option>` +
    allActors.map(a => `<option value="${a.id}" ${a.id == actorId ? "selected" : ""}>${escapeHtml(a.name)}</option>`).join("");

  // Character name input
  const charInput = document.createElement("input");
  charInput.type        = "text";
  charInput.className   = "form-input character-input";
  charInput.placeholder = "Character name";
  charInput.value       = characterName;

  // Remove row button
  const removeBtn = document.createElement("button");
  removeBtn.type      = "button";
  removeBtn.className = "btn btn-danger btn-icon";
  removeBtn.innerHTML = "✕";
  removeBtn.setAttribute("aria-label", "Remove actor row");
  removeBtn.onclick = () => row.remove();

  row.append(actorSel, charInput, removeBtn);
  actorsCont.appendChild(row);
}

// ══════════════════════════════════════════════════════════════════════════════
//  OPEN ADD MODAL
// ══════════════════════════════════════════════════════════════════════════════
function openAddModal() {
  editingMovieId = null;
  modalTitle.textContent = "Add Movie";
  document.getElementById("movie-form").reset();
  document.getElementById("form-movie-id").value = "";
  renderGenrePills([]);
  actorsCont.innerHTML = "";
  addActorRow(); // Start with one empty actor row
  openModal();
}

// ══════════════════════════════════════════════════════════════════════════════
//  OPEN EDIT MODAL  (pre-populate from /api/movies/:id)
// ══════════════════════════════════════════════════════════════════════════════
async function openEditModal(movieId) {
  editingMovieId = movieId;
  modalTitle.textContent = "Edit Movie";

  try {
    const data  = await apiFetch(`/movies/${movieId}`);
    const movie = data.data;

    // ── Populate core fields ──────────────────────────────────────────────
    document.getElementById("form-movie-id").value = movie.id;
    document.getElementById("form-title").value    = movie.title || "";
    document.getElementById("form-year").value     = movie.release_year || "";
    document.getElementById("form-duration").value = movie.duration_minutes || "";
    document.getElementById("form-synopsis").value = movie.synopsis || "";
    document.getElementById("form-poster").value   = movie.poster_url || "";
    document.getElementById("form-director").value = movie.director_id || "";

    // ── Pre-select genres ─────────────────────────────────────────────────
    const genreIds = (movie.genres || []).map(g => g.id);
    renderGenrePills(genreIds);

    // ── Pre-fill actor rows ───────────────────────────────────────────────
    actorsCont.innerHTML = "";
    if (movie.cast && movie.cast.length > 0) {
      movie.cast.forEach(a => addActorRow(a.id, a.character_name));
    } else {
      addActorRow();
    }

    openModal();
  } catch (err) {
    showToast("Failed to load movie data.", "error");
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  SAVE MOVIE  (POST or PUT with transaction on server)
// ══════════════════════════════════════════════════════════════════════════════
async function saveMovie() {
  const title      = document.getElementById("form-title").value.trim();
  const directorId = document.getElementById("form-director").value;

  if (!title) { showToast("Title is required.", "error"); return; }
  if (!directorId) { showToast("Please select a director.", "error"); return; }

  // ── Collect actor rows ────────────────────────────────────────────────────
  const actors = [];
  actorsCont.querySelectorAll(".actor-row").forEach(row => {
    const actorId       = row.querySelector(".actor-select").value;
    const characterName = row.querySelector(".character-input").value.trim();
    if (actorId) actors.push({ actor_id: parseInt(actorId), character_name: characterName });
  });

  // ── Build payload ─────────────────────────────────────────────────────────
  const payload = {
    title:            title,
    release_year:     parseInt(document.getElementById("form-year").value)     || null,
    duration_minutes: parseInt(document.getElementById("form-duration").value) || null,
    synopsis:         document.getElementById("form-synopsis").value.trim(),
    poster_url:       document.getElementById("form-poster").value.trim(),
    director_id:      parseInt(directorId),
    genre_ids:        selectedGenreIds,   // M:N genre links
    actors:           actors,             // M:N actor links with character_name
  };

  saveBtn.disabled = true;
  saveBtn.textContent = "Saving…";

  try {
    const isEdit = !!editingMovieId;
    const url    = isEdit ? `/movies/${editingMovieId}` : "/movies/";
    const method = isEdit ? "PUT" : "POST";

    const res  = await fetch(`${API}${url}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Save failed");

    showToast(isEdit ? "Movie updated!" : "Movie added!", "success");
    closeModal();
    await loadMoviesTable();
  } catch (err) {
    showToast(err.message || "Save failed.", "error");
  } finally {
    saveBtn.disabled    = false;
    saveBtn.textContent = "💾 Save Movie";
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  DELETE MOVIE  (DELETE /api/movies/:id — cascades on server via ON DELETE CASCADE)
// ══════════════════════════════════════════════════════════════════════════════
async function deleteMovie(movieId, title) {
  if (!confirm(`Delete "${title}"? This cannot be undone. All cast, genre links, and reviews will be removed.`)) return;

  try {
    const res = await fetch(`${API}/movies/${movieId}`, { method: "DELETE" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error);
    showToast(`"${title}" deleted.`, "success");
    await loadMoviesTable();
  } catch (err) {
    showToast(err.message || "Delete failed.", "error");
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  MODAL HELPERS
// ══════════════════════════════════════════════════════════════════════════════
function openModal()  { modal.classList.add("open"); document.body.style.overflow = "hidden"; }
function closeModal() { modal.classList.remove("open"); document.body.style.overflow = ""; }

// ══════════════════════════════════════════════════════════════════════════════
//  BIND EVENTS
// ══════════════════════════════════════════════════════════════════════════════
function bindEvents() {
  addMovieBtn.addEventListener("click", openAddModal);
  closeBtn.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);
  saveBtn.addEventListener("click", saveMovie);
  addActorBtn.addEventListener("click", () => addActorRow());

  // Close modal on backdrop click
  modal.addEventListener("click", e => {
    if (e.target === modal) closeModal();
  });

  // Close on Escape key
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && modal.classList.contains("open")) closeModal();
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  UTILITIES
// ══════════════════════════════════════════════════════════════════════════════
async function apiFetch(path) {
  const res = await fetch(`${API}${path}`);
  return await res.json();
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast     = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────
init();
