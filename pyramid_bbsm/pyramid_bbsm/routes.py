def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('root', "/")
    # config.add_route('inscription', "/inscription")
    # config.add_route('connexion', "/connexion")
    # config.add_route('home', "/home")

    config.add_route('signin', "/")
    config.add_route('signup', "/signup")
    config.add_route('profile', "/profile")
    config.add_route('accueil', "/accueil")
    config.add_route('get_messages', '/get_messages')
    config.add_route('send_message', '/send_message')

