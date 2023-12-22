document.getElementById('send-btn').addEventListener('click', function() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message) {
        var messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML += '<p>' + message + '</p>';
        input.value = '';
    }
});
