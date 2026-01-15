# task-manager

A command line task manager written in Python that helps prioritize recurring tasks based on when they were last completed and available time.

I built this project because I wanted to build something that's usable in real life. I used to track tasks manually in an Excel sheet, so this felt like the perfect first project.
While building this project I learned core Python skills such as program structure, input validation, file I/O and date based logic.


## Features

- Add, edit and remove tasks

- Save/load tasks using a JSON file

- Track when tasks were last completed

- Identify overdue tasks by using a repeat window

- Option for manual and random task completion modes

- Randomly select tasks based on available time

- User friendly CLI menus with input validation


---


## How it works

Each task contains:

- A name

- An estimated completion time in minutes

- A repeat window in weeks

- A last completion date


Tasks are considered due if the last completion date exceeds the repeat window.
When starting a session, the user may pick the option to complete tasks manually or let the program randomly select tasks based on available time. 


---


## Known Limitations

- Tasks are stored as dictionaries instead of objects

- CLI only interface

- Only uses dd- mm- yyyy date format


These are intentional for now and will be addressed in later versions


---


## Future improvements

- Refactor tasks into "Task" class

- Add option to change date format

- Support additional task prioritization strategies
