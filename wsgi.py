import os , sys
from project.app import app


# Add the project directory to the sys.path
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))

from app import app


if __name__ == "__main__":
    app.run(debug=1)
