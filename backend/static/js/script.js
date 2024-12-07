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
      alert('Error: ' + data.error);
    } else {
      // Populate parsed information into the frontend
      document.getElementById('name').textContent = data.name || 'N/A';
      document.getElementById('email').textContent = data.email || 'N/A';
      document.getElementById('parsedJobRole').textContent = data.job_role || 'N/A';  // Display the job role here
      document.getElementById('phone').textContent = data.phone || 'N/A';

      // Ensure data.skills is an array before using .join
      const skillsList = data.skills && Array.isArray(data.skills) ? data.skills.join(', ') : 'N/A';
      document.getElementById('skills-list').textContent = skillsList;

      // Display experience as a list
      var experienceList = document.getElementById('experience-list');
      experienceList.innerHTML = '';  // Clear previous content
      if (Array.isArray(data.experience) && data.experience.length > 0) {
        data.experience.forEach((point) => {
          var li = document.createElement('li');
          li.textContent = point;
          experienceList.appendChild(li);
        });
      } else {
        experienceList.innerHTML = '<li>N/A</li>';
      }

      // Display education
      document.getElementById('education-info').textContent = data.education || 'N/A';

      // Display qualification graph
      displayQualificationGraph(data.skill_score, data.education_score, data.experience_score, data.job_requirements);

      // Display overall score and verdict
      document.getElementById('candidateScore').textContent = `${data.overall_score}/100`;
      document.getElementById('resultMessage').textContent = data.verdict;
    }
  })
  .catch(error => {
    alert('Error: ' + error.message); // Handle fetch errors
  });
});

// Function to display qualification comparison graph
function displayQualificationGraph(skillScore, educationScore, experienceScore, jobRequirements) {
  const ctx = document.getElementById('qualificationChart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Skills', 'Education', 'Experience'],
      datasets: [
        {
          label: 'Candidate Qualification',
          data: [skillScore, educationScore, experienceScore],
          borderColor: 'blue',
          backgroundColor: 'rgba(0, 0, 255, 0.3)',
          fill: true,
          tension: 0.3
        },
        {
          label: 'Job Requirements',
          data: jobRequirements,
          borderColor: 'red',
          backgroundColor: 'rgba(255, 0, 0, 0.3)',
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Qualification vs Job Requirements' }
      },
      scales: {
        y: { beginAtZero: true, max: 100 }
      }
    }
  });
}
