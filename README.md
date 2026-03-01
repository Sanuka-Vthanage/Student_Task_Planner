Student Task Planner

Group members:
- Sanuka Vithanage    - ITBIN-2313-0118
- Mulani Yohansa      - ITBIN-2312-0019
- Maleesha Godakanda  - ITBIN-2313-0069


Technologies used:

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Flask
- Flask-CORS
- Gunicorn

Database:
- SQLite

Deployment:
- Frontend deployed on Netlify
- Backend deployed on Render



Project Overview

Student Task Planner is a web-based task management system that allows users to:

- Add new tasks
- View all tasks
- Store tasks persistently using SQLite
- Access the system through a deployed cloud environment

This project demonstrates Git collaboration and DevOps deployment practices.



System Architecture

Client (Browser)
    |
    v
Netlify (Static Frontend)
    |
    v
Render (Flask Backend API)
    |
    v
SQLite Database



Technologies Used

Frontend:
- HTML5
- CSS3
- JavaScript (Fetch API)

Backend:
- Python
- Flask
- Flask-CORS
- Gunicorn

Database:
- SQLite (Embedded database)


Deployment Details

Frontend:
- Hosted on Netlify
- Connected to GitHub repository
- Automatic deployment on push to main branch

Backend:
- Hosted on Render
- Runtime: Python
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app

Project Structure

Student_Task_Planner/
|
|-- index.html
|-- New.css
|-- new.js
|
|-- app.py
|-- requirements.txt
|-- .gitignore
|-- README.md

Render deployment: Add a free PostgreSQL database in the Render dashboard and connect it to your web service. The app automatically uses PostgreSQL when DATABASE_URL is set.




