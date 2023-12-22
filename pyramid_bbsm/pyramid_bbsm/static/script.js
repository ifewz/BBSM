document.addEventListener('DOMContentLoaded', function() {
    // Gestion de l'envoi de message dans la chatbox
    document.getElementById('send-btn').addEventListener('click', function() {
        var input = document.getElementById('chat-input');
        var message = input.value.trim();
        if (message) {
            var messagesContainer = document.getElementById('messages');
            messagesContainer.innerHTML += '<p>' + message + '</p>';
            input.value = '';

            // Envoyer le message au serveur
            fetch('/send_message', {
                method: 'POST',
                body: JSON.stringify({ message: message }),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response => {
                if (response.ok) {
                    console.log('Message envoyé');
                    refreshMessages(); // Actualiser la liste des messages
                }
            }).catch(error => {
                console.error('Erreur lors de l\'envoi du message', error);
            });
        }
    });

    // Fonction pour actualiser les messages
    function refreshMessages() {
        fetch('/get_messages').then(response => {
            return response.json();
        }).then(data => {
            var chatBox = document.getElementById('messages');
            chatBox.innerHTML = ''; // Effacer les messages existants

            // Ajouter les nouveaux messages
            data.forEach(message => {
                let messageDiv = document.createElement('div');
                messageDiv.textContent = message.user + ': ' + message.text;
                chatBox.appendChild(messageDiv);
            });
        }).catch(error => {
            console.error('Erreur lors de la récupération des messages', error);
        });
    }

    // Actualiser les messages toutes les 5 secondes
    setInterval(refreshMessages, 5000);

    // Gestion de la soumission du formulaire de connexion
    var loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Logique de connexion avec le nom d'utilisateur
        });
    }

    // Gestion de la soumission du formulaire d'inscription
    var signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Logique d'inscription avec le nom d'utilisateur
        });
    }
});
