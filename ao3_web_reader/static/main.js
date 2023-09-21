function fallbackToLocalFileLink(el, localPath) {
    el.href = localPath;
}


function fallbackToLocalJS(el, localPath) {
    document.write("<script src=" + localPath + "></script>");
}


function showRemoveModal(modalID, itemName, actionURL) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("remove-modal-item-name").innerHTML = itemName;
    document.getElementById("remove-modal-form").action = actionURL;

    modal.show();
}


function showChaptersCompletionModal(modalID, text, actionURL) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("chapter-completion-modal-text").innerHTML = text;
    document.getElementById("chapters-completion-form").action = actionURL;

    modal.show();
}


function showWorkFavoriteToggleModal(modalID, text, actionURL) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("work-favorite-modal-text").innerHTML = text;
    document.getElementById("work-favorite-form").action = actionURL;

    modal.show();
}


function updateCloudSyncIcon() {
    getData("/api/sync_status").then((data) => {
      if (data.is_running) {
        document.getElementById("sync-container").classList.remove("d-none");
        document.getElementById("sync-progress").innerHTML = data.progress + "%";
      }
      else {
        document.getElementById("sync-container").classList.add("d-none");
      }
    });
}


function toggleChapterCompletion(completedMessage, incompleteMessage, toggleULR) {
    postData(toggleULR);

    let message = "";
    const completionButton = document.getElementById("toggle-chapter-completion-button");

    if (completionButton.innerHTML.trim() == completedMessage) {
        message = incompleteMessage;
    } else {
        message = completedMessage;
    }

    completionButton.innerHTML = message;
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

    return response.json();
}
