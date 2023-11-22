
// Realtime Datagrid

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
        // Perform any actions you need when there is an error with the WebSocket connection
    };

}

connectWebSocket();

let refreshTable = document.getElementById("refreshTable");

const chartTableCreation = () => {

    socket.onopen = function (event) {
        socket.send("get data");
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        // console.log(data);
        let tableData = []
        for (let i = 0; i < data.teams.length; i++) {
            const element = data.teams[i];
            for (let j = 0; j < element.employees.length; j++) {
                const emp = element.employees[j];
                emp["team_leader"] = element.team_leader;
                tableData.push(emp);
            }
        }
        refreshTable.innerHTML = "Refresh";
        let table = new Tabulator("#chartTable", {
            data: tableData,
            height: "500px",
            layout: "fitColumns",
            movableRows: false,
            groupBy: "team_leader",
            columns: [
                { title: "Employee Name", field: "employee_username", width: 200 },
                { title: "Today's Submissions", field: "number_of_today_submissions", sorter: "number" },
                { title: "Week's Submissions", field: "number_of_week_submissions", sorter: "number" },
                { title: "Month's Submissions", field: "number_of_month_submissions", sorter: "number" },
                { title: "Total Submissions", field: "number_of_submissions", sorter: "number", sorterParams: { sortDirection: "desc" } },
                // { title: "Team Leader", field: "team_leader", hozAlign: "center" },
            ],
        });
    }
};

chartTableCreation();

refreshTable.addEventListener("click", event => {
    refreshTable.innerHTML = `<div class="customLoader"></div>`;
    socket.send("get data");
});
