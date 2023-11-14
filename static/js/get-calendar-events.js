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

    const api_path = `${window.location.protocol}//${window.location.host}/api/calendar-events/`
    const public_path = `${window.location.protocol}//${window.location.host}/calendar-events/`;
    const token = getToken();

    fetch(api_path, {
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
                    let title = calendarEvent["title"];
                    let description = calendarEvent["description"] || "Not specified";
                    const startDate = calendarEvent["start_date"] || "Not specified";
                    const endDate = calendarEvent["end_date"] || "Not specified";
                    const url = `${public_path}${calendarEvent.id}`;

                    if (title.length > 30) {
                        title = `${title.substring(0, 30)}...`;
                    }

                    if (description.length > 50) {
                        description = `${description.substring(0, 50)}...`;
                    }

                    const row = document.createElement("tr");

                    const cellEvent = document.createElement("td");
                    const cellEventLink = document.createElement("a");
                    cellEventLink.href = url;
                    cellEventLink.textContent = title;
                    cellEventLink.style.color = "blue";
                    
                    cellEvent.appendChild(cellEventLink);
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
                "You must be logged in to view calendar events.\n" +
                "If you already have an account, please log in again.\n" +
                "Otherwise, please register for an account."
            );

            const path = `${window.location.protocol}//${window.location.host}/auth/register`;

            window.location.href = path;
        } else {
            console.log(`Unknown status code: ${response.status}`);
        }
    });
}

getCalendarEvents();