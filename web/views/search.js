// Field search box on the dashboard.
// TRAINING DEMO: this file contains an INTENTIONAL vulnerability (client-side XSS).

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const term = params.get("q");
  if (term) {
    // VULNERABLE (intentional): URL input is written into the page as HTML
    document.getElementById("search-title").innerHTML = "Results for: " + term;
  }
});
