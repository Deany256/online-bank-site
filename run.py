from app import create_app
import os

# Get the environment ('development' or 'production') from the .env file
env = os.getenv('FLASK_ENV', 'development')

# Create the Flask app with the appropriate configuration
app = create_app(config_name=env)

if __name__ == '__main__':
    # Run the app
    app.run()