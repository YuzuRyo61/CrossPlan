function sendState(state) {
    document.getElementById("changeState").value = state
    var userStateForm = $("#userStateForm").serialize()
    var postTarget = $("#userStateForm").attr('action')
    $.post(postTarget, userStateForm)
        .done(function (data) {
            $.uiAlert({
                textHead: '受諾されました。',
                text: '',
                bgcolor: '#19c3aa',
                textcolor: '#fff',
                position: 'bottom-left',
                icon: 'checkmark box',
                time: 3,
            })
        })
        .fail(function (jqXHR) {
            var res = JSON.parse(jqXHR.responseText)
            $.uiAlert({
                textHead: 'エラー',
                text: res.error.msg,
                bgcolor: '#DB2828',
                textcolor: '#fff',
                position: 'bottom-left',
                icon: 'remove circle',
                time: 5,
            })
        })
        .always(function () {

        })
}
