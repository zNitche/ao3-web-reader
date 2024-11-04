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
