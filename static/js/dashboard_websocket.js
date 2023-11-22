
// Custom Charts

let socket;

function connectWebSocket() {
    // Your WebSocket connection code
    socket = new WebSocket(document.getElementById("DASHBOARD_WEBSOCKET_URL").value);

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


const teamsPerformanceColumnsChart = () => {
    socket.onopen = function (event) {
        socket.send("get data");
    };

    // get data
    let teamNames = [];
    let submissionData = [];

    let options = {
        series: [
            {
                name: "Submissions",
                data: submissionData,
            },
        ],
        chart: {
            height: 400, // Adjust the height as needed
            type: "bar",
        },
        plotOptions: {
            bar: {
                borderRadius: 10,
                dataLabels: {
                    position: "top", // top, center, bottom
                },
            },
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                return val;
            },
            offsetY: -20,
            style: {
                fontSize: "12px",
                colors: ["#304758"],
            },
        },

        xaxis: {
            categories: teamNames, // Use team names instead of months
            position: "bottom",
            axisBorder: {
                show: false,
            },
            tickPlacement: "on",
            axisTicks: {
                show: true,
            },
            crosshairs: {
                fill: {
                    type: "gradient",
                    gradient: {
                        colorFrom: "#D8E3F0",
                        colorTo: "#BED1E6",
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    },
                },
            },
            tooltip: {
                enabled: true,
            },
        },
        yaxis: {
            max: 2000,
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
            labels: {
                show: false,
                formatter: function (val) {
                    return val;
                },
            },
        },
        title: {
            text: "Number of Submissions by Teams",
            floating: false,
            offsetY: 0,
            align: "center",
            style: {
                color: "#444",
            },
        },
    };

    // const teamsPerSlide = 6;

    // Update the x-axis with the initial subset of teams
    // if (teamNames.length > teamsPerSlide) {
    //     options.xaxis.categories = teamNames.slice(0, teamsPerSlide);
    //     options.series[0].data = submissionData.slice(0, teamsPerSlide);
    // }

    let chart = new ApexCharts(
        document.querySelector("#submissionsChart"),
        options
    );

    // Handle received data from the server
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        teamNames = data.team_leaders;
        submissionData = data.submissions_data;
        options.xaxis.categories = teamNames;
        options.yaxis.max = Math.max(...submissionData) + (Math.max(...submissionData) * 0.5);
        console.log(options.yaxis.max);
        options.series[0].data = submissionData;
        chart.updateOptions(options);
    };

    chart.render();

    // Add a function to update the chart data for the next subset of teams
    // function updateChartData(startIndex) {
    //     const endIndex = startIndex + teamsPerSlide;
    //     let newTeamSubset;
    //     let newTeamSubmissions;
    //     if (endIndex <= (teamNames.length - 1)) {
    //         newTeamSubset = teamNames.slice(startIndex, endIndex);
    //         newTeamSubmissions = submissionData.slice(startIndex, endIndex);
    //     } else {
    //         newTeamSubset = teamNames.slice(startIndex, teamNames.length - 1).concat(teamNames.slice(0, endIndex - teamNames.length - 1));
    //         newTeamSubmissions = submissionData.slice(startIndex, teamNames.length - 1).concat(submissionData.slice(0, endIndex - teamNames.length - 1));
    //     }

    //     // Update x-axis categories
    //     teamNames.length > teamsPerSlide && chart.updateOptions({
    //         series: [
    //             {
    //                 name: "Submissions",
    //                 data: newTeamSubmissions,
    //             },
    //         ],
    //         xaxis: {
    //             categories: newTeamSubset,
    //         },
    //         yaxis: {
    //             max: Math.max(...submissionData) + (Math.max(...submissionData) * 0.5),
    //         },
    //         plotOptions: {
    //             bar: {
    //                 columnWidth: '50%', // Set a fixed column width as needed
    //             },
    //         },
    //     });
    // }

    // Add a timer to simulate the slider effect
    // let currentIndex = 0;
    setInterval(() => {
        // currentIndex = (currentIndex + teamsPerSlide) % teamNames.length;
        // updateChartData(currentIndex);
        socket.send("get data");
    }, 2000); // Adjust the interval as needed (in milliseconds)
};

teamsPerformanceColumnsChart();

