$(document).keydown(function (e) {
    switch (e.keyCode) {
        case 78:
            // Key: N
            $('#newPostButton').click();
            break;

        case 27:
            // Key: [ESC]
            if (window.isNewPostModalActive == true) {
                $('#newPostModal')
                    .modal('hide')
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
})
