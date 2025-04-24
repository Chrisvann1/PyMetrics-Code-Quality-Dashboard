from flask import Flask, request, jsonify,render_template
import radon.complexity as radon_cc
import pycodestyle


dashboard = Flask(__name__, static_folder="static", template_folder='templates')

#home
@dashboard.route('/')
def HomePage(): 
    return render_template('home.html')

#metric page 
@dashboard.route('/metrics')
def MetricPage(): 
    #Allows you to dynamically use the metrics html page 
    #allowing it to be accessible whenever you run the flask 
    #flask framework
    return render_template('metrics.html')


#This function is used to take get the formdata object from the javascript code, decode it into 
# a readable string, call the RunMetrics functions to calculate the score of each individual file, 
# add all of the individual scores of each metric together, calculate an average for each metric score, 
# and calculate an overall score which is the average of the individual score averages
#Metrics[0] = Cyclomatic Complexity
#Metrics[1] = Documentation 
#Metrics[2] = Code Style
@dashboard.route('/get-folder', methods=['POST'])
def GetFolder():
    files = request.files.getlist('files')
    metrics = [0,0,0] 
    total = 0

    number_of_files = len(files)
    if number_of_files > 0: 
        for file in files: 
            #Decodes the form data back into readable text (python string)
            content = file.read().decode('utf-8')
            scores = RunMetrics(content)
            for x in range(len(scores)): 
                metrics[x] += scores[x]

    #Gets the averages by keeping track of the number of files and 
    #their scores Then it adds this value on to the total score so we can get the 
    #total of all the files
    if number_of_files > 0: 
        for x in range(len(metrics)): 
            metrics[x] = metrics[x] / number_of_files
            total += metrics[x]

        overall_score = sum(metrics) / len(metrics)

    else: 
        metrics = [0,0,0]
        overall_score = 0

    print(metrics)
    print(overall_score)
    return jsonify({
        'metric_scores': metrics,
        'overall_score': overall_score
        })

#Used to calculate cyclomatic complexity of methods, classes, and functions
#It just counts how many decision points there are in a function 
#The simpler the code the higher the score
def cyclomatic_score(file): 
    code_blocks = radon_cc.cc_visit(file)

    if not code_blocks: 
        return 100

    complexity_of_file = 0
    for block in code_blocks: 
        complexity_of_file += block.complexity

    #Calculates the average complexity for the blocks in a given file (needed to figure out score)
    average_complexity_of_block = complexity_of_file / len(code_blocks)

    # Perfect Score: 1-5 decision points 
    if average_complexity_of_block <= 5: 
        return 100
    cyclomaticScore = 100 - (average_complexity_of_block - 5) * 4

    #0 is the minimum 
    if cyclomaticScore < 0: 
        cyclomaticScore = 0
    
    return round(cyclomaticScore, 2)

#Calculates documentation score of each file 
#by counting the number of comment lines and docstrings 
#and then comparing this to the number of functions and classes
def documentation_score(file):
    #Makes each line of code an element of a list
    lines = file.splitlines()

    function_count = 0 
    class_count = 0

    docstring_count = 0
    comment_count = 0

    for line in lines: 
        if line.strip().startswith("def "): 
            function_count += 1
        if line.strip().startswith("class "):
            class_count += 1

        #checks for docstring
        if line.strip().startswith('"""') or line.strip().startswith("'''"):
            docstring_count += 1
        
        #looks for comments
        if line.strip().startswith("#"): 
            comment_count += 1

    total = function_count + class_count 
    if total == 0: 
        return 100
    

    docstring_to_total_ratio = 1 - (docstring_count / total)
    comment_to_total_ratio = 1 - (comment_count / total)

    entire_ratio = (docstring_to_total_ratio + comment_to_total_ratio) / 2

    dScore = 100 - (entire_ratio * 100)

    #100 is the max score
    if dScore > 100: 
        dScore = 100 

    return round(dScore, 2)


#Calculates code style score of each file
#by counting number of errors according to PEP 8 standards
def code_style_score(file): 

    #Creates a list of lines from the file
    list_of_lines = file.splitlines()
    if not list_of_lines: 
        return 100
    
    #check if each line is an empty string, if so return 100
    empty_lines = True 
    for line in list_of_lines: 
        if line.strip() != '':
            empty_lines = False 
            break 

    if empty_lines: 
        return 100

    #This creates a pycodestyle object which allows us to check the 
    #total number of errors in the following line 
    check_style = pycodestyle.Checker(filename = '<string>', lines=list_of_lines)

    #Checks PEP 8 style errors
    check_errors = check_style.check_all()

    #Counts number of elements in the list_of_lines list
    number_of_lines = len(list_of_lines)
    if number_of_lines == 0: 
        return 100

    #checks the ratio between the number of errors and number of lines
    error_rate = check_errors / number_of_lines

    codeScore = 100 - (error_rate * 100)
    if codeScore < 0: 
        codeScore = 0

    return round(codeScore, 2)

#Calls each of the individual metric functions and returns their scores as a list
def RunMetrics(file):
    # I needed to make sure each variable was initalized even if there was an error 
    # So I just used try statements that would try to use the function 
    # and if there was an error
    try: 
        cyclomatic_complexity_score = cyclomatic_score(file)

    #checks for syntax errors and other things the program cannot not handle
    except (SyntaxError, Exception) as file_error: 
        print("Cyclomatic score error for file", file_error)
        cyclomatic_complexity_score = 0

    try: 
        document_score = documentation_score(file)
    except (SyntaxError, Exception) as file_error: 
        print("Documentation score error for file", file_error)
        document_score = 0

    try: 
        code_style = code_style_score(file)
    except (SyntaxError, Exception) as file_error: 
        print("Code Style score error for file", file_error)
        code_style = 0


    metricScores = [cyclomatic_complexity_score, document_score, code_style]

    return metricScores

#Locally hosted
if __name__ == '__main__':
    dashboard.run(debug=True, host="127.0.0.1")