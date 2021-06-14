/** Advanced Blob Host script */
let saveAdvancedBlobHostData = function() {
    return new FormData($($("#modal-" + moduleElement[0].id)[0]).find(".advanced-blob-host-form")[0]);
};

let advancedBlobHostPopupOptions = {
    title: "Select a file",
    getData: saveAdvancedBlobHostData
}

// FIXME: update url?
configurePopUp('module-advanced-blob-host', advancedBlobHostPopupOptions);
