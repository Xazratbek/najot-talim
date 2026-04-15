const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.querySelector(".primary-nav");

if (navToggle && primaryNav) {
    navToggle.addEventListener("click", () => {
        const expanded = navToggle.getAttribute("aria-expanded") === "true";
        navToggle.setAttribute("aria-expanded", String(!expanded));
        primaryNav.classList.toggle("is-open");
    });
}

const revealItems = document.querySelectorAll(".reveal");
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.16,
});

revealItems.forEach((item) => revealObserver.observe(item));

const isAuthenticated = document.body.dataset.authenticated === "true";

function getCookie(name) {
    const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
    return match ? decodeURIComponent(match[2]) : null;
}

function setButtonState(button, text) {
    if (!button) return;
    if (button.classList.contains("icon-button")) {
        const icon = button.querySelector("i");
        if (icon) {
            if (button.classList.contains("icon-button-cart")) {
                const added = text.toLowerCase().includes("qo'shildi") || text.toLowerCase().includes("added");
                icon.className = added ? "bi bi-bag-check-fill" : "bi bi-bag-plus";
            } else {
                const added = text.toLowerCase().includes("qo'shildi");
                const removed = text.toLowerCase().includes("olib tashlandi");
                icon.className = added ? "bi bi-heart-fill" : removed ? "bi bi-heart" : icon.className;
            }
        }
        button.title = text;
        return;
    }
    const original = button.dataset.originalText || button.textContent.trim();
    button.dataset.originalText = original;
    button.textContent = text;
    window.setTimeout(() => {
        button.textContent = button.dataset.originalText;
    }, 1600);
}

const cartDrawer = document.querySelector("[data-cart-drawer]");
const cartBackdrop = document.querySelector("[data-cart-backdrop]");
const cartOpenButton = document.querySelector("[data-cart-open]");
const cartCloseButton = document.querySelector("[data-cart-close]");
const cartItemsNode = document.querySelector("[data-cart-items]");
const cartCountNode = document.querySelector("[data-cart-count]");

function openCart() {
    if (!cartDrawer || !cartBackdrop) return;
    cartDrawer.classList.add("is-open");
    cartBackdrop.classList.add("is-visible");
    cartDrawer.setAttribute("aria-hidden", "false");
}

function closeCart() {
    if (!cartDrawer || !cartBackdrop) return;
    cartDrawer.classList.remove("is-open");
    cartBackdrop.classList.remove("is-visible");
    cartDrawer.setAttribute("aria-hidden", "true");
}

async function loadCart() {
    if (!isAuthenticated || !cartItemsNode) return;

    try {
        const response = await fetch("/orders/my_cart/", {
            headers: { "X-Requested-With": "XMLHttpRequest" },
        });

        if (!response.ok) return;
        const data = await response.json();

        if (cartCountNode) {
            cartCountNode.textContent = data.total_count ?? 0;
        }

        if (!data.cart_items || !data.cart_items.length) {
            cartItemsNode.innerHTML = '<p class="empty-state">Savat hozircha bo‘sh.</p>';
            return;
        }

        cartItemsNode.innerHTML = data.cart_items.map((item) => `
            <article class="cart-line">
                ${item.image ? `<img src="${item.image}" alt="${item.title}">` : '<div class="placeholder-card compact">No image</div>'}
                <div>
                    <button class="cart-line__remove" type="button" data-remove-cart-item="${item.id}" aria-label="O'chirish">
                        <i class="bi bi-x-lg"></i>
                    </button>
                    <strong>${item.title}</strong>
                    <p>Miqdor: ${item.quantity}</p>
                    <span>$${item.price}</span>
                </div>
            </article>
        `).join("");
        bindCartRemoveButtons();
    } catch (error) {
        cartItemsNode.innerHTML = '<p class="empty-state">Savatni yuklab bo‘lmadi.</p>';
    }
}

async function removeCartItem(itemId) {
    const response = await fetch(`/orders/remove/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
            "X-Requested-With": "XMLHttpRequest",
        },
    });

    if (!response.ok) return;
    await loadCart();
}

function bindCartRemoveButtons() {
    document.querySelectorAll("[data-remove-cart-item]").forEach((button) => {
        button.addEventListener("click", () => {
            removeCartItem(button.dataset.removeCartItem);
        });
    });
}

async function addToCart(productId, quantity, button) {
    if (!isAuthenticated) {
        window.location.href = "/user/login/";
        return;
    }

    const formData = new FormData();
    formData.append("product_id", productId);
    formData.append("quantity", quantity);

    const response = await fetch("/orders/add/to/cart/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
    });

    if (!response.ok) {
        setButtonState(button, "Xatolik");
        return;
    }

    setButtonState(button, "Qo'shildi");
    await loadCart();
    openCart();
}

async function toggleSaved(productId, button) {
    if (!isAuthenticated) {
        window.location.href = "/user/login/";
        return;
    }

    const response = await fetch(`/add/to/saved/${productId}/`, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
    });

    if (!response.ok) {
        setButtonState(button, "Xatolik");
        return;
    }

    const text = (await response.text()).trim();
    setButtonState(button, text);
}

document.querySelectorAll("[data-add-to-cart]").forEach((button) => {
    button.addEventListener("click", () => {
        const productId = button.dataset.productId;
        const source = button.dataset.quantitySource;
        const quantity = source
            ? document.querySelector(source)?.value || 1
            : button.dataset.quantity || 1;
        addToCart(productId, quantity, button);
    });
});

document.querySelectorAll("[data-toggle-saved]").forEach((button) => {
    button.addEventListener("click", () => {
        toggleSaved(button.dataset.productId, button);
    });
});

const productCards = document.querySelectorAll("[data-product-card]");
const params = new URLSearchParams(window.location.search);
const searchQuery = (params.get("q") || "").trim().toLowerCase();
const selectedCategory = (params.get("category") || "").trim().toLowerCase();

if (productCards.length && (searchQuery || selectedCategory)) {
    productCards.forEach((card) => {
        const title = card.dataset.title || "";
        const category = card.dataset.category || "";
        const matchesSearch = !searchQuery || title.includes(searchQuery);
        const matchesCategory = !selectedCategory || category === selectedCategory;
        card.style.display = matchesSearch && matchesCategory ? "" : "none";
    });
}

if (cartOpenButton) {
    cartOpenButton.addEventListener("click", async () => {
        await loadCart();
        openCart();
    });
}

if (cartCloseButton) {
    cartCloseButton.addEventListener("click", closeCart);
}

if (cartBackdrop) {
    cartBackdrop.addEventListener("click", closeCart);
}

if (isAuthenticated) {
    loadCart();
}

function dismissToast(toast) {
    if (!toast || toast.dataset.closing === "true") return;
    toast.dataset.closing = "true";
    toast.classList.add("is-leaving");
    window.setTimeout(() => {
        toast.remove();
    }, 220);
}

document.querySelectorAll("[data-toast]").forEach((toast) => {
    const closeButton = toast.querySelector("[data-toast-close]");
    const timeoutId = window.setTimeout(() => {
        dismissToast(toast);
    }, 3000);

    if (closeButton) {
        closeButton.addEventListener("click", () => {
            window.clearTimeout(timeoutId);
            dismissToast(toast);
        });
    }
});
