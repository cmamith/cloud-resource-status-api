function updateStatus(service, value) {
    const element = document.getElementById(
        `${service}-status`
    );

    element.textContent = value.toUpperCase();
    element.className = `status ${value}`;
}


function updateOverallStatus(status) {
    const serviceStates = [
        status.ec2,
        status.rds,
        status.eks
    ];

    const unhealthyCount = serviceStates.filter(
        state => state !== "healthy"
    ).length;

    const overallStatus =
        document.getElementById("overall-status");

    const overallDetail =
        document.getElementById("overall-detail");


    if (unhealthyCount === 0) {
        overallStatus.textContent = "HEALTHY";

        overallStatus.className =
            "overall-status healthy";

        overallDetail.textContent =
            "All services operational";
    } else {
        overallStatus.textContent = "DEGRADED";

        overallStatus.className =
            "overall-status degraded";

        overallDetail.textContent =
            `${unhealthyCount} ${
                unhealthyCount === 1
                    ? "service"
                    : "services"
            } unhealthy`;
    }
}


async function loadDashboard() {
    try {
        const statusResponse =
            await fetch("/platform-status");

        const status =
            await statusResponse.json();

        updateStatus("ec2", status.ec2);
        updateStatus("rds", status.rds);
        updateStatus("eks", status.eks);

        updateOverallStatus(status);


        const instanceResponse =
            await fetch("/instances");

        const instances =
            await instanceResponse.json();

        const table =
            document.getElementById("instance-table");

        table.innerHTML = "";

        instances.forEach(instance => {
            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td class="resource-id">
                    ${instance.instance_id}
                </td>

                <td>
                    ${instance.region}
                </td>

                <td>
                    <span class="instance-state ${instance.state}">
                        ${instance.state}
                    </span>
                </td>
            `;

            table.appendChild(row);
        });


        document.getElementById(
            "instance-count"
        ).textContent =
            `${instances.length} resources`;


        document.getElementById(
            "last-updated"
        ).textContent =
            new Date().toLocaleTimeString();

    } catch (error) {
        console.error(
            "Dashboard refresh failed",
            error
        );
    }
}


loadDashboard();