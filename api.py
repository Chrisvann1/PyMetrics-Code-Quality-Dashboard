from flask import Flask, request, jsonify,render_template
import radon.complexity as radon_cc
import pycodestyle
from io import StringIO


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




#VERY IMPORTANT INFORMATION ABOUT THE METRICS LIST BELOW|
#                                                       |
#                                                       |    
#Metrics[0] = 
#Metrics[1] = 
#Metrics[2] = 

@dashboard.route('/get-folder', methods=['POST'])
def GetFolder():
    files = request.files.getlist('files')
    metrics = [0,0,0] 
    total = 0

    number_of_files = len(files)
    if number_of_files > 0: 
        for file in files: 
            #Decodes the form data back into readable text that 
            #consists of strings which looks like the original python code
            content = file.read().decode('utf-8')
            #Calls run_metrics and goes through each file and 
            #adds their scores to each individual metric score
            #Scores will be a list (to make it easier this list will be in the same order
            #as the metric list for the metrics)
            scores = RunMetrics(content)
            for x in range(len(scores)): 
                metrics[x] += scores[x]

    #Gets the averages by keeping track of the number of files and 
    #their scores
    #Then it adds this value on to the total score so we can get the 
    #total of all the files
    if number_of_files > 0: 
        for x in range(len(metrics)): 
            metrics[x] = metrics[x] / number_of_files
            total += metrics[x]

        #Finds the overall score by finding the average of all individual metrics 
        #divides the sum of the metrics by how many metrics there are
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


def cyclomatic_score(file): 
    pass

def documentation_score(file):
    pass

def code_style_score(file): 
    pass

def RunMetrics(file):
    cyclomatic_complexity_score = cyclomatic_score(file)
    document_score = documentation_score(file)
    code_style = code_style_score(file)

    metricScores = [cyclomatic_complexity_score, document_score, code_style]
    return [20,50,85]

if __name__ == '__main__':
    #127.0.0.1 means its locally hosted
    #meaning you can only run the dashboard on the same computer that flask is running 
    #0.0.0.0 if I want it for all other devices on the same network (NOT RELEVANT FOR THIS PROJECT)
    dashboard.run(debug=True, host="127.0.0.1")