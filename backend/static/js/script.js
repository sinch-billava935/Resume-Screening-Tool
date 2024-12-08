// Handle Form Submission
document.getElementById("resumeForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission

  // Get user inputs
  const fileInput = document.getElementById("resumeUpload").files[0];
  const jobRole = document.getElementById("jobRole").value;

  if (!fileInput || !jobRole) {
    alert("Please upload a resume and specify a job role.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", fileInput);
  formData.append("job_role", jobRole);

  // Send form data to the backend
  fetch("/analyze", {
    method: "POST",
    body: formData,
  })
<<<<<<< HEAD
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
=======
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
>>>>>>> 54dda24779567580eecf4d361aac8b45fe727649
      } else {
        updateResults(data);
      }
<<<<<<< HEAD
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while processing the resume.");
    });
});

// Update Results
function updateResults(data) {
  // Update Basic Info
  document.getElementById("name").innerText = data.name || "N/A";
  document.getElementById("email").innerText = data.email || "N/A";
  document.getElementById("parsedJobRole").innerText = data.job_role || "N/A";
  document.getElementById("age").innerText = data.age || "N/A";

  // Update Score
  document.getElementById("candidateScore").innerText = data.score || "N/A";

  // Update Verdict
  const verdictMessage = data.score >= 70 ? "Candidate is Selected!" : "Candidate is Not Selected.";
  document.getElementById("resultMessage").innerText = verdictMessage;

  // Generate Graph
  if (data.skills && data.job_requirements) {
    createGraph(data.skills, data.job_requirements);
  } else {
    alert("No data available for graph visualization.");
  }
}

// Generate Graph
function createGraph(candidateSkills, jobRequirements) {
  const labels = Object.keys(candidateSkills);
  const candidateData = Object.values(candidateSkills);
  const jobData = Object.values(jobRequirements);

  const data = {
    labels: labels,
    datasets: [
      {
        label: "Candidate Skills",
        data: candidateData,
        backgroundColor: "rgba(75, 192, 192, 0.5)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
      {
        label: "Job Requirements",
        data: jobData,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const ctx = document.getElementById("resultGraph").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Candidate Skills vs Job Requirements" },
      },
    },
  });
}
=======

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
>>>>>>> 54dda24779567580eecf4d361aac8b45fe727649
