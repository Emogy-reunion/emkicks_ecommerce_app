from create_app import create_app
'''
initializes the libraries
creates initial admins
runs the application
'''


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
