//Intializes graph
let chart = null;

// Function allows user to select a folder of Python files 
// and display their metrics on the dashboard
async function InsertFolderAndRun() {

    //Allows selection of folder from directory
    const folder = await window.showDirectoryPicker();
    let files = []; 


    //FormData object to access file information on backend
    const formData = new FormData();


    //Iterates through all the files in the folder and stores in an array called files if the file name ends with .py
    //folder.values - all the files from the directory you picked 
    //fileHandle - variable holding the file we are on while iterating through the directory folder
    for await (const fileHandle of folder.values()) {
        if (fileHandle.name.endsWith('.py')) {
            //reads file
            const file = await fileHandle.getFile(); 
            files.push(file);
            formData.append('files', file, fileHandle.name);
        }
    }

    //Edge case for if a folder has no Python files - inform the user and destroy the chart
    if (files.length == 0) {
        document.getElementById("overall_score").innerText = "No Python files in the folder.";
        document.getElementById("metric_scores1").innerText = "";
        document.getElementById("metric_scores2").innerText = "";
        document.getElementById("metric_scores3").innerText = "";
        
        if (chart) {
            chart.destroy();
        }
        return;
    }


    //Sends the files to the Python backend (using flask)
    const response = await fetch('http://127.0.0.1:5000/get-folder', {
        method: 'POST', 
        body: formData,
    });

    //Sends scores to console of website
    const all_scores = await response.json();
    console.log(all_scores);


    //Puts metric score information on actual dashboard (not just console)
    document.getElementById("overall_score").innerText = "PyMetrics Score: " + all_scores.overall_score.toFixed(2);
    document.getElementById("metric_scores1").innerText = "Cyclomatic Complexity Score: " + all_scores.metric_scores[0].toFixed(2);
    document.getElementById("metric_scores2").innerText = "Documentation Quality Score: " + all_scores.metric_scores[1].toFixed(2);
    document.getElementById("metric_scores3").innerText = "Code Style Score: " + all_scores.metric_scores[2].toFixed(2);



    //Creates ID so that the graph can be accessed via HTML and specifies 2D chart
    //(Needed to "draw" on website)
    const graph_information = document.getElementById('metricGraph').getContext('2d')
    
    //Bar Graph details
    const graph = {
        type: 'bar',
        labels: ['Cyclomatic Complexity', 'Documentation Quality', 'Code Style'],
        datasets: [{
            data: all_scores.metric_scores,
            borderColor: '#008000',
            backgroundColor: '#4CAF50',
        }]
    };

    const options = {
        plugins: {
        legend: {
            display: false},
        title: {
            display: true,  
            text: 'Metric Scores Bar Graph',
            font: {
                size: 24,
            },
            color: '#556b2f',
        },
    },
        
  scales: {
    y: {
      beginAtZero: true,
      //max will always be 100 on this scale
      max: 100,
      title: {
        display: true, 
        text: 'Individual Score Averages'
      }
    },
    x: {
        title : {
            display: true,
            text: 'Metrics'
        },
      }
  },
};

    //need this to reset the graph information if you use another file by destroying the old chart 
    if (chart) {
        chart.destroy();
    }
    
    //creates an instance that allows you to render the chart on the website
    chart = new Chart(graph_information,
    {
        type: 'bar', 
        data: graph,
        options: options,
    });

}
