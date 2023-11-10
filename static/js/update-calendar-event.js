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

function updateCalendarEvent() {
    const form = document.getElementById("update-calendar-event-form");
    
    let pathname = window.location.pathname;
    if (pathname.endsWith("/")) {
        pathname = pathname.substring(0, pathname.length - 1);
    }
    const lastSlashIndex = pathname.lastIndexOf("/");
    const calendarEventId = pathname.substring(lastSlashIndex + 1);

    const path = `${window.location.protocol}//${window.location.host}/api/calendar-events/${calendarEventId}`;

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
            method: "PUT",
            body,
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        }).then((response) => {
            if (response.status === 204) {
                console.log("Event has been updated.");

                // Reload the page to show the updated event.
                window.location.reload();
            } else if (response.status === 401) {
                console.log("User is not logged in or token is invalid.");

                alert(
                    "You must be logged in to update a calendar event.\n" +
                    "If you already have an account, please log in again.\n" +
                    "Otherwise, please register for an account."
                );

                const path = `${window.location.protocol}//${window.location.host}/auth/register`;

                window.location.href = path;
            } else if (response.status === 403) {
                console.log("User is forbidden to update the calendar event.");

                alert("Calendar event is not owned by you. You can't update it.");
            } else {
                console.log(`Unknown status code: ${response.status}`);
            }
        });
    });
}

window.addEventListener("load", updateCalendarEvent)
