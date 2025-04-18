// Form 1 Validation
function validateForm1() {
    const form = document.getElementById("vehicle-form");
    const nextButton = document.getElementById("form1-next-btn");
  
    if (!form || !nextButton) return; // Exit if elements don't exist
  
    const requiredFields = form.querySelectorAll("input[required]");
    let allFilled = true;
  
    requiredFields.forEach(input => {
      if (input.name !== 'middleName' && !input.value) {
        allFilled = false;
      }
    });
  
    nextButton.disabled = !allFilled;
  }
  
  // Form 1 Submit Handler
  function handleForm1Submit(event) {
    const form = document.getElementById("vehicle-form");
    
    if (!form) return; // Exit if element doesn't exist
    
    const requiredFields = form.querySelectorAll("input[required]");
    let allFilled = true;
  
    requiredFields.forEach(input => {
      if (!input.value) {
        allFilled = false;
      }
    });
  
    if (!allFilled) {
      event.preventDefault(); 
      alert("Please fill in all required fields before proceeding.");
    }
  }
  
  // Form 2 Owner Toggle
  function toggleOwnerDetails() {
    const ownerDetailsSection = document.getElementById('owner-details');
    const ownerRadio = document.querySelector('input[name="owner"]:checked');
    
    if (!ownerDetailsSection || !ownerRadio) return; // Exit if elements don't exist
    
    if (ownerRadio.value === 'no') {
      ownerDetailsSection.style.display = 'block';
    } else {
      ownerDetailsSection.style.display = 'none';
    }
  }
  
  // Form 2 Validation
  function validateForm2() {
    const ownerRadio = document.querySelector('input[name="owner"]:checked');
    const ownerDetailsSection = document.getElementById('owner-details');
    const nextButton = document.querySelector('.form2-btn');
    
    if (!nextButton) return; // Exit if element doesn't exist
    
    let isValid = true;
  
    if (ownerRadio && ownerRadio.value === 'no' && ownerDetailsSection) {
      const requiredFields = ownerDetailsSection.querySelectorAll('input[required]');
      requiredFields.forEach(input => {
        if (!input.value) {
          isValid = false;
        }
      });
    } else if (!ownerRadio) {
      isValid = false;
    }
    
    if (nextButton) {
      nextButton.disabled = !isValid;
    }
  }
  
  // Form 3 Validation
  function validateForm3() {
    const googleFolderLink = document.querySelector('.form3-form-group input[type="url"]');
    const nextButton = document.querySelector('.form3-btn');
    
    if (!googleFolderLink || !nextButton) return; // Exit if elements don't exist
    
    nextButton.disabled = !googleFolderLink.value;
  }
  
  // Initialize event listeners when DOM is loaded
  document.addEventListener('DOMContentLoaded', function() {
    // Form 1 event listeners
    const form1 = document.getElementById("vehicle-form");
    if (form1) {
      form1.addEventListener("input", validateForm1);
      form1.addEventListener("submit", handleForm1Submit);
    }
    
    // Form 2 event listeners
    const form2Inputs = document.querySelectorAll('.form2-form-group input');
    if (form2Inputs.length > 0) {
      form2Inputs.forEach(input => input.addEventListener('input', validateForm2));
      
      // Add listeners to radio buttons
      const ownerRadios = document.querySelectorAll('input[name="owner"]');
      ownerRadios.forEach(radio => {
        radio.addEventListener('change', function() {
          toggleOwnerDetails();
          validateForm2();
        });
      });
    }
    
    // Form 3 event listeners
    const form3Input = document.querySelector('.form3-form-group input[type="url"]');
    if (form3Input) {
      form3Input.addEventListener('input', validateForm3);
    }
  });