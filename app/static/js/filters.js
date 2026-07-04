document.addEventListener("DOMContentLoaded", function () {
    const pills = document.querySelectorAll(".filter-pill");

    pills.forEach(function (pill) {
        pill.addEventListener("click", function (e) {
            e.stopPropagation();
            const panel = document.getElementById(pill.dataset.panel);
            const isOpen = panel.classList.contains("open");

            // Close all panels first
            document.querySelectorAll(".filter-panel").forEach(function (p) {
                p.classList.remove("open");
            });

            // Open this one if it was not already open
            if (!isOpen) {
                panel.classList.add("open");
            }
        });
    });

    // Clicking outside closes any open panel
    document.addEventListener("click", function (e) {
        if (!e.target.closest(".filter-pill-wrap")) {
            document.querySelectorAll(".filter-panel").forEach(function (p) {
                p.classList.remove("open");
            });
        }
    });
});