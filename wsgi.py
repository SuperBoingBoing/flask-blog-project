import sys

# Add the path to your project to PYTHONPATH so Python can find your app
sys.path.append('/home/SuperBoingBoing/flask-blog-project') # 1. Replace with your project path

from app import app # 2. Replace 'app' with the name of your Flask app instance

application = app
