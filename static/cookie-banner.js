document.addEventListener('DOMContentLoaded', function () {
    if (!localStorage.getItem('cookie-accepted')) {
        const banner = document.createElement('div');
        banner.className = 'fixed bottom-0 left-0 right-0 bg-gray-800 text-white p-4 text-center';
        banner.innerHTML = `
            <p>This website uses cookies to ensure you get the best experience on our website. 
            <a href="/privacy-policy.html" class="underline">Learn more</a>
            <button id="accept-cookies" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4">
                Accept
            </button>
            `;
        document.body.appendChild(banner);

        document.getElementById('accept-cookies').addEventListener('click', function () {
            localStorage.setItem('cookie-accepted', 'true');
            banner.style.display = 'none';
        });
    }
});