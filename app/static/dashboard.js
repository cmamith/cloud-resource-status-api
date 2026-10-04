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

        await loadAIAnalysis(status);


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

async function loadAIAnalysis(status) {
    const severityElement =
        document.getElementById("ai-severity");

    const summaryElement =
        document.getElementById("ai-summary");

    const impactElement =
        document.getElementById("ai-impact");

    const recommendationsElement =
        document.getElementById(
            "ai-recommendations"
        );

    severityElement.textContent =
        "ANALYZING";

    severityElement.className =
        "overall-status loading";

    summaryElement.textContent =
        "Analyzing current platform status...";

    impactElement.textContent = "-";

    recommendationsElement.innerHTML = "";

    try {
        const response = await fetch(
            "/ai/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(status)
            }
        );

        if (!response.ok) {
            throw new Error(
                "AI analysis request failed"
            );
        }

        const analysis =
            await response.json();


        severityElement.textContent =
            analysis.severity.toUpperCase();

        severityElement.className =
            `overall-status ${analysis.severity}`;


        summaryElement.textContent =
            analysis.summary;


        impactElement.textContent =
            analysis.possible_impact;


        recommendationsElement.innerHTML =
            "";

        analysis.recommended_checks.forEach(
            check => {

                const item =
                    document.createElement("li");

                item.textContent = check;

                recommendationsElement
                    .appendChild(item);
            }
        );

    } catch (error) {

        console.error(
            "AI analysis failed",
            error
        );

        severityElement.textContent =
            "UNAVAILABLE";

        severityElement.className =
            "overall-status failed";

        summaryElement.textContent =
            "AI analysis is currently unavailable.";

        impactElement.textContent = "-";
    }
}

loadDashboard();