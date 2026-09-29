/**
 * public/js/catalog.js
 * ====================
 * Catalog page — fetches movies from /api/movies with search/filter/sort,
 * renders movie cards, and handles user interactions.
 */

const API = "/api";

// ── State ──────────────────────────────────────────────────────────────────
let debounceTimer = null;

// ── DOM references ─────────────────────────────────────────────────────────
const grid          = document.getElementById("movie-grid");
const searchInput   = document.getElementById("search-input");
const genreFilter   = document.getElementById("genre-filter");
const yearFrom      = document.getElementById("year-from");
const yearTo        = document.getElementById("year-to");
const sortBy        = document.getElementById("sort-by");
const sortOrder     = document.getElementById("sort-order");
const clearBtn      = document.getElementById("clear-filters");
const resultsCount  = document.getElementById("results-count");

// ══════════════════════════════════════════════════════════════════════════════
//  INITIALISE
// ══════════════════════════════════════════════════════════════════════════════
async function init() {
  renderSkeletons(8);
  await Promise.all([loadGenres(), loadYearOptions()]);
  await loadMovies();
  bindControls();
}

// ══════════════════════════════════════════════════════════════════════════════
//  LOAD GENRES  (populate dropdown from /api/genres)
// ══════════════════════════════════════════════════════════════════════════════
async function loadGenres() {
  try {
    const res  = await fetch(`${API}/genres/`);
    const data = await res.json();
    const genres = data.data || [];

    genres.forEach(g => {
      const opt = document.createElement("option");
      opt.value = g.name;
      opt.textContent = g.name;
      genreFilter.appendChild(opt);
    });
  } catch (err) {
    console.error("Failed to load genres:", err);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  LOAD YEAR OPTIONS  (range: 1970 → current year)
// ══════════════════════════════════════════════════════════════════════════════
function loadYearOptions() {
  const currentYear = new Date().getFullYear();
  for (let y = currentYear; y >= 1970; y--) {
    const from = document.createElement("option");
    from.value = y;
    from.textContent = y;
    yearFrom.appendChild(from);

    const to = document.createElement("option");
    to.value = y;
    to.textContent = y;
    yearTo.appendChild(to);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  LOAD MOVIES  (calls /api/movies with all query params)
// ══════════════════════════════════════════════════════════════════════════════
async function loadMovies() {
  renderSkeletons(8);

  // Build query string from current filter state
  const params = new URLSearchParams();
  const search = searchInput.value.trim();
  const genre  = genreFilter.value;
  const from   = yearFrom.value;
  const to     = yearTo.value;

  if (search) params.set("search",     search);
  if (genre)  params.set("genre",      genre);
  if (from)   params.set("year_from",  from);
  if (to)     params.set("year_to",    to);
  params.set("sort_by",    sortBy.value);
  params.set("sort_order", sortOrder.value);

  try {
    const res  = await fetch(`${API}/movies/?${params}`);
    const data = await res.json();
    const movies = data.data || [];

    // Update results count
    const countText = movies.length === 1 ? "1 movie" : `${movies.length} movies`;
    const filterLabel = search || genre ? ` matching filters` : "";
    resultsCount.innerHTML = `<span>${countText}</span>${filterLabel}`;

    renderMovies(movies);
  } catch (err) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3>Failed to load movies</h3>
        <p>Make sure the server is running on port 5000.</p>
      </div>
    `;
    console.error("Failed to load movies:", err);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  RENDER MOVIES  (build movie cards)
// ══════════════════════════════════════════════════════════════════════════════
function renderMovies(movies) {
  grid.innerHTML = "";

  if (!movies.length) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🎬</div>
        <h3>No movies found</h3>
        <p>Try adjusting your search or filters.</p>
      </div>
    `;
    return;
  }

  movies.forEach(movie => {
    grid.appendChild(createMovieCard(movie));
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  CREATE MOVIE CARD
// ══════════════════════════════════════════════════════════════════════════════
function createMovieCard(movie) {
  const card = document.createElement("div");
  card.className = "movie-card";
  card.setAttribute("role", "article");
  card.setAttribute("tabindex", "0");
  card.setAttribute("aria-label", `${movie.title} (${movie.release_year})`);

  // Rating display
  const rating     = movie.avg_rating ? parseFloat(movie.avg_rating).toFixed(1) : null;
  const ratingHTML = rating
    ? `<div class="card-rating-badge">
         <span class="star-icon">★</span>${rating}
       </div>`
    : "";

  // Genre tags (max 3 shown)
  const genres = (movie.genres || []).slice(0, 3);
  const genreTags = genres.map(g =>
    `<span class="genre-tag">${escapeHtml(g.name)}</span>`
  ).join("");

  // Duration formatting
  const duration = movie.duration_minutes
    ? `${Math.floor(movie.duration_minutes / 60)}h ${movie.duration_minutes % 60}m`
    : "";

  card.innerHTML = `
    <div class="card-poster">
      ${movie.poster_url
        ? `<img
             src="${escapeHtml(movie.poster_url)}"
             alt="${escapeHtml(movie.title)} poster"
             loading="lazy"
             onerror="this.parentElement.innerHTML='<div class=card-poster-fallback><span>🎬</span><small>No poster</small></div>'"
           />`
        : `<div class="card-poster-fallback"><span>🎬</span><small>No poster</small></div>`
      }
      ${ratingHTML}
    </div>
    <div class="card-body">
      <div class="card-title">${escapeHtml(movie.title)}</div>
      <div class="card-director">by <span>${escapeHtml(movie.director_name || "Unknown")}</span></div>
      <div class="card-meta">
        <span>${movie.release_year || "—"}</span>
        ${duration ? `<span class="meta-dot">·</span><span>${duration}</span>` : ""}
        ${movie.rating_count ? `<span class="meta-dot">·</span><span>${movie.rating_count} reviews</span>` : ""}
      </div>
      <div class="genre-tags">${genreTags}</div>
    </div>
  `;

  // Navigate to detail page on click or Enter key
  const navigate = () => {
    window.location.href = `/movie?id=${movie.id}`;
  };
  card.addEventListener("click", navigate);
  card.addEventListener("keydown", e => { if (e.key === "Enter") navigate(); });

  return card;
}

// ══════════════════════════════════════════════════════════════════════════════
//  SKELETON LOADING CARDS
// ══════════════════════════════════════════════════════════════════════════════
function renderSkeletons(count) {
  grid.innerHTML = "";
  for (let i = 0; i < count; i++) {
    grid.innerHTML += `
      <div class="skeleton-card">
        <div class="skeleton skeleton-poster"></div>
        <div class="skeleton-body">
          <div class="skeleton skeleton-line medium"></div>
          <div class="skeleton skeleton-line short"></div>
          <div class="skeleton skeleton-line" style="height:10px;width:50%;"></div>
        </div>
      </div>
    `;
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  BIND CONTROLS  (search debounce + filter/sort listeners)
// ══════════════════════════════════════════════════════════════════════════════
function bindControls() {
  // Debounced search — waits 350ms after user stops typing
  searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(loadMovies, 350);
  });

  // Instant filter/sort changes
  [genreFilter, yearFrom, yearTo, sortBy, sortOrder].forEach(el => {
    el.addEventListener("change", loadMovies);
  });

  // Clear all filters
  clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    genreFilter.value = "";
    yearFrom.value    = "";
    yearTo.value      = "";
    sortBy.value      = "title";
    sortOrder.value   = "ASC";
    loadMovies();
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  UTILITIES
// ══════════════════════════════════════════════════════════════════════════════
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────
init();
