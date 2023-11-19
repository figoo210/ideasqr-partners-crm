let socket;

function connectWebSocket() {
    // Your WebSocket connection code
    socket = new WebSocket(document.getElementById("REALTIME_WEBSOCKET_URL").value);

    // Handle socket close event
    socket.onclose = function (event) {
        console.log("WebSocket connection closed:", event);

        // Reconnect after a delay (e.g., 3 seconds)
        setTimeout(function () {
            console.log("Reconnecting...");
            connectWebSocket();
        }, 3000);
    };

    // Handle socket error event
    socket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

}

connectWebSocket();

function fetchRealtimeData() {
    socket.send("get data");
}

// Data variables
let totalSubmissions = document.getElementById("totals");
let teamsNames = document.getElementById("teams");
let employeesData = document.getElementById("employeesData");

// Store previous data to compare for changes
let previousData = {};

// Handle received data from the server
socket.onmessage = function (event) {
    document.querySelector(".loader").style.display = "none";
    const data = JSON.parse(event.data);
    data.teams.sort((a, b) => b.total_submissions - a.total_submissions);
    // console.log(data);

    // Update Values
    totalSubmissions.innerHTML = totalSubmissions.innerHTML;
    teamsNames.innerHTML = teamsNames.innerHTML;
    employeesData.innerHTML = employeesData.innerHTML;

    let tsPot = "<th>Total Submissions</th>";
    let tnPot = "<th>Employees / Team Leader</th>";

    let allEmployees = [];

    for (let i = 0; i < data.teams.length; i++) {
        const element = data.teams[i];
        tsPot += `<td data-team="${element.team_leader}">${element.total_submissions}</td>`
        tnPot += `<th>${element.team_leader}</th>`

        allEmployees = allEmployees.concat(element.employees);
    }
    totalSubmissions.innerHTML = tsPot;
    teamsNames.innerHTML = tnPot;

    let edPot = "";
    allEmployees.sort((a, b) => b.number_of_submissions - a.number_of_submissions);
    for (let j = 0; j < allEmployees.length; j++) {
        const element = allEmployees[j];
        let row = `<tr><td>${element.employee_username}</td>`; // Start the row with username cell

        for (let k = 0; k < data.teams.length; k++) {
            const team = data.teams[k];
            const foundEmployee = team.employees.find(emp => emp.employee_username === element.employee_username);

            if (foundEmployee) {
                row += `<td data-username="${element.employee_username}" data-team="${team.team_leader}">${element.number_of_submissions}</td>`;
            } else {
                row += `<td style="background-color: #eee; opacity: 0.5;"></td>`;
            }
        }

        row += '</tr>';
        edPot += row;
    }

    employeesData.innerHTML = edPot;


    // Check if previous data exists and compare for changes
    if (Object.keys(previousData).length !== 0) {
        for (let i = 0; i < data.teams.length; i++) {
            const currentTeam = data.teams[i];
            const previousTeam = previousData.teams.find(
                prevTeam => prevTeam.team_leader === currentTeam.team_leader
            );

            if (previousTeam) {
                if (previousTeam.total_submissions < currentTeam.total_submissions) {
                    const totalCell = document.querySelector(`td[data-team="${currentTeam.team_leader}"]`);
                    if (totalCell) {
                        totalCell.style.backgroundColor = 'lightgreen';
                        setTimeout(() => {
                            totalCell.style.backgroundColor = '';
                        }, 3000);
                    }
                }

                for (let j = 0; j < currentTeam.employees.length; j++) {
                    const currentEmployee = currentTeam.employees[j];
                    const previousEmployee = previousTeam.employees.find(
                        prevEmp => prevEmp.employee_username === currentEmployee.employee_username
                    );

                    if (previousEmployee && currentEmployee.number_of_submissions > previousEmployee.number_of_submissions) {
                        // Highlight the cell for 3 seconds
                        const cell = document.querySelector(`td[data-username="${currentEmployee.employee_username}"][data-team="${currentTeam.team_leader}"]`);
                        if (cell) {
                            cell.style.backgroundColor = 'lightgreen';
                            setTimeout(() => {
                                cell.style.backgroundColor = '';
                            }, 3000);
                        }
                    }
                }
            }
        }
    }

    // Update previousData with the current data for the next comparison
    previousData = data;

};

// Fetch data every 5 seconds (adjust as needed)
setInterval(fetchRealtimeData, 4000);
