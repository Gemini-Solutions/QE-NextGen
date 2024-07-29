# NextGen
NextGen is a Python-based AI project that takes URL/DOM structure from the user and generates the Gherkin files, Step definition, and Implementation file for the user to reduce the manual intervention of the Quality Engineers.

## Steps to run NextGen on your system:
### 1. Install VS Code as IDE
Download VS Code from this [link](https://code.visualstudio.com/docs/?dv=win64user). If you are getting an Unverified download blocked error (refer to the image below)

<img width="323" alt="image" src="https://github.com/user-attachments/assets/447d5f9c-1211-48f1-8be1-957d49b5dd44">

open the unloaded file and click on Download unverified file to continue (refer to the image below)
<img width="560" alt="image" src="https://github.com/user-attachments/assets/73d248f8-03ce-4114-9727-651f05b8a937">

### 2. Install Python
Make sure you have Python installed on your system. Run the command given below in CMD to verify.
```bash
python --version
```

<img width="410" alt="image" src="https://github.com/user-attachments/assets/855526c2-5e2d-443e-8232-fdb922223f27">

If the command does not return the Python version, install Python from ManageEngine Desktop Central.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/4fbd43a2-5fb2-4a4a-9704-6612bf63bd07">

### 3. Install extensions that will support you while working on Python in VS Code.
### 4. Create an .env file and add a ChatGPT key there. Ask for the Key's value in DM.
```bash
NextGenKey = "value of key"
```
Note: Make sure that this key is never exposed. If `.gitignore` file does not ignore the `.env` file, make sure to add it before pushing your code

### 5. Create a virtual environment by using the command:
```bash
python -m venv <name-of-your-virtual-environment>
```

**Note:** If you are getting UnauthorizedAccessError like given in the screenshot below, run the following command before running any other Python command.
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
``` 

<img width="752" alt="image" src="https://github.com/user-attachments/assets/01059486-4af7-40e7-aa02-860f1e58dd3d">

On Gemini machines, you have restrictions to set execution policy for the current session only, so make sure to execute this command each session.

### 6. Activate your virtual environment by running the following command:
```bash
venv\Scripts\activate
```
Note: 
1. Never install any library without activating the virtual environment.
2. You will be able to see the name of your virtual environment at the beginning of the terminal's command line interface.

### 7. Install required Python libraries by running the command given below:
```bash 
pip install -r requirements.txt
```

### To run the application, activate the Streamlit App by running the command given below:
```bash
python -m streamlit run main.py
```
## Some other important pointers to note:
1. Create your branch from `develop` branch to make the changes.
2. Never push anything before raising a Peer Review request
3. The API key is intended to be used for this project only.
