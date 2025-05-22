document.addEventListener("DOMContentLoaded", function () {
    // Role Filter Dropdown Functionality
    const roleFilterDropdown = document.getElementById("roleFilterDropdown");
    const dropdownItems = document.querySelectorAll(".dropdown-menu .dropdown-item");

    // Icons for filter
    const defaultFilterIcon = '<i class="bx bx-filter-alt"></i> ';
    const boldFilterIcon = '<i class="bx bxs-filter-alt"></i> ';

    // Role Filter
    dropdownItems.forEach(item => {
        item.addEventListener("click", function (event) {
            event.preventDefault();
            let selectedText = this.innerHTML.replace(/<i.*?<\/i>/, "").trim();
            let selectedValue = this.getAttribute("data-value").toLowerCase();

            let newIcon = selectedValue === "" ? defaultFilterIcon : boldFilterIcon;
            roleFilterDropdown.innerHTML = newIcon + selectedText;

            // Filter table rows
            document.querySelectorAll("#userTable tbody tr").forEach(row => {
                row.style.display = selectedValue === "" || row.querySelector(".role").textContent.toLowerCase().includes(selectedValue) ? "" : "none";
            });

            // Update active class
            dropdownItems.forEach(i => i.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Search Filter
    document.getElementById("searchUser").addEventListener("input", function () {
        let searchText = this.value.toLowerCase();
        document.querySelectorAll("#userTable tbody tr").forEach(row => {
            let username = row.querySelector(".username").textContent.toLowerCase();
            let email = row.querySelector(".email").textContent.toLowerCase();
            row.style.display = username.includes(searchText) || email.includes(searchText) ? "" : "none";
        });
    });

    // Form Handling and Modal Management
    const userForm = document.getElementById("userForm");
    const userModal = new bootstrap.Modal(document.getElementById("userModal"));
    const userIdInput = document.getElementById("userId");
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const roleSelect = document.getElementById("role");
    const statusSelect = document.getElementById("status");
    const modalTitle = document.getElementById("modalTitle");
    const passwordFields = document.getElementById("passwordFields");
    const instructorFields = document.getElementById("instructorFields");

    // Clear errors function
    function clearErrors() {
        document.querySelectorAll('.error-feedback').forEach(el => el.remove());
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
    }

    // Display errors function
    function displayErrors(errors) {
        clearErrors();
        Object.keys(errors).forEach(field => {
            const input = document.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('is-invalid');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback error-feedback';
                errorDiv.textContent = errors[field].join(', ');
                input.parentNode.appendChild(errorDiv);
            }
        });
    }

    // Reset form function
    function resetForm() {
        userForm.reset();
        clearErrors();
        userIdInput.value = "";
        roleSelect.value = "student";
        statusSelect.value = "true";
        modalTitle.textContent = "Add User";
        passwordFields.style.display = "block";
        instructorFields.style.display = "none";
    }

    // Form submission handler
    userForm.addEventListener("submit", function (e) {
        e.preventDefault();
        clearErrors();

        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    userModal.hide();
                    window.location.reload();
                } else {
                    displayErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting the form.');
            });
    });

    // Edit user handler
    document.querySelectorAll(".edit-user").forEach(button => {
        button.addEventListener("click", function () {
            clearErrors();
            const userId = this.getAttribute("data-id");
            const username = this.getAttribute("data-username");
            const email = this.getAttribute("data-email");
            const role = this.getAttribute("data-role");
            const status = this.getAttribute("data-status");

            userIdInput.value = userId;
            usernameInput.value = username;
            emailInput.value = email;
            roleSelect.value = role.toLowerCase();
            statusSelect.value = status === "True" ? "true" : "false";

            modalTitle.textContent = "Edit User";
            passwordFields.style.display = "none";

            if (role.toLowerCase() === "instructor") {
                instructorFields.style.display = "block";
            } else {
                instructorFields.style.display = "none";
            }
        });
    });

    // Add user button handler
    document.querySelector("[data-bs-target='#userModal']").addEventListener("click", function () {
        resetForm();
    });

    // Role change handler
    roleSelect.addEventListener("change", function () {
        if (this.value === "instructor") {
            instructorFields.style.display = "block";
        } else {
            instructorFields.style.display = "none";
        }
    });

    // Handle delete user
    document.querySelectorAll('.delete-user').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this user?')) {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/delete_user/${userId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            // Remove the row from the table or reload the page
                            window.location.reload();
                        } else {
                            alert('Error deleting user: ' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while deleting the user.');
                    });
            }
        });
    });

    // Password validation for new users
    document.querySelectorAll('#password1, #password2').forEach(input => {
        input.addEventListener('input', function () {
            const password1 = document.getElementById('password1').value;
            const password2 = document.getElementById('password2').value;

            if (password2 && password1 !== password2) {
                document.getElementById('password2').classList.add('is-invalid');
                if (!document.getElementById('password-match-error')) {
                    const errorDiv = document.createElement('div');
                    errorDiv.id = 'password-match-error';
                    errorDiv.className = 'invalid-feedback error-feedback';
                    errorDiv.textContent = 'Passwords do not match';
                    document.getElementById('password2').parentNode.appendChild(errorDiv);
                }
            } else {
                document.getElementById('password2').classList.remove('is-invalid');
                const errorDiv = document.getElementById('password-match-error');
                if (errorDiv) errorDiv.remove();
            }
        });
    });
});


// To handle the form submission and modal behavior.

// document.addEventListener("DOMContentLoaded", function () {

//     // Edit user data in the modal
//     document.querySelectorAll(".edit-user").forEach(btn => {
//         btn.addEventListener("click", function () {
//             const userId = this.getAttribute("data-id");
//             const username = this.getAttribute("data-username");
//             const email = this.getAttribute("data-email");
//             const role = this.getAttribute("data-role");
//             const status = this.getAttribute("data-status");

//             document.getElementById("userId").value = userId;
//             document.getElementById("username").value = username;
//             document.getElementById("email").value = email;
//             document.getElementById("role").value = role;
//             document.getElementById("status").value = status === "true" ? "true" : "false";
            
//             if (role === "instructor") {
//                 document.getElementById("instructorFields").style.display = "block";
//             } else {
//                 document.getElementById("instructorFields").style.display = "none";
//             }
//         });
//     });

//     // Reset modal form on close
//     document.getElementById("userModal").addEventListener("hidden.bs.modal", function () {
//         document.getElementById("userForm").reset();
//         document.getElementById("instructorFields").style.display = "none";
//     });

// });

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('userForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                
                // Handle success
                if (result.success) {
                    alert('User registered successfully!');
                    window.location.reload();  // Refresh the page
                } else {
                    alert(`Error: ${result.message}`);
                }
            } else {
                console.error('Failed:', response.statusText);
                alert('An error occurred while submitting the form.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while submitting the form.');
        }
    });
});
