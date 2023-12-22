import json
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import remember
import os

from ..models import MyModel


#@view_config(context=MyModel, renderer='pyramid_bbsm:templates/mytemplate.pt')

#@view_config(route_name='signin', renderer='pyramid_bbsm:templates/signin.pt')
#@view_config(route_name='login', renderer='pyramid_bbsm:templates/login.pt')
#@view_config(route_name='signup', renderer='pyramid_bbsm:templates/signup.pt')
@view_config(route_name='profile', renderer='pyramid_bbsm:templates/profile.pt')
#@view_config(route_name='accueil', renderer='pyramid_bbsm:templates/accueil.pt')
def my_view(request):
    return {'project': 'Pyramid_bbsm'}


# Fonction pour connexion
@view_config(route_name='signin', renderer='pyramid_bbsm:templates/signin.pt', request_method='GET')
def view_login(request):
    # Initialiser des valeurs vides pour le formulaire et aucun message d'erreur
    return {
        'username': '',
        'error_message': ''
    }

@view_config(route_name='signin', renderer='pyramid_bbsm:templates/signin.pt', request_method='POST')
def confirme_login(request):
    # Récupération des données du formulaire
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Chemin du fichier JSON
    json_file_path = 'users.json'  # Assurez-vous que ce chemin est correct

    # Vérifier si les champs sont remplis
    if not username or not password:
        return {
            'username': username,
            'error_message': "Le username et le mot de passe doivent être remplis."
        }

    # Lire le fichier JSON pour vérifier si l'utilisateur existe et le mot de passe est correct
    try:
        with open(json_file_path, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return {
            'username': username,
            'error_message': "Aucun utilisateur enregistré."
        }
    except json.JSONDecodeError:
        return {
            'username': username,
            'error_message': "Erreur lors de la lecture de la base de données des utilisateurs."
        }

    # Vérifier si l'email et le mot de passe correspondent
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Créer un jeton unique pour la session (dans une application réelle, utilisez plutôt un mécanisme de session sécurisé)
        headers = remember(request, user['username'])

        # Rediriger l'utilisateur après connexion réussie
        return HTTPFound(location=request.route_url('accueil'), headers=headers)

    # Si l'utilisateur n'est pas trouvé ou le mot de passe est incorrect
    return {
        'username': username,
        'error_message': "username ou mot de passe incorrect."
    }


# Fonction pour inscription
@view_config(route_name='signup', renderer='pyramid_bbsm:templates/signup.pt', request_method='GET')
def view_login(request):
    return {
        'username': '',
        'error_message': ''
    }

@view_config(route_name='signup', renderer='pyramid_bbsm:templates/signup.pt', request_method='POST')
def signup_view(request):
    # Récupérer les données du formulaire
    username = request.params.get('username')
    password = request.params.get('password')

    # Valider les données
    if not (username and password):
        return {
            'username': username,
            'error_message': "Tous les champs doivent être remplis."
        }

    # Chemin vers le fichier JSON où les utilisateurs sont enregistrés
    json_file_path = os.path.join(os.path.dirname(__file__), 'users.json')
    
    # Lire le fichier JSON pour vérifier si l'utilisateur existe déjà
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    # Vérifier si le nom d'utilisateur existe déjà
    if any(user['username'] == username for user in users):
        return {
            'username': username,
            'error_message': "Le nom d'utilisateur existe déjà."
        }

    # Ajouter le nouvel utilisateur à la liste
    users.append({'username': username, 'password': password})

    # Sauvegarder la liste mise à jour dans le fichier JSON
    with open(json_file_path, 'w') as file:
        json.dump(users, file, indent=4)

    # Authentifier l'utilisateur et le rediriger vers la page d'accueil
    headers = remember(request, username)
    return HTTPFound(location=request.route_url('accueil'), headers=headers)


# Envoie de message
@view_config(route_name='send_message', request_method='POST', renderer='json')
def send_message(request):
    # Récupérer le message depuis la requête
    message = request.json_body.get('message')
    
    # Supposons que 'request.user' contient l'objet utilisateur actuel
    # Si 'request.user' est None ou ne contient pas 'username', utilisez 'Guest'
    username = getattr(request.user, 'username', 'Guest')
    
    if message:
        # Construire l'entrée du message
        message_entry = {'user': username, 'text': message}

        # Ajouter le message à la liste existante
        try:
            with open('messages.json', 'r+') as file:
                messages = json.load(file)
                messages.append(message_entry)
                file.seek(0)  # Revenir au début du fichier avant d'écrire
                json.dump(messages, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou est vide/corrompu, créez un nouveau fichier
            with open('messages.json', 'w') as file:
                json.dump([message_entry], file, indent=4)
                
        return {'status': 'success', 'message': 'Message sent'}
    else:
        return {'status': 'error', 'message': 'No message to send'}
    

# Redirection accueil
@view_config(route_name='accueil', renderer='pyramid_bbsm:templates/accueil.pt')
def my_view(request):
    # Charger les messages depuis le fichier JSON
    try:
        with open('messages.json', 'r') as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []  # Fournir une liste vide si le fichier n'existe pas ou s'il y a une erreur de lecture

    # Retourner les messages à la vue
    return {'project': 'Pyramid_bbsm', 'messages': messages}


"""
@view_config(route_name='inscription', renderer='pyramid_bbsm:templates/inscription.pt', request_method='GET')
def view_inscription(request):
    # Initialiser des valeurs vides pour le formulaire et aucun message d'erreur
    return {
        'email': '',
        'username': '',
        'password': '',
        'error_message': ''
    }

@view_config(route_name='inscription', renderer='pyramid_bbsm:templates/inscription.pt', request_method='POST')
def confirme_inscription(request):
    # Récupération des données du formulaire
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    # Chemin du fichier JSON
    json_file_path = 'users.json'  # Chemin modifié pour 'users.json'

    # Vérifier si les champs sont remplis
    if not username or not password or not email:
        return HTTPBadRequest(detail="Tous les champs doivent être remplis.")

    # Vérifier la validité de l'email (cette étape est basique, utilisez une expression régulière pour une validation plus robuste)
    if '@' not in email:
        return HTTPBadRequest(detail="Email non valide.")

    # Lire le fichier JSON pour vérifier si l'utilisateur ou l'email existe déjà
    try:
        with open(json_file_path, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    except json.JSONDecodeError:
        users = []

    # Vérifier si l'utilisateur ou l'email existe déjà
    user_exists = any(user['username'] == username for user in users)
    email_exists = any(user['email'] == email for user in users)

    error_message = ''
    if not username or not password or not email:
        error_message = "Tous les champs doivent être remplis."
    elif user_exists:
        error_message = "Utilisateur existe déjà."
    elif email_exists:
        error_message = "Email déjà utilisé."

    if error_message:
        # Renvoyer le rendu du template avec les données du formulaire et le message d'erreur
        return {
            'username': username,
            'email': email,
            'error_message': error_message
        }

    # Ajouter le nouvel utilisateur
    users.append({'username': username, 'email': email, 'password': password})

    # Enregistrer les données dans le fichier JSON
    with open(json_file_path, 'w') as file:
        json.dump(users, file, indent=4)

    # Rediriger l'utilisateur après inscription réussie
    return HTTPFound(location=request.route_url('home'), headers={'Refresh': '1.5'})
"""