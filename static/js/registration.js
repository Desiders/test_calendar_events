window.onload = (_event) => {
    const form = document.getElementById("registration-form");
    const path = `${window.location.protocol}//${window.location.host}/api/auth/register/`

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const body = new FormData(form)

        fetch(path, {
            method: "POST",
            body,
        }).then((response) => {
            if (response.status === 201) {
                console.log("User has been registered.");

                response.json().then((data) => {
                    document.cookie = `ACCESS_TOKEN=${data.access_token}; path=/; SameSite=Strict; Domain=${window.location.hostname}`;

                    window.location.href = "/";
                });
            } else if (response.status === 409) {
                console.log("Username already exists.");

                alert("Username already exists.");

                // Clear the password field.
                document.getElementById("password").value = "";

                // Clear the confirm password field.
                document.getElementById("confirm-password").value = "";

                // Focus the username field.
                document.getElementById("login").focus();
            }
        });
    });
};