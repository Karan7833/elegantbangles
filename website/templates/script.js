document.getElementById("contactForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const submitBtn = e.target.querySelector('button[type="submit"]');
  const successMsg = document.getElementById("successMessage");

  submitBtn.classList.add("loading");
  submitBtn.disabled = true;
  successMsg.classList.remove("show");

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    message: document.getElementById("message").value
  };

  try {
    const res = await fetch("http://localhost:5000/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    successMsg.textContent = result.message;
    successMsg.classList.add("show");
  } catch (err) {
    alert("Something went wrong. Try again later.");
  } finally {
    submitBtn.classList.remove("loading");
    submitBtn.disabled = false;
  }
});
