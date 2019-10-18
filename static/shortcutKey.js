$(document).keydown(function (e) {
    if (document.activeElement.toString() != "[object HTMLTextAreaElement]" || document.activeElement.classList.contains("enableShortcutKey") == true) {
        if (document.activeElement.toString() != "[object HTMLInputElement]" || document.activeElement.classList.contains("enableShortcutKey") == true) {
            switch (e.keyCode) {
                case 78:
                    // Key: N
                    if (document.activeElement.classList.contains("enableShortcutKey") == false) {
                        $('#newPostButton').click();
                    }
                    break;

                case 27:
                    // Key: [ESC]
                    if (window.isNewPostModalActive == true) {
                        $('#newPostModal')
                            .modal('hide')
                        window.isNewPostModalActive = false
                    }
                    break;

                case 13:
                    // Key: [ENTER]
                    if(event.ctrlKey && window.isNewPostModalActive == true) {
                        $('#postSubmit').click();
                        return false
                    }
                    break;
            }
        }
    }
})
