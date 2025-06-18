  function confirmDelete(userId) {
    document.getElementById('deleteUserId').value = userId;
    var deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    deleteModal.show();
  }

  // Validate password match
  document.getElementById('addUserForm').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
      event.preventDefault();
      alert('Passwords do not match!');
    }
  });
