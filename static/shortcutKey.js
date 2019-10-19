$(document).keydown(function (e) {
    if (document.activeElement.toString() != "[object HTMLTextAreaElement]" || document.activeElement.classList.contains("enableShortcutKey") == true) {
        if (document.activeElement.toString() != "[object HTMLInputElement]" || document.activeElement.classList.contains("enableShortcutKey") == true) {
            switch (e.keyCode) {
                case 78:
                    // Key: N
                    if (document.activeElement.classList.contains("enableShortcutKey") == false && window.IS_LOGIN != false) {
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
                    if (window.IS_LOGIN == true) {
                        if(event.ctrlKey && window.isNewPostModalActive == true) {
                            $('#postSubmit').click();
                            return false
                        } else if (event.ctrlKey && window.isNewPostModalActive == false) {
                            $('#postIndexSubmit').click();
                            return false
                        }
                    }
                    break;
            }
        }
    }
})
