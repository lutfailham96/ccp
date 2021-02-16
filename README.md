# Computer Control Panel
![](/screenshots/auto-scheduling.gif)

# About
Computer Control Panel (CCP) aplikasi web untuk memonitoring, remote shutdown/restart device multi platform

# Features
- Multi platform (Windows, Linux)
- Automatic connection recovery
- Fully synced with server

# Requirements
- Python > 3.7
- Flask
- Mariadb/MySQL

# Screenshots
- Login
![Alt text](/screenshots/login.png?raw=true "Login")
- Dashboard
![Alt text](/screenshots/dashboard.png?raw=true "Dashbboard")
- Profile
![Alt text](/screenshots/update-profil.png?raw=true "Update Profil")

# Installation & running on server side
- Edit config.py, specify database host, username, password, database name
- Import app.sql to your database
- Running app on terminal: python run.py
- Default credentials (username: admin, password: migascepu)

# Running on client side
- Choose beetween http client / socket client (recommended)
- Commmand: python socket_client.py -i instance_name -l location -c computer_name
- Example: python socket_client.py -i "PT_Maju" -l "Departmen_A" -c "A8"
- Better to use it as service with your own way
