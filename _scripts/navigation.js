/* Accessible responsive navigation. */
{
  const initNavigation = () => {
    const header = document.querySelector(".site-header");
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.querySelector(".primary-navigation");
    if (!header || !toggle || !nav) return;

    const close = () => {
      header.removeAttribute("data-menu-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open navigation");
      document.body.classList.remove("nav-open");
    };

    const open = () => {
      header.setAttribute("data-menu-open", "");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close navigation");
      document.body.classList.add("nav-open");
    };

    toggle.addEventListener("click", () => {
      toggle.getAttribute("aria-expanded") === "true" ? close() : open();
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) close();
    });

    document.addEventListener("click", (event) => {
      if (!header.contains(event.target)) close();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") close();
    });

    const updateHeader = () => header.toggleAttribute("data-scrolled", window.scrollY > 12);
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
    window.matchMedia("(min-width: 901px)").addEventListener("change", close);
  };

  window.addEventListener("load", initNavigation);
}
