## Install Django within a Virtual Environment

For better flexibility, we will install Django and all of its dependencies within a Python virtual environment.

You can get the virtualenv package that allows you to create these environments by typing:

```
sudo pip install virtualenv
```

Move into the project directory afterwards:

```
mkdir ~/trail-assignment
cd ~/trail-assignment
```

We can create a virtual environment to store our Django project’s Python requirements by typing:

```
virtualenv env
```

This will install a local copy of Python and pip into a directory called myprojectenv within your project directory.

Before we install applications within the virtual environment, we need to activate it. You can do so by typing:

```
source env/bin/activate
```

Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this 

```
(env)user@host:~/trail-assignment$.
```

Once your virtual environment is active, you can install Django with pip. We will also install the psycopg2 package that will allow us to use the database we configured:

```
pip install -r requirements.txt
```

We can now start a Django server within our myproject directory. 

```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Frontend repo setup

Node js installation

```
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs
```

Install the node libraries 

```
cd /trail-assignment/src/frontend/
npm install
npm run build
```

This will create a build folder inside the frontend application.

```
/trail-assignment/src/frontend/build
```

We have added this build in Django settings app so if this file is in this exact position We don't need to change anything else

## Serving React APP with Django

We need to add configuration for react static files in settings.py. Then a view to render the React page and a URL config to display the view is needed, both of these can be added to the project directory where the settings.py is located.

### First add the path to React build drectory in Djnago settings.py inside the project diretory

```
REACT_APP_DIR = os.path.join(BASE_DIR, "src/frontend")
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, "build", "static"),
]
```

### Now we can create a views.py in Django project directory and add this code


```
import os
import logging
from django.conf import settings
from django.http import HttpResponse

index_file_path = os.path.join(settings.REACT_APP_DIR, "build", "index.html")


def react(request):
    """
    A view to serve the react app by reading the index.html from the
    build  react app and serving it as a Httpresponse.
    """
    try:
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception("Production build of app not found")
```

### Now inside urls.py in project directory add the URL for this view


```
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path for user urls,
    # path for sales urls,
    re_path(r"^.*$", views.react, name="home"),
]

```

**Edit a file, create a new file, and clone from Bitbucket in under 2 minutes**

When you're done, you can delete the content in this README and update the file with details for others getting started with your repository.

*We recommend that you open this README in another tab as you perform the tasks below. You can [watch our video](https://youtu.be/0ocf7u76WSo) for a full demo of all the steps in this tutorial. Open the video in a new tab to avoid leaving Bitbucket.*

---

## Edit a file

You’ll start by editing this README file to learn how to edit a file in Bitbucket.

1. Click **Source** on the left side.
2. Click the README.md link from the list of files.
3. Click the **Edit** button.
4. Delete the following text: *Delete this line to make a change to the README from Bitbucket.*
5. After making your change, click **Commit** and then **Commit** again in the dialog. The commit page will open and you’ll see the change you just made.
6. Go back to the **Source** page.

---

## Create a file

Next, you’ll add a new file to this repository.

1. Click the **New file** button at the top of the **Source** page.
2. Give the file a filename of **contributors.txt**.
3. Enter your name in the empty file space.
4. Click **Commit** and then **Commit** again in the dialog.
5. Go back to the **Source** page.

Before you move on, go ahead and explore the repository. You've already seen the **Source** page, but check out the **Commits**, **Branches**, and **Settings** pages.

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).