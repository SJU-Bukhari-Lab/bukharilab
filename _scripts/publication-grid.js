(() => {
  const initializePublicationGrid = () => {
    const catalog = document.querySelector("#publication-catalog");
    const searchInput = document.querySelector("#publication-search");
    const yearSelect = document.querySelector("#publication-year");
    const categorySelect = document.querySelector("#publication-category");
    const resetButton = document.querySelector("#publication-reset");
    const resultCount = document.querySelector("#publication-results-count");
    const emptyState = document.querySelector("#publication-empty-state");

    if (
      !catalog ||
      !searchInput ||
      !yearSelect ||
      !categorySelect ||
      !resetButton ||
      !resultCount ||
      !emptyState
    ) {
      return;
    }

    const cards = Array.from(
      catalog.querySelectorAll(".publication-grid-card")
    );

    const years = Array.from(
      new Set(
        cards
          .map((card) => card.dataset.year)
          .filter((year) => year && year !== "Undated")
      )
    ).sort((a, b) => Number(b) - Number(a));

    const categories = Array.from(
      new Set(
        cards
          .map((card) => card.dataset.category)
          .filter(Boolean)
      )
    ).sort((a, b) => a.localeCompare(b));

    years.forEach((year) => {
      const option = document.createElement("option");
      option.value = year;
      option.textContent = year;
      yearSelect.append(option);
    });

    categories.forEach((category) => {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      categorySelect.append(option);
    });

    const update = () => {
      const query = searchInput.value.trim().toLowerCase();
      const selectedYear = yearSelect.value;
      const selectedCategory = categorySelect.value;
      let visibleCount = 0;

      cards.forEach((card) => {
        const matchesSearch =
          !query || (card.dataset.search || "").includes(query);
        const matchesYear =
          !selectedYear || card.dataset.year === selectedYear;
        const matchesCategory =
          !selectedCategory ||
          card.dataset.category === selectedCategory;
        const visible =
          matchesSearch && matchesYear && matchesCategory;

        card.hidden = !visible;

        if (visible) {
          visibleCount += 1;
        }
      });

      resultCount.textContent = `${visibleCount} ${
        visibleCount === 1 ? "publication" : "publications"
      }`;

      emptyState.hidden = visibleCount !== 0;

      resetButton.disabled =
        !query && !selectedYear && !selectedCategory;
    };

    const reset = () => {
      searchInput.value = "";
      yearSelect.value = "";
      categorySelect.value = "";
      update();
      searchInput.focus();
    };

    searchInput.addEventListener("input", update);
    yearSelect.addEventListener("change", update);
    categorySelect.addEventListener("change", update);
    resetButton.addEventListener("click", reset);

    update();
  };

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      initializePublicationGrid,
      { once: true }
    );
  } else {
    initializePublicationGrid();
  }
})();
