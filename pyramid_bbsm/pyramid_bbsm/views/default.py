import json
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPBadRequest

from ..models import MyModel


#@view_config(context=MyModel, renderer='pyramid_bbsm:templates/mytemplate.pt')

@view_config(route_name='home', renderer='pyramid_bbsm:templates/signin.pt')
@view_config(route_name='login', renderer='pyramid_bbsm:templates/login.pt')
@view_config(route_name='signup', renderer='pyramid_bbsm:templates/signup.pt')
@view_config(route_name='profile', renderer='pyramid_bbsm:templates/profile.pt')
@view_config(route_name='accueil', renderer='pyramid_bbsm:templates/accueil.pt')
def my_view(request):
    return {'project': 'Pyramid_bbsm'}


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