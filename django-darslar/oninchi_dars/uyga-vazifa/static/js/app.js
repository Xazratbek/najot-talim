function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return "";
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-favorite-url]");
  if (!button) return;

  event.preventDefault();

  const response = await fetch(button.dataset.favoriteUrl, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "X-Requested-With": "XMLHttpRequest",
    },
  });

  if (response.status === 403) {
    window.location.href = button.dataset.loginUrl;
    return;
  }

  if (!response.ok) return;

  const payload = await response.json();
  button.classList.toggle("is-active", payload.status === "added");
});

document.addEventListener("click", (event) => {
  const thumb = event.target.closest("[data-gallery-thumb]");
  if (!thumb) return;

  const target = document.querySelector("[data-gallery-main]");
  if (!target) return;

  target.src = thumb.dataset.galleryThumb;
});
