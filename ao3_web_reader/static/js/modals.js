function showRunLongRunningTaskModal(modalId, actionUrl) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    document.getElementById("run-long-running-task-form").action = actionUrl;

    modal.show();
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

function showExportWorkObjectModal(workId) {
    const modalElem = document.getElementById("exportWorkObjectModal");
    let modal = new bootstrap.Modal(modalElem);

    let items = modalElem.getElementsByTagName("a");

    for (const item of items) {
        item.href = item.href.replace("WORK_ID", workId);
    }

    modal.show();
}
