/////////////////////////
/**
 * Copyright :: Components
 */
/////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    const spanYear = document.getElementById('span-year');
    if (spanYear) {
        spanYear.innerHTML = new Date().getFullYear();
    }
});

/////////////////////////