# NextGen
NextGen is a Python-based AI project that takes URL/DOM structure from the user and generates the Gherkin files, Step definition and Implementation file for the user to reduce the manual intervention of the Quality Engineers.

## Steps to run NextGen on your system:
### 1. Install VS Code as IDE
Download VS Code from this [link](https://code.visualstudio.com/docs/?dv=win64user). If you are getting an Unverified download blocked error (refer to the image below)
<img width="323" alt="image" src="https://github.com/user-attachments/assets/447d5f9c-1211-48f1-8be1-957d49b5dd44">

open the unloaded file and click on Download unverified file to continue (refer to the image below)
<img width="560" alt="image" src="https://github.com/user-attachments/assets/73d248f8-03ce-4114-9727-651f05b8a937">

### 2. Install Python
Make sure you have Python installed on your system. Run command ```python --version``` in CMD to verify.

<img width="410" alt="image" src="https://github.com/user-attachments/assets/855526c2-5e2d-443e-8232-fdb922223f27">

If the command does not return the Python version, install Python from ManageEngine Desktop Central

<img width="800" alt="image" src="https://github.com/user-attachments/assets/4fbd43a2-5fb2-4a4a-9704-6612bf63bd07">

### 3. Install extensions that will support you while working on Python in VS Code
### 4. Create a virtual environment by using the command:
```python -m venv <name-of-your-virtual-environment>```

Note: If you are getting UnauthorizedAccessError like given in the screenshot below, run the command ```Set-ExecutionPolicy Unrestricted -Scope Process``` before running any Python command.

<img width="752" alt="image" src="https://github.com/user-attachments/assets/01059486-4af7-40e7-aa02-860f1e58dd3d">

On Gemini machines, you have restrictions to set execution policy for the current session only, so make sure to execute this command each session.

### On Unix or MacOS
```bash
python3 -m venv venv
```
### On Windows
```bash
python -m venv venv
```

## 2. Activate the Virtual Environment

### On Unix or MacOS

```bash
source venv/bin/activate
```

### On Windows
```bash
venv\Scripts\activate
```
## 3. install python libs 
```bash 
pip install -r requirements.txt
```

# Run Streamlit App:
Follow steps 1 to 3 then run

```bash
  streamlit run main.py
  ```
In case this doesn't work, run
```bash
python -m streamlit run main.py
```
