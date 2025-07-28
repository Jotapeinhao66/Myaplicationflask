
# Deployment Instructions for Flask Application

This document provides instructions on how to deploy the Flask web application for visualizing country data.

## Prerequisites

*   A web hosting platform that supports Python applications and WSGI servers (e.g., Heroku, render.com, AWS Elastic Beanstalk, etc.). This guide will focus on a general approach applicable to platforms like Heroku or render.com.
*   Git installed and the project code committed to a Git repository (e.g., GitHub, GitLab, Bitbucket).
*   A Heroku or render.com account (or an account on your chosen platform).
*   Heroku CLI or Render CLI installed (if using those platforms).

## Files

Ensure your project directory contains the following files:

*   `app.py`: The main Flask application file.
*   `data_processing.py`: Module for data loading and cleaning.
*   `requirements.txt`: Lists Python dependencies.
*   `Procfile` (to be created): Tells the hosting platform how to run the application.
*   `templates/index.html`: The HTML template for the web page.
*   `static/`: Directory for static files (if any).
*   Data files (`DatosGDPCONS2.csv`, `Porcentaje_acceso_internet.csv`): Your data files. These need to be accessible by the application on the server. For simplicity, you might place them in the root directory or a data subdirectory.

## Step 1: Create a Procfile

A `Procfile` tells the hosting platform what command to run to start your web application. Create a file named `Procfile` (no extension) in the root directory of your project with the following content:

```text
web: gunicorn app:app
```

This line tells the platform to start a web process using Gunicorn, running the `app` callable within the `app.py` file.

## Step 2: Choose a Deployment Platform and Set Up

Choose a platform like Heroku or render.com.

### Using Heroku:

1.  **Create a new Heroku app:**
    ```bash
    heroku create your-app-name
    ```
    (Replace `your-app-name` with a unique name)
2.  **Link your local Git repository to the Heroku app:**
    ```bash
    heroku git:remote -a your-app-name
    ```
3.  **Configure Environment Variables (if needed):** If your application uses environment variables (e.g., for API keys, database connections - though not needed for this simple app), you would set them here:
    ```bash
    heroku config:set MY_VARIABLE=my_value
    ```
4.  **Add buildpacks (if needed):** Heroku automatically detects Python, but if you needed specific buildpacks, you'd add them here.

### Using render.com:

1.  **Create a new Web Service:** In your Render dashboard, create a new Web Service.
2.  **Connect your Git repository:** Link your GitHub/GitLab/Bitbucket repository.
3.  **Configure settings:**
    *   **Name:** Choose a name for your service.
    *   **Region:** Select a region.
    *   **Branch:** Choose the branch to deploy from.
    *   **Root Directory:** Usually leave blank if your app is in the repo root.
    *   **Runtime:** Python 3.
    *   **Build Command:** `pip install -r requirements.txt`.
    *   **Start Command:** `gunicorn app:app`.
    *   **Environment Variables (if needed):** Add any environment variables.

## Step 3: Deploy Your Code

Once your `Procfile` is created and your platform is set up:

### Using Heroku:

1.  **Commit your Procfile:**
    ```bash
    git add Procfile
    git commit -m "Add Procfile"
    ```
2.  **Push to Heroku:**
    ```bash
    git push heroku main
    ```
    (or `master`, depending on your branch name)
    Heroku will detect the `requirements.txt`, install dependencies, and start the web process defined in the `Procfile`.

### Using render.com:

Render automatically deploys when you push changes to the configured branch of your connected repository. Just ensure your `requirements.txt` and `Procfile` are committed and pushed to your repository.

## Step 4: Access Your Application

After the deployment is successful, your application will be accessible at the URL provided by your hosting platform (e.g., `https://your-app-name.herokuapp.com/` for Heroku, or a similar URL for Render).

## Important Considerations:

*   **Data Files:** Ensure your data files (`DatosGDPCONS2.csv`, `Porcentaje_acceso_internet.csv`) are included in your Git repository and placed in a location where `data_processing.py` can find them on the server (e.g., the root directory).
*   **Environment Variables:** If you expand your application to use sensitive information or configuration that shouldn't be in your code, use environment variables and configure them on your hosting platform.
*   **Scaling:** For production applications with significant traffic, you would need to configure scaling on your platform (e.g., adding more Gunicorn worker processes).
*   **Logging:** Set up proper logging to monitor your application on the server.
*   **Error Handling:** Implement more robust error handling in your Flask app.
