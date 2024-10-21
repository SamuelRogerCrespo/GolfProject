from website import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Check if running on Heroku or in development
    if os.environ.get('HEROKU'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Dynamic port for Heroku
    else:
        app.run(debug=True)  # Enable debug mode for local development
