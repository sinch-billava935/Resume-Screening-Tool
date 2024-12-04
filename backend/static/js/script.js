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
      // Show error message on the page instead of alert
      document.getElementById('resultMessage').textContent = 'Error: ' + data.error;
    } else {
      // Populate the parsed information into the frontend
      document.getElementById('name').textContent = data.name || 'N/A';
      document.getElementById('email').textContent = data.email || 'N/A';
      document.getElementById('parsedJobRole').textContent = data.job_role || 'N/A';
      document.getElementById('phone').textContent = data.phone || 'N/A';

      // Display skills
      document.getElementById('skills-list').textContent = data.skills ? data.skills.join(', ') : 'N/A';

      // Display experience as bullet points
      var experienceList = document.getElementById('experience-list');
      experienceList.innerHTML = '';  // Clear previous content
      if (Array.isArray(data.experience) && data.experience.length > 0) {
        data.experience.forEach(point => {
          var li = document.createElement('li');
          li.textContent = point;
          experienceList.appendChild(li);
        });
      } else {
        experienceList.innerHTML = '<li>N/A</li>';
      }

      // Display education
      document.getElementById('education-info').textContent = data.education || 'N/A';

      // Calculate and display score (this can be customized based on your model logic)
      var score = data.score || 0;
      document.getElementById('candidateScore').textContent = score + "/100";

      // Display verdict based on score
      document.getElementById('resultMessage').textContent = score >= 75 ? 'Selected' : 'Not Selected';
    }
  })
  .catch(error => {
    document.getElementById('resultMessage').textContent = 'Error: ' + error.message;
  });
});
