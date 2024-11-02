async function renderRunningScraperProcesses() {
    const apiData = await getData("/api/running-scraping-tasks");
    const processesData = apiData.processes_data;

    const mainContentContainer = document.getElementById("scraper-processes-container");
    mainContentContainer.innerHTML = "";

    if (processesData.length > 0) {
        let processesContainer = createProcessesContainer();
        mainContentContainer.appendChild(processesContainer);

        const processesWrapper = document.getElementById("running-processes-container");

        for (let data of processesData) {
            let processContainer = createProcessContainer(data);
            processesWrapper.appendChild(processContainer);
        }
    }
}


function createProcessesContainer() {
    let container = document.createElement("div");
    container.classList.add("running-processes-wrapper");

    let containerHeader = document.createElement("div");
    containerHeader.classList.add("running-processes-title")
    containerHeader.innerHTML = "Running Processes";

    let processesWrapper = document.createElement("div");
    processesWrapper.classList.add("running-processes-container");
    processesWrapper.id = "running-processes-container"

    container.appendChild(containerHeader);
    container.appendChild(processesWrapper);

    return container;
}


function createProcessContainer(processData) {
    let container = document.createElement("div");
    container.classList.add("running-process-container");

    let processTitle = document.createElement("div");
    processTitle.classList.add("running-process-name")
    processTitle.innerHTML = processData.work_title;

    let processProgress = document.createElement("div");
    processProgress.classList.add("running-process-progress")
    processProgress.innerHTML = processData.progress + "%";

    container.appendChild(processTitle);
    container.appendChild(processProgress);

    return container;
}
