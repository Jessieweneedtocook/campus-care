# Campus Care 

**How to run the application**

1. First run docker-compose.yml, this runs mysql container and flask container
2. Then if database not initialised, run db-connection.py
3. Then run Frontend/main.py


Campus Care is a student wellness application developed with the goal of promoting healthier habits and improve mental wellbeing among students by monitoring daily activities, delivering wellness quizzes, and providing personalized progress insights.

The contributers to this project include:
- cellis1912
- imtheguy456
- jessieweneedtocook
-
-


The application was built using:
- **Frontend:** [Kivy](https://kivy.org/) for cross-platform GUI development.  
- **Backend:** [Flask](https://flask.palletsprojects.com/) with Docker for containerized database services.  
- **Database:** Local SQLite for activity/user preferences + Dockerized user database for authentication.  

Key features:
- Secure login, signup, and password reset.  
- Daily wellness quiz with personalized questions.  
- Activity tracking and visualization (graphs, weekly insights).  
- Wellness progress screen showing most/least improved habits.  
- Integration between Kivy frontend and Flask backend via URL requests.  

---

## My Contributions

I was mostly responsible for leading the **frontend development** of Campus Care, while also supporting backend integration tasks. My main contributions included:

- **Frontend design & prototyping**
  - Designed initial GUI prototypes in Figma.
  - Specified functional and non-functional UI requirements in the design document.
  - Produced UML diagrams for class interactions and user flows.

- **Frontend implementation**
  - Built core GUI screens (login, signup, reset password, daily quiz, home, wellness progress) using Kivy + KV language.
  - Implemented a dynamic `DailyQuizScreen` system to cycle through quiz questions sequentially.
  - Developed screen manager and app template (`app.py`) for navigation and structure.
  - Ensured accessibility by following guidelines for text size and colour-blindness compatibility.

- **Integration with backend**
  - Implemented URL requests in Kivy to send signup/login data to the Flask backend and Dockerized user database.
  - Connected frontend to local SQLite databases for personalized quiz questions and wellness tracking.
  - Displayed data visualizations in the GUI, including weekly activity progress graphs.
  - Added frontend validation linked with backend error handling for robust user input.

- **Team & project management**
  - Set up and maintained the Git repository for collaborative work.
  - Created collaboration documents and Gantt charts for planning.
  - Edited and formatted the technical design document before submission.
  - Contributed to backend debugging (e.g., fixing SQL queries for activity progress).


