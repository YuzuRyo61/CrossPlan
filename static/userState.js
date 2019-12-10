function openUserMuteModal() {
    $('#userMuteConfirm')
        .modal({
            onApprove: function () {
                sendState('mute')
            }
        })
        .modal('show')
}

function openUserBlockModal() {
    $('#userBlockConfirm')
        .modal({
            onApprove: function () {
                sendState('block')
            }
        })
        .modal('show')
}

function sendState(state) {
    $(".stateActionBtn").addClass("disabled loading")
    document.getElementById("changeState").value = state
    var userStateForm = $("#userStateForm").serialize()
    var postTarget = $("#userStateForm").attr('action')
    $.post(postTarget, userStateForm)
        .done(function (data) {
            $.uiAlert({
                textHead: '受諾されました。',
                text: state,
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
                $.uiAlert({
                    textHead: 'エラー',
                    text: res.error.msg,
                    bgcolor: '#DB2828',
                    textcolor: '#fff',
                    position: 'bottom-left',
                    icon: 'remove circle',
                    time: 5,
                })
            } catch (error) {
                $.uiAlert({
                    textHead: 'エラー',
                    text: '不明なエラーが発生しました。',
                    bgcolor: '#DB2828',
                    textcolor: '#fff',
                    position: 'bottom-left',
                    icon: 'remove circle',
                    time: 5,
                })
            }
        })
        .always(function () {
            $('.stateActionBtn').removeClass("disabled loading")
        })
}
