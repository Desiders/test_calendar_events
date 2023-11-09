function getToken() {
    for (const cookie of document.cookie.split(";")) {
        const [key, value] = cookie.split("=");

        if (decodeURIComponent(key.trim()) === "ACCESS_TOKEN") {
            const token = decodeURIComponent(value.trim());

            return token;
        }
    }
}

function isEmpty(value) {
    return value == null || value === "";
}

function addCalendarEvent() {
    const form = document.getElementById("add-calendar-event-form");
    const path = `${window.location.protocol}//${window.location.host}/api/calendar-events/`

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const token = getToken();
        const body = new FormData();

        body.append("title", form["title"].value)
        body.append("is_private", form["is-private"].checked);

        if (!isEmpty(form["description"].value)) {
            body.append("description", form["description"].value);
        }

        if (!isEmpty(form["start-date"].value)) {
            body.append("start_date", form["start-date"].value);
        }

        if (!isEmpty(form["end-date"].value)) {
            body.append("end_date", form["end-date"].value);
        }

        fetch(path, {
            method: "POST",
            body,
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        }).then((response) => {
            if (response.status === 201) {
                console.log("Event has been added.");

                // Reload the page to show the new event.
                window.location.reload();
            } else if (response.status === 401) {
                console.log("User is not logged in or token is invalid.");

                alert(
                    "You must be logged in to add a calendar event. \
                    If you already have an account, please log in again. \
                    Otherwise, please register for an account."
                );

                const path = `${window.location.protocol}//${window.location.host}/auth/register`;

                window.location.href = path;
            } else {
                console.log("Unknown status code");
            }
        });
    });
}

window.addEventListener("load", addCalendarEvent)
