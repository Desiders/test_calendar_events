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

function deleteCalendarEvent() {
    const form = document.getElementById("delete-calendar-event-form");
    
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

        fetch(path, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        }).then((response) => {
            if (response.status === 204) {
                console.log("Event has been deleted.");

                const path = `${window.location.protocol}//${window.location.host}/`;

                window.location.href = path;
            } else if (response.status === 401) {
                console.log("User is not logged in or token is invalid.");

                alert(
                    "You must be logged in to delete a calendar event.\n" +
                    "If you already have an account, please log in again.\n" +
                    "Otherwise, please register for an account."
                );

                const path = `${window.location.protocol}//${window.location.host}/auth/register`;

                window.location.href = path;
            } else if (response.status === 403) {
                console.log("User is forbidden to delete the calendar event.");

                alert("Calendar event is not owned by you. You can't delete it.");
            } else {
                console.log(`Unknown status code: ${response.status}`);
            }
        });
    });
}

window.addEventListener("load", deleteCalendarEvent)
