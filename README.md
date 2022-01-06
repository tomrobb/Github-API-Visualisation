# Github-API-Visualisation
A project for CSU33012 Software Engineering written in Python, which interrogates the Github REST API (documentation [here](https://docs.github.com/en/rest)), and creates a visualisation of the chosen data.

## Technologies Used
- Python3
- PyGithub to access the GitHub REST API
- Streamlit for user interface/deploying application
- Plotly for data visualisation

## How to run
- Clone this repository, and open it in the command line
- Open the directory in the command line/terminal, and activate a new virtual environment. On Windows, this can be done by running the commands
`python -m venv venv` to create the virtual environment, and 
`venv\Scripts\activate.bat` to activate the virtual environment
- Install the dependencies by running the command `pip install -r requirements.txt`
- Deploy the application with the command `streamlit run app.py`, this will automatically open the application in a new browser tab. 

**Note:**  Make sure that you have included your GitHub Auth token in "token.txt". The application will notify you if the token is invalid.

## Demonstration
### User Dashboard:
<p align="center">
  <img src="https://github.com/tomroberts201/Github-API-Visualisation/blob/master/images/user_demo.gif">
</p>

### Repository Visualisation:
<p align="center">
  <img src="https://github.com/tomroberts201/Github-API-Visualisation/blob/master/images/repo_demo.gif">
</p>

I'll add more to this README in the future
