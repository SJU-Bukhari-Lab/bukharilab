/* Preserve hash navigation without adding link icons beside headings. */
{
  const scrollToTarget = () => {
    const id = window.location.hash.replace("#", "");
    const target = document.getElementById(id);
    if (!target) return;

    const header = document.querySelector("header");
    const offset = header ? header.clientHeight + 16 : 16;
    window.scrollTo({
      top: target.getBoundingClientRect().top + window.scrollY - offset,
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto"
        : "smooth",
    });
  };

  window.addEventListener("load", scrollToTarget);
  window.addEventListener("tagsfetched", scrollToTarget);
  window.addEventListener("hashchange", scrollToTarget);
}
