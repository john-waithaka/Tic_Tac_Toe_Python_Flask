To run your Tic Tac Toe game with the integrated React front end and Flask back end, follow these steps:

1. Set Up and Run the Flask Back End
Navigate to the Flask Project Directory: Open a terminal and navigate to the root directory of your Flask project.

cd path/to/your/server
Create and Activate a Virtual Environment: It's good practice to use a virtual environment to manage your project dependencies.

python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
Install Dependencies: Install the required packages listed in your requirements.txt file.

pip install -r requirements.txt
Set Environment Variables: Ensure your Flask environment variables are set (you can do this in a .env file or directly in your terminal).

export FLASK_APP=run.py
export FLASK_ENV=development
Run Flask Migrations: Initialize the database and apply migrations.

flask db upgrade
Start the Flask Server: Run the Flask application.

flask run
The Flask server should now be running and accessible at http://localhost:5000.

2. Set Up and Run the React Front End
Navigate to the React Project Directory: Open a new terminal window and navigate to the root directory of your React project.

cd path/to/your/client
Install Dependencies: Install the required packages listed in your package.json file.

npm install
Start the React Development Server: Run the React development server.

npm start or npm run dev

