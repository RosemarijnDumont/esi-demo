from auth_service.app import create_app, db
from auth_service.app.models.user import User

app = create_app()

@app.cli.command('create-admin')
def create_admin():
    """Creates a default admin user"""
    with app.app_context():
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        
        if User.query.filter_by(username=username).first():
            print(f"User {username} already exists.")
            return

        admin_user = User(username=username)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {username} created successfully.")

if __name__ == '__main__':
    app.run(debug=True)
