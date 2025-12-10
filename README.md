# IEE305-Group-5-Final-Project
Final project for IEE305. Uses USGS API, backend data storage and API, and a frontend user interface to allow users to search earthquake data.

TO USE:
1. Download and install all files and paste them into a new VSCode project.
2. In the terminal, enter a virtual environment with ".\venv\Scripts\Activate.ps1"
3. Input "uvicorn Backend.main:app --reload" into terminal to initialize the backend server.
4. Verify that backend server is running by navigating to http://127.0.0.1:8000/
5. Navigate to http://127.0.0.1:8000/reset-db to wipe the database files and create new database tables.
6. Database files should now be set up. Now, navigate to http://127.0.0.1:8000/docs#/default/fetch_data_fetch_post and execute /fetch to populate database with data.
7. Now that the local database has data, navigate to terminal in VSCode. Create new terminal.
8. Enter "streamlit run Frontend/frontend.py" into terminal to run frontend GUI. New browser tab should pop up.
9. You can now use the GUI to select a minimum and maximum magnitude, and visualize it on the map!
