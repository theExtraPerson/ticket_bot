from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
    app.run(debug=True)

