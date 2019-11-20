function announce (uuid, elem) {
    if (!$(elem).attr('disabled')) {
        var uidv = document.cp_posts.elements['target']
        uidv.value = uuid
        let formValue = $('#cp_posts').serialize()
        let locate = window.ANNOUNCE_LOC
        $.post(locate, formValue)
            .done(function (data) {
                $.uiAlert({
                    textHead: 'アナウンスしました。',
                    text: uuid,
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
                        textHead: 'アナウンスできません。',
                        text: res.error.msg,
                        bgcolor: '#DB2828',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'remove circle',
                        time: 5,
                    })
                } catch (error) {
                    $.uiAlert({
                        textHead: 'アナウンスできません。',
                        text: '不明なエラー',
                        bgcolor: '#DB2828',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'remove circle',
                        time: 5,
                    })
                }
            })
    }
}

function favorite (uuid, elem) {
    if (!$(elem).attr('disabled')) {
        var uidv = document.cp_posts.elements['target']
        uidv.value = uuid
        let formValue = $('#cp_posts').serialize()
        let locate = window.FAVORITE_LOC
        $.post(locate, formValue)
            .done(function (data) {
                if (data.liked == true) {
                    $.uiAlert({
                        textHead: 'いいねしました。',
                        text: uuid,
                        bgcolor: '#19c3aa',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'checkmark box',
                        time: 3,
                    })
                } else {
                    $.uiAlert({
                        textHead: 'いいね解除しました。',
                        text: uuid,
                        bgcolor: '#19c3aa',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'checkmark box',
                        time: 3,
                    })
                }
            })
            .fail(function (jqXHR) {
                try {
                    var res = JSON.parse(jqXHR.responseText)
                    $.uiAlert({
                        textHead: 'いいねできません。',
                        text: res.error.msg,
                        bgcolor: '#DB2828',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'remove circle',
                        time: 5,
                    })
                } catch (error) {
                    $.uiAlert({
                        textHead: 'いいねできません。',
                        text: '不明なエラー',
                        bgcolor: '#DB2828',
                        textcolor: '#fff',
                        position: 'bottom-left',
                        icon: 'remove circle',
                        time: 5,
                    })
                }
            })
    }
}
