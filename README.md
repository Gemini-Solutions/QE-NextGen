# summary_generator_flask
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

## 3. If you get any error while creating the virtual environment, run
```Set-ExecutionPolicy Unrestricted -Scope Process``` command
