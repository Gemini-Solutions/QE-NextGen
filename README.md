# NextGen
NextGen is a Python-based AI project that takes URL/DOM structure from the user and generates the Gherkin files, Step definition and Implementation file for the user to reduce the manual intervention of the Quality Engineers.

## Steps to run NextGen on your system:
### 1. Install VS Code as IDE
Download VS Code from this [link](https://code.visualstudio.com/docs/?dv=win64user). If you are getting an Unverified download blocked error, <img width="323" alt="image" src="https://github.com/user-attachments/assets/447d5f9c-1211-48f1-8be1-957d49b5dd44">, open the unloaded file and click on Download unverified file to continue <img width="560" alt="image" src="https://github.com/user-attachments/assets/73d248f8-03ce-4114-9727-651f05b8a937">


## 1. Create a Virtual Environment

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
