// Sample Data
const labels = ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5"];
const jobRequirements = [80, 90, 70, 60, 50]; // Job requirements percentage
const candidateSkills = [70, 85, 65, 40, 60]; // Candidate match percentage

const data = {
  labels: labels,
  datasets: [
    {
      label: "Job Requirements",
      data: jobRequirements,
      backgroundColor: "rgba(54, 162, 235, 0.5)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    },
    {
      label: "Candidate Skills",
      data: candidateSkills,
      backgroundColor: "rgba(75, 192, 192, 0.5)",
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 1,
    },
  ],
};

const config = {
  type: "bar", // Change to "line" for a line chart
  data: data,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Candidate Skills vs. Job Requirements",
      },
    },
  },
};

// Render Chart
const ctx = document.getElementById("resultGraph").getContext("2d");
new Chart(ctx, config);
