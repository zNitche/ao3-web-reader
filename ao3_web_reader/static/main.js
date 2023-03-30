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
