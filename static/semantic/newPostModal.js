$('#newPostButton').click(function () {
    $('#newPostModal')
        .modal({
            closable: false
        })
        .modal('show')
    window.isNewPostModalActive = true;
})

$('#postSubmit').click(function () {
    $('#postSubmit').addClass("disabled loading")
    var postFormValue = $('#newPostForm').serialize()
    var postTarget = $('#newPostForm').attr('action')
    $.post(postTarget, postFormValue)
        .done(function (data) {
            console.info("Post complete!")
            console.info(data)
            $('#newPostModal').modal('hide')
            window.isNewPostModalActive = false;
            $('#newPostForm')[0].reset()
            $.uiAlert({
                textHead: '投稿に成功しました。',
                text: '',
                bgcolor: '#19c3aa',
                textcolor: '#fff',
                position: 'bottom-left',
                icon: 'checkmark box',
                time: 3,
            })
        })
        .fail(function (jqXHR) {
            try {
                var res = JSON.parse(jqXHR.responseText)
                console.error("Post failed!: " + res.error.msg)
                $.uiAlert({
                    textHead: '投稿できません。',
                    text: res.error.msg,
                    bgcolor: '#DB2828',
                    textcolor: '#fff',
                    position: 'bottom-left',
                    icon: 'remove circle',
                    time: 5,
                })
            } catch (error) {
                $.uiAlert({
                    textHead: '投稿できません。',
                    text: '不明なエラー',
                    bgcolor: '#DB2828',
                    textcolor: '#fff',
                    position: 'bottom-left',
                    icon: 'remove circle',
                    time: 5,
                })
            }
        })
        .always(function () {
            $('#postSubmit').removeClass("disabled loading")
        })
})
