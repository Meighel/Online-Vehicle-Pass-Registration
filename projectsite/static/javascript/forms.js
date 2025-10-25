document.addEventListener("DOMContentLoaded", () => {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);

  // Helper function to create and show error messages
  const createErrorElement = (inputElement, message) => {
    const errorId = `${inputElement.id}_error`;
    let errorEl = document.getElementById(errorId);

    if (!errorEl) {
      errorEl = document.createElement("div");
      errorEl.id = errorId;
      errorEl.style.color = "red";
      errorEl.style.fontSize = "0.85rem";
      errorEl.style.marginTop = "5px";
      inputElement.insertAdjacentElement("afterend", errorEl);
    }

    return errorEl;
  };

  // Generic validation function
  const validateField = ({ el, regex, message }) => {
    if (!el) return;

    const errorEl = createErrorElement(el, message);

    el.addEventListener("input", () => {
      const value = el.value.trim();
      const valid = regex.test(value);
      
      el.classList.toggle("invalid", !valid && value !== "");
      errorEl.textContent = !valid && value !== "" ? message : "";
    });

    el.addEventListener("blur", () => {
      const value = el.value.trim();
      if (value !== "") {
        const valid = regex.test(value);
        errorEl.textContent = !valid ? message : "";
      }
    });
  };

  // Set progress bar based on current page
  const setProgressBar = () => {
    const path = window.location.pathname;
    const progress = $(".progress-bar");
    if (!progress) return;

    if (path.includes("step_1")) progress.style.width = "33%";
    else if (path.includes("step_2")) progress.style.width = "66%";
    else if (path.includes("step_3")) progress.style.width = "100%";
  };

  // ===================================
  // PAGE 1: PERSONAL INFORMATION
  // ===================================
  const initPage1Validation = () => {
    console.log("Initializing Page 1 validation");

    // Define validation rules for page 1
    const page1Fields = {
      contact: {
        el: $("#id_contact"),
        regex: /^(\+63|0)[0-9]{10}$/,
        message: "Contact must start with +63 or 0 and be 11-13 digits total"
      },
      dl_number: {
        el: $("#id_dl_number"),
        regex: /^[A-Z]\d{2}-\d{2}-\d{6}$/,
        message: "Driver's license must be in format N03-12-123456"
      },
      corporate_email: {
        el: $("#id_corporate_email"),
        regex: /^[0-9]{9}@psu\.edu\.ph$/,
        message: "Email must be in format 202280001@psu.edu.ph"
      }
    };

    // Apply validation to each field
    Object.values(page1Fields).forEach(validateField);

    // School role change handler
    const schoolRoleRadios = $$('input[name="school_role"]');
    const employeeFields = $("#employee-fields");
    const studentFields = $("#student-fields");
    const familyInfoSection = $("#family-info-section");

    const updateFieldsVisibility = () => {
      let selectedRole = "";
      schoolRoleRadios.forEach(radio => {
        if (radio.checked) selectedRole = radio.value;
      });

      if (selectedRole === "student") {
        if (studentFields) studentFields.style.display = "flex";
        if (employeeFields) employeeFields.style.display = "none";
        if (familyInfoSection) familyInfoSection.style.display = "block";
      } else if (selectedRole === "faculty & staff" || selectedRole === "university official") {
        if (employeeFields) employeeFields.style.display = "flex";
        if (studentFields) studentFields.style.display = "none";
        if (familyInfoSection) familyInfoSection.style.display = "none";
      } else {
        if (employeeFields) employeeFields.style.display = "none";
        if (studentFields) studentFields.style.display = "none";
        if (familyInfoSection) familyInfoSection.style.display = "none";
      }
    };

    if (schoolRoleRadios.length) {
      schoolRoleRadios.forEach(radio => {
        radio.addEventListener("change", updateFieldsVisibility);
      });
      updateFieldsVisibility(); // Initial call
    }

    // Form submission validation
    const form = $("form");
    const nextBtn = $("#form1-next-btn");

    if (form && nextBtn) {
      form.addEventListener("submit", (e) => {
        // Check required fields
        const requiredFields = form.querySelectorAll("input[required], select[required]");
        let allValid = true;

        requiredFields.forEach(field => {
          // Skip hidden fields
          if (field.offsetParent === null) return;
          
          if (!field.value.trim()) {
            allValid = false;
            const errorEl = createErrorElement(field, "This field is required");
            errorEl.textContent = "This field is required";
            field.classList.add("invalid");
          }
        });

        if (!allValid) {
          e.preventDefault();
          alert("Please fill in all required fields before proceeding.");
        }
      });
    }
  };

  // ===================================
  // PAGE 2: VEHICLE INFORMATION
  // ===================================
  const initPage2Validation = () => {
    console.log("Initializing Page 2 validation");

    // Define validation rules for page 2
    const page2Fields = {
      plateNumber: {
        el: $("#id_plate_number"),
        regex: /^[A-Za-z]{1,3}[- ]?\d{1,4}$/,
        message: "Plate number must be in format ABC-1234 or ABC1234"
      },
      chassisNumber: {
        el: $("#id_chassis_number"),
        regex: /^[A-Za-z0-9]{17}$/,
        message: "Chassis number must be exactly 17 alphanumeric characters"
      },
      orNumber: {
        el: $("#id_or_number"),
        regex: /^\d{1,15}$/,
        message: "OR number must be numeric (max 15 digits)"
      },
      crNumber: {
        el: $("#id_cr_number"),
        regex: /^\d{1,9}$/,
        message: "CR number must be numeric (max 9 digits)"
      },
      yearModel: {
        el: $("#id_year_model"),
        regex: /^(19|20)\d{2}$/,
        message: "Year must be between 1900-2099"
      },
      contactNumber: {
        el: $("#id_contact_number"),
        regex: /^(\+63|0)[0-9]{10}$/,
        message: "Contact must start with +63 or 0 (11-13 digits total)"
      }
    };

    // Apply validation
    Object.values(page2Fields).forEach(validateField);

    // Owner radio button handler
    const ownerRadios = $$('input[name="owner"]');
    const ownerDetails = $("#owner-details");

    const toggleOwnerDetails = () => {
      const selected = $('input[name="owner"]:checked');
      
      if (!ownerDetails || !selected) return;

      if (selected.value === "no") {
        ownerDetails.style.display = "block";
        
        // Make owner fields required
        ownerDetails.querySelectorAll("input").forEach(input => {
          if (input.id.includes("firstname") || 
              input.id.includes("lastname") || 
              input.id.includes("relationship") || 
              input.id.includes("contact_number") ||
              input.id.includes("address")) {
            input.required = true;
          }
        });
      } else {
        ownerDetails.style.display = "none";
        
        // Clear and remove required from owner fields
        ownerDetails.querySelectorAll("input").forEach(input => {
          input.value = "";
          input.required = false;
          input.classList.remove("invalid");
          const errorEl = document.getElementById(`${input.id}_error`);
          if (errorEl) errorEl.textContent = "";
        });
      }
    };

    if (ownerRadios.length) {
      ownerRadios.forEach(radio => {
        radio.addEventListener("change", toggleOwnerDetails);
      });
      toggleOwnerDetails(); // Initial call
    }

    // Form submission validation
    const form = $("form");
    const nextBtn = $("#form2-next-btn");

    if (form && nextBtn) {
      form.addEventListener("submit", (e) => {
        const ownerRadio = $('input[name="owner"]:checked');
        
        if (!ownerRadio) {
          e.preventDefault();
          alert("Please select whether you are the vehicle owner.");
          return;
        }

        // If not owner, check required owner fields
        if (ownerRadio.value === "no" && ownerDetails) {
          const requiredInputs = ownerDetails.querySelectorAll("input[required]");
          let allValid = true;

          requiredInputs.forEach(input => {
            if (!input.value.trim()) {
              allValid = false;
              const errorEl = createErrorElement(input, "This field is required");
              errorEl.textContent = "This field is required";
              input.classList.add("invalid");
            }
          });

          if (!allValid) {
            e.preventDefault();
            alert("Please fill in all required owner information.");
          }
        }
      });
    }
  };

  // ===================================
  // PAGE 3: DOCUMENTS AND SIGNATURE
  // ===================================
  const initPage3Validation = () => {
    console.log("Initializing Page 3 validation");

    // Google Drive link validation
    const driveLinkInput = $("#id_google_drive_link");
    
    if (driveLinkInput) {
      const driveLinkValidation = {
        el: driveLinkInput,
        regex: /^https:\/\/drive\.google\.com\/(file\/d\/|open\?id=|drive\/folders\/|folderview\?id=)[\w-]+/,
        message: "Please enter a valid Google Drive link"
      };
      
      validateField(driveLinkValidation);
    }

    // Form submission
    const form = $("form");
    const submitBtn = $("#form3-next-btn");

    if (form && submitBtn) {
      form.addEventListener("submit", (e) => {
        let isValid = true;

        // Check Google Drive link
        if (driveLinkInput && !driveLinkInput.value.trim()) {
          isValid = false;
          const errorEl = createErrorElement(driveLinkInput, "Google Drive link is required");
          errorEl.textContent = "Google Drive link is required";
        }

        // Check printed name
        const printedName = $("#id_printed_name");
        if (printedName && !printedName.value.trim()) {
          isValid = false;
          const errorEl = createErrorElement(printedName, "Printed name is required");
          errorEl.textContent = "Printed name is required";
        }

        // Check signature date
        const signatureDate = $("#id_signature_date");
        if (signatureDate && !signatureDate.value.trim()) {
          isValid = false;
          const errorEl = createErrorElement(signatureDate, "Signature date is required");
          errorEl.textContent = "Signature date is required";
        }

        if (!isValid) {
          e.preventDefault();
          alert("Please fill in all required fields.");
        }
      });
    }
  };

  // ===================================
  // INITIALIZE BASED ON CURRENT PAGE
  // ===================================
  const init = () => {
    setProgressBar();

    const path = window.location.pathname;

    if (path.includes("step_1")) {
      initPage1Validation();
    } else if (path.includes("step_2")) {
      initPage2Validation();
    } else if (path.includes("step_3")) {
      initPage3Validation();
    }

    console.log(`Initialized validation for: ${path}`);
  };

  // Run initialization
  init();
});