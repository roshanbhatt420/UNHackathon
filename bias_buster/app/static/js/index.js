document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("fileInput");
  const checkBtn = document.getElementById("checkFairnessBtn");
  const analysisResults = document.getElementById("analysisResults");
  const msgBox = document.getElementById("msgBox");
  const fileName = document.getElementById("fileName");

  let msgTimeout; // to track and clear previous timeouts

  // Drag & Drop
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  function showMsg(text, status = "success", isTemporary = false) {
    clearTimeout(msgTimeout); // This clears old timers
    msgBox.classList.remove("hidden", "success", "error");
    msgBox.classList.add(status);
    fileName.textContent = text;
  
    if (isTemporary) {
      msgTimeout = setTimeout(() => {
        msgBox.classList.add("hidden");
        msgBox.classList.remove("success", "error");
        fileName.textContent = "";
      }, 4000);
    }
  }
  
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
  
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".csv")) {
      fileInput.files = e.dataTransfer.files;
      showMsg(`Uploaded: ${file.name}`, "success", false); 
    } else {
      showMsg("Please upload a valid CSV file.", "error", false); 
    }
  });
  
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith(".csv")) {
      showMsg(`Uploaded: ${file.name}`, "success", false); 
    } else {
      showMsg("Please select a valid CSV file.", "error", false); 
    }
    });
  
    // Check Fairness
    checkBtn.addEventListener("click", () => {
    if (!fileInput.files.length) {
      showMsg("Please upload a file first!", "error", false); // stay there
      return;
    }
  
    setTimeout(() => {
      analysisResults.classList.remove("hidden");
      showMsg("Analysis completed!", "success", true); // The success message will be hidden after a timeout
    }, 1000);
    });
  

  
  }
);
