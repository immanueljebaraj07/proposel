# Setup Guide for Grocery Proposal Generator

## Installation and Configuration Instructions

### Prerequisites
- Python 3.7 or later
- Flask
- A database (SQLite or any relational database)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/immanueljebaraj07/proposel.git
   cd proposel
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Flask Setup
1. **Set Environment Variables**:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

2. **Run the Application**:
   ```bash
   flask run
   ```
   Open your browser and go to `http://127.0.0.1:5000`.

### Email Configuration
- Create a `.env` file in the project root and add the following:
  ```
  EMAIL_USER='your_email@example.com'
  EMAIL_PASSWORD='your_email_password'
  ```

### Database Initialization
1. **Initialize the Database**:
   Make sure to create the necessary tables in your database. For SQLite, you can do this via:
   ```bash
   python init_db.py
   ```

### Running the Application
Once everything is set up, you can run the application using:
```bash
flask run
```

 Visit the application in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Conclusion
You should now have the Grocery Proposal Generator application running locally. For any issues, please check the repository's issue tracker.