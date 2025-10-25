document.addEventListener("DOMContentLoaded", () => {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);

  // Helper function to create and show error messages
  const createErrorElement = (inputElement, message) => {
    // FIX: Added backticks (``) for template literal
    const errorId = `${inputElement.id}_error`;
    let errorEl = document.getElementById(errorId);

    if (!errorEl) {
      errorEl = document.createElement("div");
      errorEl.id = errorId;
      errorEl.className = "validation-error";
      errorEl.style.color = "red";
      errorEl.style.fontSize = "0.85rem";
      errorEl.style.marginTop = "5px";
      errorEl.setAttribute("aria-live", "polite");

      const parent = inputElement.parentNode;
      if (parent) {
        if (inputElement.nextSibling) parent.insertBefore(errorEl, inputElement.nextSibling);
        else parent.appendChild(errorEl);
      } else {
        inputElement.insertAdjacentElement("afterend", errorEl);
      }
    }
    return errorEl;
  };

  // Generic validation function
  const validateField = ({ el, regex, message }) => {
    if (!el) return;
    const errorEl = createErrorElement(el, message);

    const check = () => {
      if (el.offsetParent === null) {
        errorEl.textContent = "";
        el.classList.remove('invalid');
        return;
      }
      const value = (el.type === 'file') ? (el.files && el.files.length > 0 ? 'file' : '') : el.value.trim();
      const valid = regex.test ? regex.test(value) : !!value;
      el.classList.toggle("invalid", !valid && String(value) !== "");
      errorEl.textContent = !valid && String(value) !== "" ? message : "";
    };

    el.addEventListener("input", check);
    el.addEventListener("change", check);
    el.addEventListener("blur", check);
    // Don't run check() on init, let the submit handler do it.
    // This avoids showing errors on a blank form.
  };

  // Simple required validator (no regex)
  const validateRequired = ({ el, message }) => {
    if (!el) return;
    const errorEl = createErrorElement(el, message);

    const check = () => {
      if (el.offsetParent === null) {
        errorEl.textContent = "";
        el.classList.remove('invalid');
        return;
      }
      const value = (el.type === 'file') ? (el.files && el.files.length > 0 ? 'file' : '') : el.value.trim();
      const valid = !!value;
      // Only show required error on blur if it's empty
      el.classList.toggle('invalid', !valid); 
      errorEl.textContent = !valid ? message : '';
    };

    el.addEventListener('input', check);
    el.addEventListener('change', check);
    el.addEventListener('blur', check);
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
  
  /**
   * Universal submit handler logic.
   * Triggers validation on all fields and stops submission if any are invalid.
   */
  const handleFormSubmit = (form) => {
    form.addEventListener("submit", (e) => {
      // 1. Manually trigger a 'blur' on all fields to run their validation
      form.querySelectorAll("input[required], select[required], textarea[required], input[data-validate]").forEach(el => {
        // Only validate visible fields
        if (el.offsetParent !== null) {
            el.dispatchEvent(new Event('blur'));
        }
      });

      // 2. Check if any '.invalid' fields exist *inside the form*
      const firstErrorField = form.querySelector(".invalid");

      if (firstErrorField) {
        e.preventDefault(); // Stop the form from submitting
        alert("Please correct the highlighted fields before proceeding.");
        
        // Focus the first field with an error
        firstErrorField.focus(); 
      }
    });
  };

  // ===================================
  // PAGE 1: PERSONAL INFORMATION
  // ===================================
  const initPage1Validation = () => {
    console.log("Initializing Page 1 validation");

    const page1Fields = {
      contact: { el: $("#id_contact"), regex: /^(\+63|0)[0-9]{10}$/, message: "Contact must start with +63 or 0" },
      dl_number: { el: $("#id_dl_number"), regex: /^[A-Z]\d{2}-\d{2}-\d{6}$/, message: "Format: N03-12-123456" },
      corporate_email: { el: $("#id_corporate_email"), regex: /^(?:[0-9]{9}|[a-z0-9\._-]+)@psu(?:\.[a-z0-9-]+)?\.edu\.ph$/i, message: "Must be a valid PSU email" }
    };

    const familyContactRegex = /^(\+63|0)[0-9]{10}$/;
    const familyContacts = [
      { key: 'father_contact', id: '#id_father_contact' },
      { key: 'mother_contact', id: '#id_mother_contact' },
      { key: 'guardian_contact', id: '#id_guardian_contact' }
    ];

    familyContacts.forEach(({ key, id }) => {
      const el = $(id);
      if (el) {
        page1Fields[key] = { el, regex: familyContactRegex, message: 'Contact must start with +63 or 0' };
      }
    });

    Object.values(page1Fields).forEach(validateField);

    // Also validate other required fields that don't have special regex
    $$("#id_first_name, #id_last_name, #id_present_address").forEach(el => {
        if(el) validateRequired({el, message: "This field is required"});
    });
    // ... add any other 'simple required' fields for page 1 here ...


    // School role change handler
    const schoolRoleRadios = $$('input[name="school_role"]');
    const employeeFields = $("#employee-fields");
    const studentFields = $("#student-fields");
    const familyInfoSection = $("#family-info-section");

    const updateFieldsVisibility = () => {
      let selectedRole = $('input[name="school_role"]:checked')?.value;

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
      schoolRoleRadios.forEach(radio => radio.addEventListener("change", updateFieldsVisibility));
      updateFieldsVisibility(); // Initial call
    }

    // Form submission validation
    const form = $("form");
    if (form) handleFormSubmit(form); // REFACTORED
  };

  // ===================================
  // PAGE 2: VEHICLE INFORMATION
  // ===================================
  const initPage2Validation = () => {
    console.log("Initializing Page 2 validation");

    const page2Fields = {
      plateNumber: { el: $("#id_plate_number"), regex: /^[A-Za-z]{1,3}[- ]?\d{1,4}$/, message: "Format: ABC-1234" },
      chassisNumber: { el: $("#id_chassis_number"), regex: /^[A-Za-z0-9]{17}$/, message: "Must be 17 characters" },
      orNumber: { el: $("#id_or_number"), regex: /^\d{1,15}$/, message: "Numeric, max 15 digits" },
      crNumber: { el: $("#id_cr_number"), regex: /^\d{1,9}$/, message: "Numeric, max 9 digits" },
      yearModel: { el: $("#id_year_model"), regex: /^(19|20)\d{2}$/, message: "Year 1900-2099" },
      contactNumber: { el: $("#id_contact_number"), regex: /^(\+63|0)[0-9]{10}$/, message: "Contact must start with +63 or 0" }
    };
    Object.values(page2Fields).forEach(validateField);

    // Owner detail inline validators
    if ($("#id_owner_firstname")) validateRequired({ el: $("#id_owner_firstname"), message: "Owner's first name is required" });
    if ($("#id_owner_lastname")) validateRequired({ el: $("#id_owner_lastname"), message: "Owner's last name is required" });
    if ($("#id_relationship_to_owner")) validateRequired({ el: $("#id_relationship_to_owner"), message: "Relationship is required" });
    if ($("#id_address")) validateRequired({ el: $("#id_address"), message: "Owner's address is required" });
    // Note: owner contact number is already covered by 'page2Fields' if it's the same ID. If not, add it here.
    
    // Owner radio button handler
    const ownerRadios = $$('input[name="owner"]');
    const ownerDetails = $("#owner-details");

    const toggleOwnerDetails = () => {
      const selected = $('input[name="owner"]:checked');
      if (!ownerDetails || !selected) return;

      if (selected.value === "no") {
        ownerDetails.style.display = "block";
        ownerDetails.querySelectorAll("input").forEach(input => input.required = true);
      } else {
        ownerDetails.style.display = "none";
        ownerDetails.querySelectorAll("input").forEach(input => {
          input.value = "";
          input.required = false;
          input.classList.remove("invalid");
          // FIX: Added backticks (``)
          const errorEl = document.getElementById(`${input.id}_error`);
          if (errorEl) errorEl.textContent = "";
        });
      }
    };

    if (ownerRadios.length) {
      ownerRadios.forEach(radio => radio.addEventListener("change", toggleOwnerDetails));
      toggleOwnerDetails(); // Initial call
    }

    // Form submission validation
    const form = $("form");
    if (form) handleFormSubmit(form); // REFACTORED
  };

  // ===================================
  // PAGE 3: DOCUMENTS AND SIGNATURE
  // ===================================
  const initPage3Validation = () => {
    console.log("Initializing Page 3 validation");

    // Google Drive link validation
    const driveLinkInput = $("#id_google_drive_link");
    if (driveLinkInput) {
      validateField({
        el: driveLinkInput,
        regex: /^https:\/\/drive\.google\.com\/(file\/d\/|open\?id=|drive\/folders\/|folderview\?id=)[\w-]+/,
        message: "Please enter a valid Google Drive link"
      });
    }

    // Printed name required
    const printedName = $("#id_printed_name");
    if (printedName) validateRequired({ el: printedName, message: "Printed name is required" });

    // Signature date required
    const signatureDate = $("#id_signature_date");
    if (signatureDate) validateRequired({ el: signatureDate, message: "Signature date is required" });

    // E-signature (file input)
    const eSignature = $("#e-signature") || $("#id_e_signature") || $("#id_e-signature");
    if (eSignature) validateRequired({ el: eSignature, message: "E-signature image is required" });

    // Form submission
    const form = $("form");
    if (form) handleFormSubmit(form); // REFACTORED
  };

  // ===================================
  // INITIALIZE BASED ON CURRENT PAGE
  // ===================================
  const init = () => {
    setProgressBar();
    
    // FIX: Moved path declaration to the top
    const path = window.location.pathname;

    try {
      const hasPage1 = !!$("#form1-next-btn");
      const hasPage2 = !!$("#form2-next-btn");
      const hasPage3 = !!$("#form3-next-btn");

      if (hasPage1) initPage1Validation();
      if (hasPage2) initPage2Validation();
      if (hasPage3) initPage3Validation();
    } catch (err) {
      console.error("Element-based init failed, falling back to path-based:", err);
      if (path.includes("step_1")) initPage1Validation();
      else if (path.includes("step_2")) initPage2Validation();
      else if (path.includes("step_3")) initPage3Validation();
    }

    // FIX: Added backticks (``)
    console.log(`Initialized validation for: ${path}`);
  };

  // Run initialization
  init();
});