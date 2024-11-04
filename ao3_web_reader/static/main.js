function fallbackToLocalFileLink(el, localPath) {
    el.href = localPath;
}


function fallbackToLocalJS(el, localPath) {
    document.write("<script src=" + localPath + "></script>");
}


function updateCloudSyncIcon() {
    getData("/api/sync-status").then((data) => {
      if (data.is_running) {
        document.getElementById("sync-container").classList.remove("d-none");
        document.getElementById("sync-progress").innerHTML = data.progress + "%";
      }
      else {
        document.getElementById("sync-container").classList.add("d-none");
      }
    });
}


async function toggleChapterCompletion(completedMessage, incompleteMessage, toggleURL) {
    const res = await postData(toggleURL);
    const completionButton = document.getElementById("toggle-chapter-completion-button");

    completionButton.innerHTML = res.body.status === true ? completedMessage : incompleteMessage;
}


async function getData(url) {
    const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }

    const response = await fetch(url, options);

    return response.json();
}


async function postData(url, data={}) {
    const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        }

    const response = await fetch(url, options);
    const body = await response.json()

    return {status: response.status, body};
}
