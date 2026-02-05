from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 🔹 This will now see SQLALCHEMY_DATABASE_URI
    app.run(debug=True, port=5001, threaded=False) # 🔹 Use 5001 to avoid Mac AirPlay conflicts