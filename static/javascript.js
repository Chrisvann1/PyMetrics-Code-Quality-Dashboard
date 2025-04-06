async function InsertFolderAndRun() {
    //Allows me to select a folder from my directory
    const folder = await window.showDirectoryPicker();
    let files = []; 


    //Allows you to create FormData object 
    //to send the files themselves rather than 
    //their names/paths (which I was trying to do before)
    const formData = new FormData();


    //Iterates through all the files in the folder 
    //and stores in an array called files if the file 
    //name ends with .py
    //Await allows you to pause the execution of the for loop
    //until the iteration is complete
    for await (const fileHandle of folder.values()) {
        if (fileHandle.name.endsWith('.py')) {
            const file = await fileHandle.getFile();  // Read file
            files.push(file);
            formData.append('files', file, fileHandle.name);  // Append to FormData
        }
    }


    if (files.length == 0) {
        console.log("No Python files")
        return; 
    }


    //Sends the files to the Python backend (using flask)
    const response = await fetch('http://127.0.0.1:5000/get-folder', {
        method: 'POST', 
        body: formData,
    });

    //Allows you to take the metric scores calculated with python 
    //and send them to the console of the website
    const all_scores = await response.json();
    console.log(all_scores);

    //allows you to use the metric_score information and put the text on the actual website
    //rather than just the console
    document.getElementById("overall_score").innerText = "PyMetrics Score: " + all_scores.overall_score.toFixed(2);
    document.getElementById("metric_scores1").innerText = "Score 1: " + all_scores.metric_scores[0].toFixed(2);
    document.getElementById("metric_scores2").innerText = "Score 2: " + all_scores.metric_scores[1].toFixed(2);
    document.getElementById("metric_scores3").innerText = "Score 3: " + all_scores.metric_scores[2].toFixed(2);


    //Needed to "draw" on the website and specifies that you will be using a 
    //2D chart. This is also needed to create an ID so that the chart can be accessed via HTMl code
    const graph_information = document.getElementById('metricGraph').getContext('2d')
    //creates the chart
    const graph = {
        type: 'bar',
        labels: ['Metric 1', 'Metric 2', 'Metric 3'],
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


    //creates an instance that allows you to render the chart 
    //on the website
    chart = new Chart(graph_information,
    {
        type: 'bar', 
        data: graph,
        options: options,
    });

}
