const debugBtn = document.getElementById("debugBtn");

debugBtn.addEventListener("click", async () => {

  const code = document.getElementById("code").value;
  const error = document.getElementById("error").value;

  const result = document.getElementById("result");
  const loading = document.getElementById("loading");

  // Clear previous result
  result.innerText = "";

  // Show loading
  loading.style.display = "block";

  try {

    const response = await fetch("https://ai-java-debugger-backend.onrender.com/debug"), {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        code: code,
        error: error
      })

    });

    const data = await response.json();

    // Hide loading
    loading.style.display = "none";

    // Display AI result
    if (data.result) {

      result.innerText = data.result;

    } else if (data.error) {

      result.innerText = "❌ " + data.error;

    } else {

      result.innerText = "Something went wrong";

    }

  } catch (err) {

    loading.style.display = "none";

    result.innerText = "❌ Cannot connect to backend";

    console.log(err);

  }

});