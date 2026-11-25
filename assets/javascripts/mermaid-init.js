(function () {
  function currentTheme() {
    var scheme = document.body && document.body.getAttribute("data-md-color-scheme");
    return scheme === "slate" ? "dark" : "default";
  }

  function renderMermaid() {
    if (typeof mermaid === "undefined") return;
    var nodes = document.querySelectorAll(".mermaid");
    if (!nodes.length) return;
    nodes.forEach(function (el) {
      if (!el.dataset.mermaidSrc) {
        el.dataset.mermaidSrc = el.textContent;
      } else {
        el.removeAttribute("data-processed");
        el.textContent = el.dataset.mermaidSrc;
      }
    });
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: currentTheme(),
    });
    mermaid.run({ nodes: nodes });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderMermaid();
    if (document.body && typeof MutationObserver !== "undefined") {
      var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          if (mutations[i].attributeName === "data-md-color-scheme") {
            renderMermaid();
            break;
          }
        }
      });
      observer.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
    }
  });
})();
