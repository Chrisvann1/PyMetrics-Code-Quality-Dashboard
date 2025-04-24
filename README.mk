# PyMetrics

## Welcome!

  

PyMetrics is a code quality metric dashboard where users can select a folder with Python files from their computer and run code quality metrics on them. The current available metrics are as follows:

- Cyclomatic Complexity: The number of decision points in a code base\

- Code Documentation: The percentage of code that is documented\

- Code Style: Adherence to established code practices and standards\

## What You Will Need

PyMetrics requires Python version 3.7 or later, and uses the following modules:

- Flask

- Radon

- pycodestyle


## How to Use 

### Installation 

First, download all the project files and store them in a directory of your choice. You will run the api.py Python file, which runs the API and allows you to access the dashboard. 

Specifically, run the following command in the terminal of the directory the project is located: 

```
python api.py
```

### Accessing the dashboard 

After the server is active, you can access the dashboard by using the following link in a search engine: 
```
http://127.0.0.1:5000
```

This link can also be found in the terminal.

### Utilizing the dashboard 

##### Home Page: 

The home page of the dashboard will be available immediately after accessing the link. Here you can learn about the importance of code quality, find information about the available metrics on the dashboard, and click the big green button to access the "Metric Page" where you can run metrics on your code. 

##### Metric Page: 

Here is the page where you can run code quality metrics on your code. You simply need to click the button that says "Select Folder & Run Metrics" and select the folder of Python files that you want to run metrics on. It is important to note that this dashboard exclusively works on Python files and will skip all files that are not Python files. 

The metric scores on this page will range from 0-100, with 0 being the worst score and 100 being the best. 

### Project Structure 

Project Structure:
- api.py
- README.mk
- /static
  - javascript.js
  - style.css
- /templates
  - home.html
  - metrics.html

### File Descriptions

- `api.py` - The main Flask application that runs the backend server and handles metric calculations.
- `/static/javascript.js` - Handles interactivity, such as button clicks and file uploads.
- `/static/style.css` - Styling for the dashboard UI.
- `/templates/home.html` - The homepage with project introduction and navigation.
- `/templates/metrics.html` - The page for uploading Python files and displaying metric results.

- `test_metrics.py` - A python file that tests the metric functions to see if they are working as intended 
  - How to use: Type "pytest" into terminal of this project's main directory


### Contact Information 
Email: Christopherdvann123@gmail.com






