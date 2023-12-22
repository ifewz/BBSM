document.getElementById('send-btn').addEventListener('click', function() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message) {
        var messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML += '<p>' + message + '</p>';
        input.value = '';
    }
});


document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Logique de connexion avec le nom d'utilisateur
});

document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Logique d'inscription avec le nom d'utilisateur
});

