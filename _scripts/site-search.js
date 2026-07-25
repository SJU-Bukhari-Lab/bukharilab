/* Site search component. Searches the current domain through Google. */
(() => {
  window.onSiteSearchSubmit = (event) => {
    event.preventDefault();

    const queryInput = event.currentTarget?.elements?.query;
    const query = queryInput?.value?.trim();

    if (!query) {
      queryInput?.focus();
      return;
    }

    const params = new URLSearchParams({
      q: `site:${window.location.hostname} ${query}`,
    });

    window.location.assign(`https://www.google.com/search?${params.toString()}`);
  };
})();
