# topkek-

You need Python 3 and pip installed to set up this project.

Navigate to the project repository and do this to set up the python virtual environment and enable it:

```
python3 -m venv venv
source venv/bin/activate
```

Run `run.sh` to launch the Flask server. It is configured to run the server on `http:127.0.0.1:5001` by default.

Configuration can be done by adding variables to `instance/config.py`.

For testing, first do `pip install pytest coverage`. Run `pip install -e .` to install the project in the local virtual environment (the `-e` ensures that it is updated as the project is modified). Run `pytest` to run all tests. Run `coverage run -m pytest` to generate a code coverage report. Run `coverage report` to get the report in the command line, or run `coverage html` to generate an interactive HTML page in `htmlcov/index.html`.
