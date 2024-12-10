document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const qualificationChartCanvas = document.getElementById("qualificationChart").getContext("2d");

  let chart; // Declare a variable for the chart

  uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(uploadForm);

      try {
          const response = await fetch('/analyze', {
              method: 'POST',
              body: formData
          });

          const data = await response.json();
          if (data.error) {
              alert(data.error);
              return;
          }

          // Update basic information
          document.getElementById("name").textContent = data.name || 'N/A';
          document.getElementById("email").textContent = data.email || 'N/A';
          document.getElementById("parsedJobRole").textContent = data.job_role || 'N/A';
          document.getElementById("phone").textContent = data.phone || 'N/A';

          // Update skills
          document.getElementById("skills-list").textContent = data.skills.join(', ') || 'N/A';

          // Update experience
          const experienceList = document.getElementById("experience-list");
          experienceList.innerHTML = '';
          data.experience.forEach(exp => {
              const listItem = document.createElement("li");
              listItem.textContent = exp;
              experienceList.appendChild(listItem);
          });

          // Update education
          document.getElementById("education-info").textContent = data.education || 'N/A';

          // Update scores and verdict
          document.getElementById("candidateScore").textContent = data.overall_score || 'N/A';
          document.getElementById("resultMessage").textContent = data.verdict || 'N/A';

          // Prepare chart data for candidate and job requirements
          const candidateScores = [
            data.skill_score, // Candidate's skill score from backend
            data.experience_score, // Candidate's experience score from backend
            data.education_score // Candidate's education score from backend
          ];
          
          // Job requirement scores logic:
          const jobRequirementScores = [
            // Skill score: Based on the maximum skill score (50) as defined in backend
            data.job_requirements.required_skills.length > 0 
              ? 50 // Max skill score is fixed at 50
              : 0,
          
            // Experience score: Based on the maximum experience score (30) as defined in backend
            data.job_requirements.required_experience > 0 
              ? data.job_requirements.required_experience * (30 / data.job_requirements.required_experience) 
              : 0,
          
            // Education score: Fixed at 20 as maximum education score
            data.education_score > 0 
            ? (data.education_score / 20) * 20 // Normalize fuzzy match score to max education score
            : 0
          ];
          

          // Destroy existing chart if present
          if (chart) {
              chart.destroy();
          }

          // Create new chart with updated data
          chart = new Chart(qualificationChartCanvas, {
              type: 'line',
              data: {
                  labels: ['Skills', 'Experience', 'Education'],
                  datasets: [
                      {
                          label: 'Candidate Qualifications',
                          data: candidateScores,
                          borderColor: 'rgba(75, 192, 192, 1)',
                          backgroundColor: 'rgba(75, 192, 192, 0.3)', // Add fill color for the area
                          borderWidth: 2,
                          fill: true, // Fill the area under the line
                          tension: 0.4 // Smooths the line
                      },
                      {
                          label: 'Job Requirements',
                          data: jobRequirementScores,
                          borderColor: 'rgba(255, 99, 132, 1)',
                          backgroundColor: 'rgba(255, 99, 132, 0.3)', // Add fill color for the area
                          borderWidth: 2,
                          fill: true, // Fill the area under the line
                          tension: 0.4 // Smooths the line
                      }
                  ]
              },
              options: {
                  responsive: true,
                  scales: {
                      y: {
                          beginAtZero: true,
                          max: 100,
                          title: {
                              display: true,
                              text: 'Score (%)'
                          }
                      },
                      x: {
                          title: {
                              display: true,
                              text: 'Category'
                          }
                      }
                  },
                  plugins: {
                      legend: {
                          display: true
                      },
                      tooltip: {
                          mode: 'index',
                          intersect: false
                      }
                  }
              }
          });

      } catch (error) {
          alert('An error occurred: ' + error);
      }
  });
});
