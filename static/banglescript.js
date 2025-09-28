
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eye = document.getElementById('eyebtn');  // Eye icon ka id

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eye.classList.remove('fa-eye-slash');
        eye.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        eye.classList.remove('fa-eye');
        eye.classList.add('fa-eye-slash');
    }
}
function checklogin() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please fill in all fields!");
        return;
    }

    const userData = { email, password };

    const submitBtn = document.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Signing In...";
    submitBtn.disabled = true;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Login Successful! Redirecting...");
            window.location.href = data.redirect || "/";
        } else {
            alert(data.message || "❌ Invalid email or password!");
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error("Login error:", error);
        alert("❌ Something went wrong during login. Please try again.");
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginform');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            checklogin();
        });
    }
});





// Data object - with null check
// Data object - with null check
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    // Spinner & message element create karke form ke andar inject karenge
    const messageBox = document.createElement("div");
    messageBox.id = "formMessage";
    messageBox.style.marginTop = "10px";
    messageBox.style.fontWeight = "bold";
    signupForm.appendChild(messageBox);

    const spinner = document.createElement("div");
    spinner.id = "loadingSpinner";
    spinner.style.display = "none";
    spinner.style.marginTop = "10px";
    spinner.innerHTML = "⏳ Processing...";
    signupForm.appendChild(spinner);

    signupForm.addEventListener('submit', function (e) {
        e.preventDefault(); // default submit rok dega

        // Reset message
        messageBox.innerHTML = "";
        messageBox.style.color = "black";

        // Show spinner
        spinner.style.display = "block";

        // Get form data
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm').value;
        const terms = document.getElementById('terms').checked;

        // Validation
        if (!username || !email || !password || !confirmPassword) {
            spinner.style.display = "none";
            messageBox.style.color = "red";
            messageBox.innerHTML = "⚠️ Please fill in all fields";
            return;
        }

        if (password !== confirmPassword) {
            spinner.style.display = "none";
            messageBox.style.color = "red";
            messageBox.innerHTML = "⚠️ Passwords do not match";
            return;
        }

        if (password.length < 6) {
            spinner.style.display = "none";
            messageBox.style.color = "red";
            messageBox.innerHTML = "⚠️ Password must be at least 6 characters long";
            return;
        }

        if (!terms) {
            spinner.style.display = "none";
            messageBox.style.color = "red";
            messageBox.innerHTML = "⚠️ Please accept the Terms & Conditions";
            return;
        }

        // Data object
        const userData = {
            username: username,
            email: email,
            password: password
        };

        console.log('Submitting signup data:', userData);

        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = "none"; // Hide spinner
            if (data.success) {
                messageBox.style.color = "green";
                messageBox.innerHTML = "✅ Signup Successful! Redirecting...";
                setTimeout(() => {
                    window.location.href = data.redirect || "/";
                }, 1500);
            } else {
                messageBox.style.color = "red";
                messageBox.innerHTML = "❌ " + (data.message || "Signup failed.");
            }
        })
        .catch(error => {
            spinner.style.display = "none"; // Hide spinner
            console.error('Signup error:', error);
            messageBox.style.color = "red";
            messageBox.innerHTML = "❌ Something went wrong during signup.";
        });
    });
}



// Add to cart functionality
function addcart() {
    let cartItem = document.getElementById("addcart");
    if (cartItem) {
        alert("Item added to cart!");
        // Future: yaha backend ko call kar sakte ho to save cart in DB
    } else {
        console.error("Add to cart element not found");
    }
}


// Newsletter demo
function bbSubscribe(e) {
    e.preventDefault();
    const i = e.target.querySelector('input[type="email"]');
    if (!i) return false;
    alert("Thanks for subscribing, " + i.value + " ✨");
    i.value = "";
    return false;
}
// Year - with null check
const bbYear = document.getElementById("bb-year");
if (bbYear) {
    bbYear.textContent = new Date().getFullYear();
}


function openTerms() {
    document.getElementById("termsModal").style.display = "block";
}
function closeTerms() {
    document.getElementById("termsModal").style.display = "none";
}
function acceptTerms() {
    document.getElementById("terms").disabled = false;
    document.getElementById("terms").checked = true;
    closeTerms();
}

// signupUser function removed - validation now handled in main form event listener



    // Enhanced Search functionality
    const searchInput = document.getElementById("searchInput");
    const productList = document.getElementById("productList");
    const noResultsMessage = document.getElementById("noResultsMessage");
    const searchForm = document.getElementById("searchForm");
    const clearSearchBtn = document.getElementById("clearSearch");

    // Prevent form submission
    if (searchForm) {
        searchForm.addEventListener("submit", function(e) {
            e.preventDefault();
            // Search is handled by keyup event
        });
    }

    // Clear search functionality
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener("click", function() {
            searchInput.value = "";
            searchInput.focus();
            // Trigger search to show all products
            searchInput.dispatchEvent(new Event('keyup'));
        });
    }

    if (searchInput && productList) {
        const products = productList.getElementsByClassName("product");

        searchInput.addEventListener("keyup", function () {
            const filter = searchInput.value.toLowerCase().trim();
            let visibleCount = 0;

            // Show/hide clear button
            if (clearSearchBtn) {
                clearSearchBtn.style.display = filter !== '' ? 'block' : 'none';
            }

            // Search through all products
            for (let i = 0; i < products.length; i++) {
                let productText = products[i].textContent || products[i].innerText;
                let productTitle = products[i].querySelector('.card-title');
                let productPrice = products[i].querySelector('.text-success');
                
                // Search in product title, price, and all text content
                let searchableText = '';
                if (productTitle) searchableText += productTitle.textContent + ' ';
                if (productPrice) searchableText += productPrice.textContent + ' ';
                searchableText += productText;

                if (filter === '' || searchableText.toLowerCase().indexOf(filter) > -1) {
                    products[i].style.display = "";
                    visibleCount++;
                } else {
                    products[i].style.display = "none";
                }
            }

            // Show/hide no results message
            if (filter !== '' && visibleCount === 0) {
                noResultsMessage.style.display = "block";
            } else {
                noResultsMessage.style.display = "none";
            }

            // Add search highlight effect
            if (filter !== '') {
                highlightSearchResults(filter);
            } else {
                removeHighlights();
            }
        });

        // Clear search when input is empty
        searchInput.addEventListener("input", function () {
            if (this.value.trim() === '') {
                noResultsMessage.style.display = "none";
                removeHighlights();
            }
        });
    }

    // Function to highlight search results
    function highlightSearchResults(searchTerm) {
        const products = document.getElementsByClassName("product");
        for (let i = 0; i < products.length; i++) {
            if (products[i].style.display !== "none") {
                const title = products[i].querySelector('.card-title');
                if (title) {
                    const originalText = title.getAttribute('data-original') || title.textContent;
                    title.setAttribute('data-original', originalText);
                    
                    const regex = new RegExp(`(${searchTerm})`, 'gi');
                    const highlightedText = originalText.replace(regex, '<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 3px;">$1</mark>');
                    title.innerHTML = highlightedText;
                }
            }
        }
    }

    // Function to remove highlights
    function removeHighlights() {
        const products = document.getElementsByClassName("product");
        for (let i = 0; i < products.length; i++) {
            const title = products[i].querySelector('.card-title');
            if (title && title.getAttribute('data-original')) {
                title.textContent = title.getAttribute('data-original');
                title.removeAttribute('data-original');
            }
        }
    }
