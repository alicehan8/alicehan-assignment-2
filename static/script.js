document.addEventListener('DOMContentLoaded', () => {
  let currentStep = 0
  let totalSteps = 0

  function initializeVisual() {
    console.log("initializing");
    // const numPoints = document.getElementById('numPoints').value || 300;
    const url = `/initialize`;

    const img = document.getElementById('data-visualization');
    img.src = url;
    img.style.display = 'block'; // Show the image
  }

  document.getElementById('runKMeans').addEventListener('click', () => {
    const kClusters = document.getElementById('nClusters').value;
    const initMethod = document.getElementById('initMethod').value;

    const images = [];

    // Create the URL for the initial generation request
    const url = `/kmeans?k=${kClusters}&init_method=${initMethod}`;

    // Make an AJAX request to get the total steps from the server
    fetch(url)
      //.then(response => response.text()) // Assuming the server returns a plain text with totalSteps
      .then(response => response.json())
      .then(data => {
        console.log(respponse);
        //totalSteps = parseInt(data, 10); // Convert the response to an integer
        images = data.images || [];
        totalSteps = data.steps;
        if (isNaN(totalSteps)) {
          console.error("Failed to retrieve total steps from the server.");
          return;
        }
        for (const im in images) {
          updateVisualization(im);
        }
      })
      .catch(error => console.error("Error during initialization:", error));

  });

  function updateVisualization(im) {
    const img = document.getElementById('data-visualization');

    // Add a timestamp to the URL to prevent caching
    const timestamp = new Date().getTime();
    img.src = `${im}`;

    img.style.display = 'block'; // Show the image
  }

  document.getElementById('runToConvergence').addEventListener('click', () => {
    if (currentStep == 0) {
      const kClusters = document.getElementById('nClusters').value;
      const initMethod = document.getElementById('initMethod').value;

      // Create the URL for the initial generation request
      const url = `/generate?k=${kClusters}&init_method=${initMethod}`;

      // Make an AJAX request to get the total steps from the server
      fetch(url)
        .then(response => response.text()) // Assuming the server returns a plain text with totalSteps
        .then(data => {
          totalSteps = parseInt(data, 10); // Convert the response to an integer
          if (isNaN(totalSteps)) {
            console.error("Failed to retrieve total steps from the server.");
            return;
          }
          // Start the visualization process
          currentStep = totalSteps;
          updateVisualization();
        })
        .catch(error => console.error("Error during initialization:", error));
    }

  });

  document.getElementById('generateData').addEventListener('click', () => {
    // const numPoints = document.getElementById('numPoints').value || 300;

    const url = `/generate_data?t=${new Date().getTime()}`;

    const img = document.getElementById('data-visualization');
    img.src = "";
    img.src = url;
    img.style.display = 'block';

  });


  function resetAlgorithm() {
    const url = `/reset`;

    const img = document.getElementById('data-visualization');
    img.src = "";
    img.src = url;
    img.style.display = 'block';
  }

  window.onload = function () {
    initializeVisual();
  };

});