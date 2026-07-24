/* Manages light and dark mode with resilient localStorage access. */
(() => {
  const STORAGE_KEY = "dark-mode";

  const readSavedMode = () => {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      console.warn("Dark-mode preference could not be read.", error);
      return null;
    }
  };

  const saveMode = (value) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch (error) {
      console.warn("Dark-mode preference could not be saved.", error);
    }
  };

  const preferredMode = readSavedMode();
  document.documentElement.dataset.dark = preferredMode ?? "false";

  window.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".dark-toggle");
    if (toggle instanceof HTMLInputElement) {
      toggle.checked = document.documentElement.dataset.dark === "true";
    }
  });

  window.onDarkToggleChange = (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) return;

    const value = String(target.checked);
    document.documentElement.dataset.dark = value;
    saveMode(value);
  };
})();
