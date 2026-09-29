/**
 * public/js/movie.js
 * ==================
 * Movie detail page — fetches full movie data from /api/movies/:id
 * and renders: poster, director info, genre tags, cast list,
 * reviews, avg rating stars, and handles review submission.
 */

const API = "/api";

// ── Get movie ID from URL query string (?id=5) ────────────────────────────
const movieId = new URLSearchParams(window.location.search).get("id");

// ── State: current rating score chosen by star picker ─────────────────────
let selectedScore = 0;

// ══════════════════════════════════════════════════════════════════════════════
//  INITIALISE
// ══════════════════════════════════════════════════════════════════════════════
async function init() {
  if (!movieId) {
    document.getElementById("detail-skeleton").innerHTML =
      `<div class="empty-state"><div class="empty-icon">❌</div>
       <h3>No movie specified</h3><p><a href="/">← Back to catalog</a></p></div>`;
    return;
  }

  await loadMovieDetail();
  bindReviewForm();
  bindStarPicker();
  bindDeleteButton();
}

// ══════════════════════════════════════════════════════════════════════════════
//  LOAD MOVIE DETAIL  (GET /api/movies/:id)
// ══════════════════════════════════════════════════════════════════════════════
async function loadMovieDetail() {
  try {
    const res  = await fetch(`${API}/movies/${movieId}`);
    if (!res.ok) throw new Error("Not found");
    const data  = await res.json();
    const movie = data.data;

    renderMovie(movie);

    // Set edit link to admin with movie ID
    document.getElementById("edit-movie-btn").onclick = () => {
      window.location.href = `/admin?edit=${movie.id}`;
    };

  } catch (err) {
    document.getElementById("detail-skeleton").innerHTML =
      `<div class="empty-state"><div class="empty-icon">🎬</div>
       <h3>Movie not found</h3><p><a href="/">← Back to catalog</a></p></div>`;
  }
}

// ══════════════════════════════════════════════════════════════════════════════
//  RENDER MOVIE DETAIL
// ══════════════════════════════════════════════════════════════════════════════
function renderMovie(movie) {
  // ── Page meta ─────────────────────────────────────────────────────────────
  document.title = `${movie.title} — Movie Catalog`;
  document.getElementById("page-desc").content =
    `${movie.title} (${movie.release_year}) — directed by ${movie.director_name}.`;

  // ── Poster ────────────────────────────────────────────────────────────────
  const posterImg = document.getElementById("detail-poster-img");
  if (movie.poster_url) {
    posterImg.src = movie.poster_url;
    posterImg.alt = `${movie.title} poster`;
  } else {
    posterImg.parentElement.innerHTML =
      `<div class="card-poster-fallback" style="height:100%;"><span>🎬</span></div>`;
  }

  // ── Core info ─────────────────────────────────────────────────────────────
  document.getElementById("detail-title").textContent    = movie.title;
  document.getElementById("detail-year").textContent     = movie.release_year || "—";
  document.getElementById("detail-duration").textContent = movie.duration_minutes
    ? `${Math.floor(movie.duration_minutes / 60)}h ${movie.duration_minutes % 60}m`
    : "—";
  document.getElementById("detail-synopsis").textContent = movie.synopsis || "No synopsis available.";

  // ── Avg Rating + Stars ────────────────────────────────────────────────────
  const score = parseFloat(movie.avg_rating);
  if (!isNaN(score)) {
    document.getElementById("detail-score").textContent = score.toFixed(1);
    document.getElementById("detail-rating-count").textContent =
      `${movie.rating_count} review${movie.rating_count !== 1 ? "s" : ""}`;
    renderStars("detail-stars", score, 10);
  } else {
    document.getElementById("detail-score").textContent = "—";
    document.getElementById("detail-rating-count").textContent = "No reviews yet";
  }

  // ── Genre badges ──────────────────────────────────────────────────────────
  const genreEl = document.getElementById("detail-genres");
  genreEl.innerHTML = (movie.genres || [])
    .map(g => `<span class="genre-tag">${escapeHtml(g.name)}</span>`)
    .join("");

  // ── Director card (1:N relationship data) ────────────────────────────────
  document.getElementById("detail-director-name").textContent = movie.director_name || "Unknown";
  document.getElementById("detail-director-meta").textContent =
    movie.director_birth_year
      ? `Born ${movie.director_birth_year}${movie.director_bio ? " · " + movie.director_bio.slice(0, 80) + "…" : ""}`
      : (movie.director_bio ? movie.director_bio.slice(0, 100) + "…" : "");

  // ── Cast list (M:N via movie_actors — character_name comes from junction) ─
  const castGrid = document.getElementById("cast-grid");
  if (movie.cast && movie.cast.length > 0) {
    castGrid.innerHTML = movie.cast.map(actor => `
      <div class="cast-card">
        <div class="cast-avatar">🎭</div>
        <div>
          <div class="cast-name">${escapeHtml(actor.name)}</div>
          <div class="cast-character">as ${escapeHtml(actor.character_name || "Unknown role")}</div>
        </div>
      </div>
    `).join("");
  } else {
    document.getElementById("cast-section").style.display = "none";
  }

  // ── Reviews ───────────────────────────────────────────────────────────────
  renderReviews(movie.ratings || []);

  // ── Show content, hide skeleton ───────────────────────────────────────────
  document.getElementById("detail-skeleton").style.display = "none";
  document.getElementById("detail-content").style.display = "block";
}

// ══════════════════════════════════════════════════════════════════════════════
//  RENDER REVIEWS LIST
// ══════════════════════════════════════════════════════════════════════════════
function renderReviews(ratings) {
  const reviewsList = document.getElementById("reviews-list");

  if (!ratings.length) {
    reviewsList.innerHTML =
      `<p style="color:var(--text-faint);font-size:0.9rem;">No reviews yet. Be the first!</p>`;
    return;
  }

  reviewsList.innerHTML = ratings.map(r => `
    <div class="review-card">
      <div class="review-header">
        <span class="reviewer-name">👤 ${escapeHtml(r.user_name)}</span>
        <span class="review-score">★ ${r.score}/10</span>
      </div>
      ${r.review ? `<p class="review-text">${escapeHtml(r.review)}</p>` : ""}
      <div class="review-date">${formatDate(r.created_at)}</div>
    </div>
  `).join("");
}

// ══════════════════════════════════════════════════════════════════════════════
//  RENDER STAR DISPLAY  (score out of 10, displayed as 5 visual stars)
// ══════════════════════════════════════════════════════════════════════════════
function renderStars(containerId, score, outOf = 10) {
  const container = document.getElementById(containerId);
  const five = (score / outOf) * 5;           // convert score to 5-star scale
  let html = "";
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(five))     html += `<span class="star filled">★</span>`;
    else if (i - 0.5 <= five)     html += `<span class="star partial">★</span>`;
    else                           html += `<span class="star">★</span>`;
  }
  container.innerHTML = html;
}

// ══════════════════════════════════════════════════════════════════════════════
//  STAR PICKER (interactive rating input)
// ══════════════════════════════════════════════════════════════════════════════
function bindStarPicker() {
  const picker     = document.getElementById("star-picker");
  const scoreInput = document.getElementById("review-score");
  const btns       = picker.querySelectorAll(".star-btn");

  function highlightStars(val) {
    btns.forEach(btn => {
      btn.classList.toggle("active", parseInt(btn.dataset.value) <= val);
    });
  }

  btns.forEach(btn => {
    btn.addEventListener("mouseenter", () => highlightStars(parseInt(btn.dataset.value)));
    btn.addEventListener("mouseleave", () => highlightStars(selectedScore));
    btn.addEventListener("click", () => {
      selectedScore = parseInt(btn.dataset.value);
      scoreInput.value = selectedScore;
      highlightStars(selectedScore);
    });
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  REVIEW FORM SUBMISSION  (POST /api/movies/:id/ratings)
// ══════════════════════════════════════════════════════════════════════════════
function bindReviewForm() {
  const form       = document.getElementById("review-form");
  const submitBtn  = document.getElementById("review-submit-btn");
  const scoreInput = document.getElementById("review-score");

  form.addEventListener("submit", async e => {
    e.preventDefault();

    const userName = document.getElementById("review-username").value.trim();
    const score    = parseInt(scoreInput.value);
    const review   = document.getElementById("review-text").value.trim();

    // ── Client-side validation ────────────────────────────────────────────
    if (!userName) { showToast("Please enter your name.", "error"); return; }
    if (!score || score < 1 || score > 10) {
      showToast("Please select a score (1–10).", "error");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting…";

    try {
      const res = await fetch(`${API}/movies/${movieId}/ratings`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ user_name: userName, score, review }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Submission failed");

      showToast("Review submitted! Thank you.", "success");

      // Reset form
      form.reset();
      selectedScore = 0;
      document.getElementById("star-picker")
        .querySelectorAll(".star-btn")
        .forEach(b => b.classList.remove("active"));

      // Reload movie to show updated avg rating + new review
      await loadMovieDetail();

    } catch (err) {
      showToast(err.message || "Failed to submit review.", "error");
    } finally {
      submitBtn.disabled  = false;
      submitBtn.textContent = "⭐ Submit Review";
    }
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  DELETE MOVIE BUTTON
// ══════════════════════════════════════════════════════════════════════════════
function bindDeleteButton() {
  document.getElementById("delete-movie-btn").addEventListener("click", async () => {
    if (!confirm("Are you sure you want to delete this movie? This action cannot be undone.")) return;

    try {
      const res = await fetch(`${API}/movies/${movieId}`, { method: "DELETE" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast("Movie deleted.", "success");
      setTimeout(() => window.location.href = "/", 1200);
    } catch (err) {
      showToast(err.message || "Delete failed.", "error");
    }
  });
}

// ══════════════════════════════════════════════════════════════════════════════
//  UTILITIES
// ══════════════════════════════════════════════════════════════════════════════
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function formatDate(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleDateString("en-IN", {
      year: "numeric", month: "short", day: "numeric"
    });
  } catch { return iso; }
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
