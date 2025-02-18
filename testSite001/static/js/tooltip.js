// ツールチップを有効化する関数
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ページ読み込み時にツールチップを適用
document.addEventListener("DOMContentLoaded", function () {
    initializeTooltips();
});

// Turbo（または Ajax）で動的に追加された要素にも適用
document.addEventListener("turbo:load", function () {
    initializeTooltips();
});
