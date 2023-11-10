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

function getCalendarEvents() {
    console.log("Fetching calendar event...");

    let pathname = window.location.pathname;
    if (pathname.endsWith("/")) {
        pathname = pathname.substring(0, pathname.length - 1);
    }
    const lastSlashIndex = pathname.lastIndexOf("/");
    const calendarEventId = pathname.substring(lastSlashIndex + 1);

    const path = `${window.location.protocol}//${window.location.host}/api/calendar-events/${calendarEventId}`;

    let headers = new Headers();

    const token = getToken();
    if (!isEmpty(token)) {
        headers.append("Authorization", `Bearer ${token}`);
    }

    fetch(path, {
        method: "GET",
        headers,
    }).then((response) => {
        if (response.status === 200) {
            console.log("Successfully fetched calendar events.");

            response.json().then((calendarEvent) => {
                const tableCalendarEvents = document.getElementById("calendar-event");

                const title = calendarEvent.title;
                const description = calendarEvent.description || "Description not provided";
                const startDate = calendarEvent.startDate || "Start date not provided";
                const endDate = calendarEvent.endDate || "End date not provided";

                const row = document.createElement("tr");

                const cellEvent = document.createElement("td");
                cellEvent.textContent = title;
                row.appendChild(cellEvent);

                const cellDescription = document.createElement("td");
                cellDescription.textContent = description;
                row.appendChild(cellDescription);

                const cellStartDate = document.createElement("td");
                cellStartDate.textContent = startDate;
                row.appendChild(cellStartDate);

                const cellEndDate = document.createElement("td");
                cellEndDate.textContent = endDate;
                row.appendChild(cellEndDate);

                tableCalendarEvents.appendChild(row);
            });
        } else if (response.status === 401) {
            console.log("User is not logged in or token is invalid.");

            alert(
                "You must be logged in to get a calendar event.\n" +
                "If you already have an account, please log in again.\n" +
                "Otherwise, please register for an account."
            );

            const path = `${window.location.protocol}//${window.location.host}/auth/register`;

            window.location.href = path;
        } else if (response.status === 403) {
            console.log("User is forbidden to view the calendar event.");

            alert("Calendar event is private. You can't access it.");

            const path = `${window.location.protocol}//${window.location.host}/`;

            window.location.href = path;
        } else {
            console.log(`Unknown status code: ${response.status}`);
        }
    });
}

getCalendarEvents();