const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.querySelector(".primary-nav");

if (navToggle && primaryNav) {
    navToggle.addEventListener("click", () => {
        const expanded = navToggle.getAttribute("aria-expanded") === "true";
        navToggle.setAttribute("aria-expanded", String(!expanded));
        primaryNav.classList.toggle("is-open");
    });
}

document.querySelectorAll("[data-catalog-dropdown]").forEach((catalogDropdown) => {
    const trigger = catalogDropdown.querySelector("[data-catalog-trigger]");
    const input = catalogDropdown.querySelector("[data-catalog-input]");
    const label = catalogDropdown.querySelector("[data-catalog-label]");
    const options = catalogDropdown.querySelectorAll("[data-catalog-option]");

    trigger?.addEventListener("click", () => {
        const isOpen = catalogDropdown.classList.toggle("is-open");
        trigger.setAttribute("aria-expanded", String(isOpen));
    });

    options.forEach((option) => {
        option.addEventListener("click", () => {
            options.forEach((item) => item.classList.remove("is-active"));
            option.classList.add("is-active");
            if (input) input.value = option.dataset.value || "";
            const optionText = option.querySelector("span")?.textContent?.trim() || option.textContent.trim();
            if (label) label.textContent = optionText;
            catalogDropdown.classList.remove("is-open");
            trigger?.setAttribute("aria-expanded", "false");

            if (catalogDropdown.dataset.submitOnSelect === "true") {
                catalogDropdown.closest("form")?.submit();
            }
        });
    });

    document.addEventListener("click", (event) => {
        if (!catalogDropdown.contains(event.target)) {
            catalogDropdown.classList.remove("is-open");
            trigger?.setAttribute("aria-expanded", "false");
        }
    });
});

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
const clearCartButton = document.querySelector("[data-clear-cart]");
const checkoutOpenButton = document.querySelector("[data-open-checkout]");
const checkoutModal = document.querySelector("[data-checkout-modal]");
const checkoutForm = document.querySelector("[data-checkout-form]");
const checkoutSubmitButton = document.querySelector("[data-checkout-submit]");
const cashModal = document.querySelector("[data-cash-modal]");
const cashForm = document.querySelector("[data-cash-form]");
const cashSubmitButton = document.querySelector("[data-cash-submit]");
const balanceAmountNode = document.querySelector("[data-balance-amount]");

function formatSensitiveValue(type, value, hidden = true) {
    const raw = String(value || "");

    if (!raw) {
        return type === "card" ? "**** **** **** ****" : "***";
    }

    if (!hidden) {
        if (type === "card") {
            return raw.replace(/\D/g, "").replace(/(.{4})/g, "$1 ").trim();
        }
        return raw;
    }

    if (type === "card") {
        const digits = raw.replace(/\D/g, "");
        const last = digits.slice(-4);
        return `**** **** **** ${last || "****"}`;
    }

    return "***";
}

function openCashModal() {
    if (!cashModal) return;
    cashModal.classList.add("is-open");
    cashModal.setAttribute("aria-hidden", "false");
}

function closeCashModal() {
    if (!cashModal) return;
    cashModal.classList.remove("is-open");
    cashModal.setAttribute("aria-hidden", "true");
}

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

function openCheckout() {
    if (!checkoutModal) return;
    checkoutModal.classList.add("is-open");
    checkoutModal.setAttribute("aria-hidden", "false");
}

function closeCheckout() {
    if (!checkoutModal) return;
    checkoutModal.classList.remove("is-open");
    checkoutModal.setAttribute("aria-hidden", "true");
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
            if (clearCartButton) {
                clearCartButton.dataset.cardId = "";
                clearCartButton.disabled = true;
            }
            if (checkoutOpenButton) {
                checkoutOpenButton.disabled = true;
            }
            return;
        }

        if (clearCartButton) {
            clearCartButton.dataset.cardId = data.cart_items[0].card_id || "";
            clearCartButton.disabled = false;
        }
        if (checkoutOpenButton) {
            checkoutOpenButton.dataset.cardId = data.cart_items[0].card_id || "";
            checkoutOpenButton.disabled = false;
        }

        cartItemsNode.innerHTML = data.cart_items.map((item) => `
            <article class="cart-line">
                ${item.image ? `<img src="${item.image}" alt="${item.title}">` : '<div class="placeholder-card compact">No image</div>'}
                <div>
                    <div class="cart-line__top">
                        <strong>${item.title}</strong>
                        <button class="cart-line__remove" type="button" data-remove-cart-item="${item.id}" aria-label="O'chirish">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    <div class="cart-line__qty">
                        <button type="button" data-decrease-cart-item="${item.id}" aria-label="Kamaytirish">
                            <i class="bi bi-dash-lg"></i>
                        </button>
                        <span>${item.quantity}</span>
                        <button type="button" data-increase-cart-item="${item.product_id}" aria-label="Ko'paytirish">
                            <i class="bi bi-plus-lg"></i>
                        </button>
                    </div>
                    <span>$${item.price}</span>
                </div>
            </article>
        `).join("");
        bindCartDrawerButtons();
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

async function decreaseCartItem(itemId) {
    const formData = new FormData();
    formData.append("quantity", "1");

    const response = await fetch(`/orders/decrease/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
    });

    if (!response.ok) return;
    await loadCart();
}

async function increaseCartItem(productId) {
    if (!productId) return;
    await addToCart(productId, 1);
}

async function clearCart(cardId) {
    if (!cardId) return;

    const response = await fetch(`/orders/clear/${cardId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
            "X-Requested-With": "XMLHttpRequest",
        },
    });

    if (!response.ok) return;
    await loadCart();
}

async function createOrder(address, cardId) {
    const formData = new FormData();
    formData.append("address", address);

    const response = await fetch("/orders/create_order/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
    });

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok || !data || String(data.status).startsWith("4")) {
        throw new Error(data?.message || "Buyurtma yaratib bo'lmadi.");
    }

    if (cardId) {
        await clearCart(cardId);
    }

    return data;
}

function bindCartDrawerButtons() {
    bindCartRemoveButtons();

    document.querySelectorAll("[data-decrease-cart-item]").forEach((button) => {
        button.addEventListener("click", () => {
            decreaseCartItem(button.dataset.decreaseCartItem);
        });
    });

    document.querySelectorAll("[data-increase-cart-item]").forEach((button) => {
        button.addEventListener("click", () => {
            increaseCartItem(button.dataset.increaseCartItem);
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

document.querySelectorAll(".product-media-rotator").forEach((media) => {
    const image = media.querySelector("img");
    const images = (media.dataset.images || "").split("||").filter(Boolean);
    if (!image || images.length < 2) return;

    let intervalId = null;
    let currentIndex = 0;
    const firstImage = images[0];

    media.addEventListener("mouseenter", () => {
        if (intervalId) return;
        intervalId = window.setInterval(() => {
            currentIndex = (currentIndex + 1) % images.length;
            image.src = images[currentIndex];
        }, 750);
    });

    media.addEventListener("mouseleave", () => {
        if (intervalId) {
            window.clearInterval(intervalId);
            intervalId = null;
        }
        currentIndex = 0;
        image.src = firstImage;
    });
});

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

if (clearCartButton) {
    clearCartButton.addEventListener("click", () => {
        clearCart(clearCartButton.dataset.cardId);
    });
}

if (checkoutOpenButton) {
    checkoutOpenButton.addEventListener("click", () => {
        openCheckout();
    });
}

document.querySelectorAll("[data-close-checkout]").forEach((button) => {
    button.addEventListener("click", closeCheckout);
});

if (checkoutModal) {
    checkoutModal.addEventListener("click", (event) => {
        if (event.target === checkoutModal) {
            closeCheckout();
        }
    });
}

if (checkoutForm) {
    checkoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const address = checkoutForm.elements.address?.value?.trim();
        const cardId = checkoutOpenButton?.dataset.cardId || clearCartButton?.dataset.cardId || "";

        if (!address) {
            if (checkoutSubmitButton) {
                setButtonState(checkoutSubmitButton, "Manzil kiriting");
            }
            return;
        }

        if (checkoutSubmitButton) {
            checkoutSubmitButton.disabled = true;
            checkoutSubmitButton.dataset.originalText = checkoutSubmitButton.textContent.trim();
            checkoutSubmitButton.textContent = "Yuborilmoqda...";
        }

        try {
            await createOrder(address, cardId);
            checkoutForm.reset();
            closeCheckout();
            closeCart();
            await loadCart();
            window.location.href = "/orders/my_orders/?new=1";
        } catch (error) {
            if (checkoutSubmitButton) {
                checkoutSubmitButton.textContent = error.message || "Xatolik";
                window.setTimeout(() => {
                    checkoutSubmitButton.textContent = checkoutSubmitButton.dataset.originalText || "Buyurtmani yaratish";
                }, 1800);
            }
        } finally {
            if (checkoutSubmitButton) {
                checkoutSubmitButton.disabled = false;
            }
        }
    });
}

document.querySelectorAll("[data-open-cash-modal]").forEach((button) => {
    button.addEventListener("click", openCashModal);
});

document.querySelectorAll("[data-close-cash-modal]").forEach((button) => {
    button.addEventListener("click", closeCashModal);
});

if (cashModal) {
    cashModal.addEventListener("click", (event) => {
        if (event.target === cashModal) {
            closeCashModal();
        }
    });
}

if (cashForm) {
    cashForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const endpoint = cashForm.dataset.endpoint;
        const amount = cashForm.elements.amount?.value?.trim();

        if (!amount) {
            return;
        }

        if (cashSubmitButton) {
            cashSubmitButton.disabled = true;
            cashSubmitButton.dataset.originalText = cashSubmitButton.textContent.trim();
            cashSubmitButton.textContent = "Yuborilmoqda...";
        }

        try {
            const formData = new FormData();
            formData.append("amount", amount);

            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken") || "",
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            });

            const data = await response.json();

            if (!response.ok || String(data.status).startsWith("4")) {
                throw new Error(data.message || "Balansni to‘ldirib bo‘lmadi.");
            }

            const nextAmount = data.amount ?? data.ammount ?? amount;
            if (balanceAmountNode) {
                balanceAmountNode.textContent = `$${nextAmount}`;
            }

            cashForm.reset();
            closeCashModal();
        } catch (error) {
            if (cashSubmitButton) {
                cashSubmitButton.textContent = error.message || "Xatolik";
                window.setTimeout(() => {
                    cashSubmitButton.textContent = cashSubmitButton.dataset.originalText || "To‘ldirish";
                }, 1800);
            }
        } finally {
            if (cashSubmitButton) {
                cashSubmitButton.disabled = false;
            }
        }
    });
}

document.querySelectorAll("[data-toggle-sensitive]").forEach((button) => {
    const container = button.closest(".bank-card__number, .bank-card__secure");
    const valueNode = container?.querySelector("[data-sensitive-value]");
    const icon = button.querySelector("i");

    if (!valueNode) return;

    const type = valueNode.dataset.sensitiveType || "card";
    valueNode.textContent = formatSensitiveValue(type, valueNode.dataset.sensitiveValue, true);

    button.addEventListener("click", () => {
        const isVisible = button.dataset.visible === "true";
        const nextVisible = !isVisible;
        button.dataset.visible = String(nextVisible);
        valueNode.textContent = formatSensitiveValue(type, valueNode.dataset.sensitiveValue, !nextVisible);
        if (icon) {
            icon.className = nextVisible ? "bi bi-eye-slash" : "bi bi-eye";
        }
    });
});

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

document.querySelectorAll("[data-sort-target]").forEach((radio) => {
    radio.addEventListener("change", () => {
        document.querySelectorAll("[data-sort-input]").forEach((input) => {
            input.value = "";
        });

        if (radio.checked) {
            const target = radio.dataset.sortTarget;
            const hiddenInput = document.querySelector(`[data-sort-input="${target}"]`);
            if (hiddenInput) {
                hiddenInput.value = "1";
            }
        }
    });
});
