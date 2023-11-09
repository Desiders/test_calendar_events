function getToken() {
    for (const cookie of document.cookie.split(";")) {
        const [key, value] = cookie.split("=");

        if (decodeURIComponent(key.trim()) === "ACCESS_TOKEN") {
            const token = decodeURIComponent(value.trim());

            return token;
        }
    }
}

function getCalendarEvents() {
    console.log("Fetching calendar events...");

    const path = `${window.location.protocol}//${window.location.host}/api/calendar-events/`
    const token = getToken();

    fetch(path, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    }).then((response) => {
        if (response.status === 200) {
            console.log("Successfully fetched calendar events.");

            response.json().then((data) => {
                if (data.length === 0) {
                    console.log("No calendar events found.");

                    return;
                }

                const tableCalendarEvents = document.getElementById("calendar-events");

                data.forEach((calendarEvent) => {
                    title = calendarEvent.title;
                    description = calendarEvent.description || "Description not provided";
                    startDate = calendarEvent.startDate || "Start date not provided";
                    endDate = calendarEvent.endDate || "End date not provided";

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
            });
        } else if (response.status === 401) {
            console.log("User is not logged in or token is invalid.");

            alert(
                "You must be logged in to view this page. \
                If you already have an account, please log in again. \
                Otherwise, please register for an account."
            );

            const path = `${window.location.protocol}//${window.location.host}/auth/register`;

            window.location.href = path;
        }
    });
}

getCalendarEvents();