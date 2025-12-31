document.addEventListener("DOMContentLoaded", () => {

    async function login(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch("/login", {
                method: "POST",
                body: new URLSearchParams(data),
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                credentials: "include"
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const html = await response.text();
                document.body.innerHTML = html;
            }
        } catch (error) {
            console.error("Login error:", error);
        }
    }

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", login);
    }

    // Auto refresh token
    async function fetchWithRefresh(url, options = {}) {
        options.credentials = "include"; 
        let response = await fetch(url, options);

        if (response.status === 401) { 
            const refreshed = await refreshToken();
            if (refreshed) {
                response = await fetch(url, options);
            }
        }

        return response;
    }

    async function refreshToken() {
        console.log("refreshToken() called");

        try {
            console.log("Calling /refresh...");
            const response = await fetch("/refresh", {
                method: "POST",
                credentials: "include"
            });

            console.log("fetch /refresh returned", response.status);

            if (response.ok) {
                console.log("Token refreshed!");
                return true;
            } else {
                console.error("Failed to refresh token");
                window.location.href = "/login"; 
            }
        } catch (error) {
            console.error("Refresh token error:", error);
        }
    }

    async function logout() {
        try {
            const response = await fetch("/logout", {
                method: "POST",
                credentials: "include"
            });

            if (response.redirected) {
                window.location.href = response.url;
            }
        } catch (error) {
            console.error("Logout error:", error);
        }
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    }

    window.fetchWithRefresh = fetchWithRefresh;

});
