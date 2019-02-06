from messenger import application


if __name__ == '__main__':
    print(f'Listening {application.config["DEBUG"]} on port {application.config["BIND_PORT"]}')
    application.run(
        host=application.config['BIND_IP'],
        port=application.config['BIND_PORT'],
        debug=application.config['DEBUG']
    )
