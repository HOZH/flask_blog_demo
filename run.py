from flask_blog import create_app


app = create_app()

if __name__=='__main__':
    app.run(debug=True, port=8999,host='0.0.0.0')
