window.onload = (_event) => {
    const form = document.getElementById("login-form");
    const path = `${window.location.protocol}//${window.location.host}/api/auth/login/`

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const body = new FormData(form)

        fetch(path, {
            method: "POST",
            body,
        }).then((response) => {
            if (response.status === 200) {
                console.log("User has been logged in.");

                response.json().then((data) => {
                    document.cookie = `ACCESS_TOKEN=${data.access_token}; path=/; SameSite=Strict; Domain=${window.location.hostname}`;

                    window.location.href = "/";
                });
            } else if (response.status === 401) {
                console.log("Invalid username or password.");

                alert("Invalid username or password.");

                // Clear the password field.
                document.getElementById("password").value = "";

                // Focus the login field.
                document.getElementById("login").focus();
            } else {
                console.log("Unknown status code");
            }
        });
    });
};