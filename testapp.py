import streamlit as st
import streamlit.components.v1 as stc
from github import Github
import plotly.graph_objects as go
from math import pi
from collections import Counter


# getting the Github User Auth Token from token.txt
file = open("token.txt")
token = file.read()
file.close()


st.set_page_config(layout="wide")


# connecting to github api via access token
valid_token = True
g = Github(token)
try:
    # running a sample "get_user" call with token
    testTokenCallback = g.get_user("tomroberts201")
except Exception as e:
    # if an error occurs, the entered token is invalid
    valid_token = False


# A function which displays a user's profile information in their respective columns.
#   Parameter(s):
#       - Github user object
#
#   Displays the following:
#       - Profile Avatar (in column 1_1)
#       - Username, Name, Location (in column 1_2)
def display_user_info(usr):
    userImage = '"' + usr.avatar_url + '"'
    userName = usr.name
    userLogin = usr.login
    userLocation = usr.location
    userLink = usr.html_url

    with col1_1:
        # html component to display avatar image rounded
        stc.html("""
        <body>
            <style>
                img {
                    border-radius: 50%;
                }
            </style>
            <img src= """ + userImage + """alt ="Avatar" style="width:175px">
        </body>""",
        width=250, height=250)
    col1_2.markdown("##### " + userLogin)
    if userName is not None:
        col1_2.write(" " + userName)
    if userLocation is not None:
        col1_2.write(userLocation)
    if userLink is not None:
        col1_2.markdown("""[Link to Profile](""" + userLink + """)""")


# A function which get's the data from all of a user's repositories.
#   Parameter(s):
#       - User Repositories
#
#   Returns:
#       - A list of dictionaries containing the relevant information for each repository.
def get_repo_data(user_repos):
    repos = []
    for i in user_repos:
        dct = {
            "name": i.name,
            "stars": i.stargazers_count,
            "language": i.language,
            "size": i.size,
        }
        repos.append(dct)
    return repos



# -----  SIDEBAR CODE  ----- #
input_type = "null"
valid_input = True

st.sidebar.image('./images/logo.png')

user_in = st.sidebar.text_input("Enter github username or repo link:")


# for when the user inputs a username
if "/" not in user_in and len(user_in) > 3:
    input_type = "user"
    try:
        usr = g.get_user(user_in)
    except Exception as e:
        st.sidebar.write("User not found")
        valid_input = False

# for when the user inputs a repo link
if "/" in user_in and len(user_in) > 5:
    input_type = "repo"
    if user_in.startswith("https"):
        user_in = user_in[19:]
    if user_in.startswith("github"):
        user_in = user_in[11:]
    try:
        rpo = g.get_repo(user_in)
    except Exception as e:
        st.sidebar.write("Repository not found")
        valid_input = False

if valid_input and input_type == "user":
    rNames = []

    for i in usr.get_repos():
        rNames.append(i.name)

    rSelection = st.sidebar.selectbox('Choose a Repository:', rNames)

    if st.sidebar.button('View Repository Data'):
        longName = usr.login + "/" + rSelection
        input_type = "repo"
        rpo = g.get_repo(longName)



# -----  TOP BAR  ----- #
# Displaying the various titles based on what "page" we're on.
if valid_token == False:
    st.title('⚠ Invalid Auth Token')
    st.write("Please make sure that a valid Auth token has been provided in the \"token.txt\" file.")

if input_type == "user":
    st.title('👥 User Dashboard')
    st.write("")
    col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns([1.0, 1.5, 1, 1, 2])

if input_type == "repo":
    st.title('📁 Repository Data Visualisation')

if input_type == "null" and valid_token == True:
    st.title('📈 GitHub API Data Visualisation')
    st.write("Enter a username or repository link to begin! : )")


# st.caption("Link to the repository [here](https://github.com/" + lRepo +")")


#  ----- Column 1_1 and 1_2 ----- #
#   +   Display User Avatar + info
#   +   Also initialises the variables used by other columns
if valid_input and input_type == "user":
    display_user_info(usr)
    userRepoData = get_repo_data(usr.get_repos())
if valid_input and input_type == "repo":
    st.write(rpo.name)


# -----  Column 1_3  ----- #
#   +   Display Followers & Total Repos
if valid_input and input_type == "user":
    col1_3.metric("Followers", usr.followers)
    col1_3.metric("Public Repos", len(userRepoData))

# rnlabels = []
# rnvalues = []
# # getting the usernames and values from the languages

# for key in numRepoCommits.keys():
#     rnlabels.append(key)
# for val in numRepoCommits.values():
#     rnvalues.append(val)

# fig2 = go.Figure(data=[go.Table(header=dict(values=['Repository Name','Number of Commits'],
#                                             line_color='#11151c',
#                                             fill_color='#262730',
#                                             align=['center', 'center'],
#                                             height=30,
#                                             font=dict(color='white', size=16)),
#                                cells=dict(values=[rnlabels, rnvalues],
#                                           line_color='#11151c',
#                                           fill_color='#0e1117',
#                                           align=['center', 'center'],
#                                           height=23,
#                                           font=dict(color='white', size=[12, 14])),
#                                 columnwidth = [150,80])
#                       ])

# fig2.update_layout(title='Number of commits for each repository', autosize=False,
#                    height=350)

# col1_2.plotly_chart(fig2, use_container_width=True)


# ----- COLUMN 1-4 ----- #
#   +   Display Following & Stars Received
if valid_input and input_type == "user":

    totalStars = 0
    for i in userRepoData:
        totalStars += i.get("stars")

    col1_4.metric("Following", usr.following)
    col1_4.metric("Stars Received", totalStars)


# ----- COLUMN 2-1 ----- #

if valid_input and input_type == "user":
    col2_1, col2_2, col2_3 = st.columns(3)

# Displays PieChart of user's main repo languages
if valid_input and input_type == "user":
    languages = []

    for i in userRepoData:
        languages.append(i.get("language"))

    # dictionary of "language":count
    clanguages = dict(Counter(languages))

    sort_orders = (sorted(clanguages.items(), key=lambda x:x[1],reverse=True))

    if len(sort_orders) > 10:
        clanguages = dict(sort_orders[:10])

        plabels = list(clanguages.keys())
        pvalues = list(clanguages.values())

        fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
        fig.update_layout(title='Repository Languages (Top 10):', autosize=False,
                        width=650, height=500)
        if len(plabels) != 0:
            col2_1.plotly_chart(fig, use_container_width=True)
    else:
        clanguages = dict(sort_orders)

        plabels = list(clanguages.keys())
        pvalues = list(clanguages.values())

        fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
        fig.update_layout(title='Repository Languages:', autosize=False,
                        width=650, height=500)
        if len(plabels) != 0:
            col2_1.plotly_chart(fig, use_container_width=True)



# ----- COLUMN 2-2 ----- #
if valid_input and input_type == "user":
    labels = []
    values = []
    stars_per_repo = {}

    for i in userRepoData:
        if i.get("stars") != 0:
            # adding value to dictionary
            stars_per_repo[i.get("name")]= i.get("stars")

    st.write(stars_per_repo)
    sort_orders = (sorted(stars_per_repo.items(), key=lambda x:x[1],reverse=True))


    if len(sort_orders) > 10:
        stars_per_repo = dict(sort_orders[:10])

        labels = list(stars_per_repo.keys())
        values = list(stars_per_repo.values())
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title='Stars per Repo (Top 10):', autosize=False,
                        width=650, height=500)
        fig.update_traces(hoverinfo='label+value', textinfo='value')
        if len(labels) != 0:
            col2_2.plotly_chart(fig, use_container_width=True)
    else:
        stars_per_repo = dict(sort_orders)

        labels = list(stars_per_repo.keys())
        values = list(stars_per_repo.values())
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title='Stars per Repo:', autosize=False,
                        width=650, height=500)
        fig.update_traces(hoverinfo='label+value', textinfo='value')
        if len(labels) != 0:
            col2_2.plotly_chart(fig, use_container_width=True)





# ----- COLUMN 2-3 ----- #
if valid_input and input_type == "user":
    names = []
    stars = []

    for i in userRepoData:
        names.append(i.get("name"))
        stars.append(i.get("stars"))

    fig = go.Figure([go.Bar(x=names, y=stars)])

    col2_3.plotly_chart(fig, use_container_width=True)

if input_type == "repo":
    st.write("repo")
