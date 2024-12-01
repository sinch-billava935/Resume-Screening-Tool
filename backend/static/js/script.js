// Handle Form Submission
document.getElementById("resumeForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const fileInput = document.getElementById("resumeUpload").files[0];
  const jobRole = document.getElementById("jobRole").value;

  if (!fileInput || !jobRole) {
    alert("Please upload a resume and specify a job role.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", fileInput);
  formData.append("jobRole", jobRole);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      updateResults(data);
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
  document.getElementById("parsedJobRole").innerText = data.jobRole || "N/A";
  document.getElementById("age").innerText = data.age || "N/A";

  // Update Score
  document.getElementById("candidateScore").innerText = data.score || "N/A";

  // Update Verdict
  const verdictMessage = data.score >= 70 ? "Candidate is Selected!" : "Candidate is Not Selected.";
  document.getElementById("resultMessage").innerText = verdictMessage;

  // Generate Graph
  createGraph(data.skills, data.jobRequirements);
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
      },
      {
        label: "Job Requirements",
        data: jobData,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
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
