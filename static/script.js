document.getElementById("upload-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("pdf-file");
    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    let formData = new FormData();
    formData.append("pdf", fileInput.files[0]);

    document.getElementById("loading").style.display = "block";
    
    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        document.getElementById("loading").style.display = "none";

        if (response.ok) {
            let quizContainer = document.getElementById("quiz-container");
            quizContainer.innerHTML = "<h2>Generated Quiz</h2><pre>" + result.quiz + "</pre>";
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        document.getElementById("loading").style.display = "none";
        alert("Failed to connect to server.");
    }
});