document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault();

  var formData = new FormData();
  var resumeFile = document.getElementById('resume').files[0];
  var jobRole = document.getElementById('job_role').value;

  formData.append('resume', resumeFile);
  formData.append('job_role', jobRole);

  fetch('/analyze', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert('Error: ' + data.error);  // Show an error alert if backend returns an error
    } else {
      // Populate the parsed information into the frontend
      document.getElementById('name').textContent = data.name || 'N/A';  // Set name
      document.getElementById('email').textContent = data.email || 'N/A';  // Set email
      document.getElementById('parsedJobRole').textContent = data.job_role || 'N/A';  // Set job role
      document.getElementById('phone').textContent = data.phone || 'N/A';  // Set phone number

      // Display skills
      document.getElementById('skills-list').textContent = data.skills ? data.skills.join(', ') : 'N/A';  // Set skills list

      // Calculate and display score (this can be customized based on your model logic)
      var score = data.score || 0;
      document.getElementById('candidateScore').textContent = score + "/100";  // Display score

      // Display verdict based on score
      document.getElementById('resultMessage').textContent = score >= 75 ? 'Selected' : 'Not Selected';  // Set verdict
    }
  })
  .catch(error => {
    alert('Error: ' + error);  // Show an error alert if there's a network or fetch error
  });
});
