$('#newPostButton').click(function () {
    $('#newPostModal')
        .modal({
            blurring: true
        })
        .modal('show')
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
            $('#newPostForm')[0].reset()
        })
        .fail(function () {
            console.error("Post failed!")
            alert("投稿に失敗しました。しばらくしてからやり直してください。")
        })
        .always(function () {
            $('#postSubmit').removeClass("disabled loading")
        })
})
