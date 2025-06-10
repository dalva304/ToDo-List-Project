document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
      const htmlElement = document.documentElement;
      
      // Check for saved theme preference
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark') {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        darkModeToggle.innerHTML = '<i class="bi bi-sun"></i>';
      }
      
      // Toggle theme
      darkModeToggle.addEventListener('click', function() {
        if (htmlElement.getAttribute('data-bs-theme') === 'dark') {
          htmlElement.setAttribute('data-bs-theme', 'light');
          localStorage.setItem('theme', 'light');
          darkModeToggle.innerHTML = '<i class="bi bi-moon"></i>';
        } else {
          htmlElement.setAttribute('data-bs-theme', 'dark');
          localStorage.setItem('theme', 'dark');
          darkModeToggle.innerHTML = '<i class="bi bi-sun"></i>';
        }
      });
    }
    
    // Task completion animation
    const taskCompletionCheckboxes = document.querySelectorAll('.task-completion-checkbox');
    taskCompletionCheckboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        if (this.checked) {
          const taskCard = this.closest('.task-card');
          if (taskCard) {
            taskCard.classList.add('task-complete-animation');
            setTimeout(() => {
              taskCard.classList.remove('task-complete-animation');
            }, 500);
          }
        }
      });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize Rich Text Editor if present
    const editorElement = document.getElementById('editor');
    if (editorElement && typeof Quill !== 'undefined') {
      const quill = new Quill('#editor', {
        theme: 'snow',
        placeholder: 'Enter task description...',
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'],
            ['blockquote', 'code-block'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            ['link'],
            ['clean']
          ]
        }
      });
      
      // If editing, populate the editor with existing content
      const descriptionInput = document.getElementById('description-input');
      if (descriptionInput && descriptionInput.value) {
        quill.root.innerHTML = descriptionInput.value;
      }
      
      // Update hidden input before form submission
      const taskForm = document.querySelector('form');
      if (taskForm) {
        taskForm.addEventListener('submit', function() {
          descriptionInput.value = quill.root.innerHTML;
        });
      }
    }
    
    // Add data-old-status attribute to the select elements to track status changes
    document.querySelectorAll('.status-select').forEach(select => {
      select.setAttribute('data-old-status', select.value);
    });
    
    // Add event listener to custom status input
    const customInputs = document.querySelectorAll('.custom-status-input');
    customInputs.forEach(input => {
      input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          // Set the select to "custom" before submitting to ensure proper status
          const selectElement = this.form.querySelector('select');
          selectElement.value = 'custom';
          this.form.submit();
        }
      });
      input.addEventListener('blur', function() {
        if (this.value.trim() !== '') {
          // Set the select to "custom" before submitting to ensure proper status
          const selectElement = this.form.querySelector('select');
          selectElement.value = 'custom';
          this.form.submit();
        }
      });
    });

});

//status updates ! dropdown

function toggleCustomField(selectElement) {
    console.log('Toggle function called with status:', selectElement.value);
    
    const form = selectElement.form;
    const customInput = form.querySelector('.custom-status-input');
    const isNewCustomInput = form.querySelector('[id^="is-new-custom-"]');
    const oldStatus = selectElement.getAttribute('data-old-status');
    
    // Update select element class based on selected value
    selectElement.className = 'form-select form-select-sm status-select';
    
    // Add appropriate class based on selection
    if (selectElement.value === 'not_started') {
        selectElement.classList.add('status-not-started');
        customInput.style.display = 'none';
        isNewCustomInput.value = '0';
        form.submit();
    } else if (selectElement.value === 'in_progress') {
        selectElement.classList.add('status-in-progress');
        customInput.style.display = 'none';
        isNewCustomInput.value = '0';
        form.submit();
    } else if (selectElement.value === 'completed') {
        selectElement.classList.add('status-completed');
        customInput.style.display = 'none';
        isNewCustomInput.value = '0';
        
        // Check if this is a transition to completed
        if (oldStatus !== 'completed') {
          // Add animation class for visual feedback
          const row = selectElement.closest('tr');
          row.classList.add('task-complete-animation');
          
          // Trigger confetti!
          console.log('Status is completed and changed from', oldStatus, 'triggering confetti');
          try {
            window.triggerConfetti(); // Use the global function
          } catch (e) {
            console.error('Error with confetti:', e);
          }
        }
        
        form.submit();
    } else if (selectElement.value === 'custom') {
        selectElement.classList.add('status-custom');
        
        // Show the custom input field for editing or entering a new value
        customInput.style.display = 'block';
        customInput.focus();
        
        // Check if we're editing an existing custom status or creating a new one
        if (oldStatus === 'custom') {
            // We're editing an existing custom status
            isNewCustomInput.value = '0';
            // Don't submit the form yet - let the user edit the value
        } else {
            // This is a new custom status
            isNewCustomInput.value = '1';
            // Don't submit yet, let user enter the value
        }
        
        // Don't submit the form automatically - wait for the user to enter text
        return false;
    }
}

function triggerConfetti() {
    console.log('Confetti function called');
    // Simple confetti test
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

