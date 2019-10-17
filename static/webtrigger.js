function announce (uuid) {
    let csrf_token = window.CSRF_TOKEN
    let locate = window.ANNOUNCE_LOC
    $.uiAlert({
        textHead: '実装待ち',
        text: uuid,
        bgcolor: '#19c3aa',
        textcolor: '#fff',
        position: 'bottom-left',
        icon: 'checkmark box',
        time: 3,
    })
}

function favorite (uuid) {
    var csrf_token = window.CSRF_TOKEN
    var locate = window.FAVORITE_LOC
    $.uiAlert({
        textHead: '実装待ち',
        text: uuid,
        bgcolor: '#19c3aa',
        textcolor: '#fff',
        position: 'bottom-left',
        icon: 'checkmark box',
        time: 3,
    })
}
