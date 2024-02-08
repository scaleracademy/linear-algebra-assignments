# Setup environment

Prefer using Linux/Macos - things might not work properly for Windows

### Macos/Linux

```bash
# create a virtual environment
python3 -m venv .venv
# activate the virtual environment
source .venv/bin/activate
# install the requirements
pip install -r requirements.txt
```

### Windows

```bash
# create a virtual environment
python -m venv .venv
# activate the virtual environment
.venv\Scripts\activate
# install the requirements
pip install -r requirements.txt
```

# Submission Instructions

1. Put your solutions inside the `solutions` folder
    - enter your email and name inside the `solutions/student_details.py` file
    - PLDU assignment: `solutions/pldu.py`
    - Linear Equations assignment: `solutions/equations.py`
    - Simplex assignment: `solutions/simplex.py`
    - Image Compression assignment: `solutions/image_compression/` directory
    - Meal Planner assignment: `solutions/meal_planner/` directory
    - note: if you've not done a particular assignment, don't worry, leave that part as it is
2. To submit
    - execute
      ```bash
      python make_submission.py
       ```
    - this will generate a solutions.zip file
    - it will also tell you the expected marks for the auto-graded assignments (PLDU, Linear Equations, Simplex)
    - upload this file to the dashboard

### Note:

- Do NOT change the file, or function names, or the number of input arguments in the functions
    - your solution will be autograded, so if the names don't match, your grade will become 0
- Do NOT use any external libraries
- Do NOT use print statements in your code
