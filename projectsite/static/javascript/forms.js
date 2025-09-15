document.addEventListener("DOMContentLoaded", () => {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);

  const setProgressBar = () => {
    const path = window.location.pathname;
    const progress = $(".progress-bar");
    if (!progress) return;

    if (path.includes("step_1")) progress.style.width = "33%";
    else if (path.includes("step_2")) progress.style.width = "66%";
    else if (path.includes("step_3")) progress.style.width = "100%";
  };

  const addRealTimeValidation = () => {
    const fields = {
      driverLicense: {
        el: $("#id_driver_license_number"),
        regex: /^[A-Z0-9]{3}-\d{2}-\d{6}$/,
        message: "Driver license number must follow the format N01-23-456789"
      },
      plateNumber: {
        el: $("#id_plate_number"),
        regex: /^[A-Za-z]{1,3}-\d{1,4}$/,
        message: "Plate number must be in the format ABC-1234"
      },
      chassisNumber: {
        el: $("#id_chassis_number"),
        regex: /^[A-Za-z0-9]{17}$/,
        message: "Chassis number must be exactly 17 alphanumeric characters"
      },
      orNumber: {
        el: $("#id_or_number"),
        regex: /^\d{1,15}$/,
        message: "OR number must be numeric and a max of 15 digits"
      },
      crNumber: {
        el: $("#id_cr_number"),
        regex: /^\d{1,9}$/,
        message: "CR number must be numeric and a max of 9 digits"
      },
      ownersContactNumber: {
        el: $("#id_contact_number"), // Fixed ID to match HTML
        regex: /^[0-9]{11}$/,
        message: "Contact number must be exactly 11 digits"
      }
    };

    const validateField = ({ el, regex, message }) => {
      if (!el) return;

      const errorId = `${el.id}_error`;
      let errorEl = document.getElementById(errorId);

      if (!errorEl) {
        errorEl = document.createElement("div");
        errorEl.id = errorId;
        errorEl.style.color = "red";
        errorEl.style.fontSize = "0.8rem";
        errorEl.style.marginTop = "5px";
        el.insertAdjacentElement("afterend", errorEl);
      }

      el.addEventListener("input", () => {
        const value = el.value.trim();
        const valid = regex.test(value);
        el.classList.toggle("invalid", !valid && value !== "");
        errorEl.textContent = !valid && value !== "" ? message : "";
      });
    };

    Object.values(fields).forEach(validateField);
  };

  const validateRequiredInputs = (container) => {
    const requiredFields = container.querySelectorAll("input[required], select[required]");
    return [...requiredFields].every((input) => {
      // Allow middle name to be empty even if required
      if (input.name === "middle_name" || input.name === "middleName") return true;
      return input.value.trim() !== "";
    });
  };

  // Step 1 validation
  const validateForm1 = () => {
    const form = $("form");
    const nextBtn = $("#form1-next-btn");
    if (!form || !nextBtn) return;

    const isValid = validateRequiredInputs(form);
    nextBtn.disabled = !isValid;
  };

  const handleForm1Submit = (e) => {
    const form = $("form");
    if (!form) return;

    if (!validateRequiredInputs(form)) {
      e.preventDefault();
      alert("Please fill in all required fields before proceeding.");
    }
  };

  // Step 2 functionality
  const toggleOwnerDetails = () => {
    const ownerDetails = $("#owner-details");
    const selected = $('input[name="owner"]:checked');

    if (!ownerDetails) return;

    if (selected && selected.value === "no") {
      ownerDetails.style.display = "block";
      // Make owner details fields required when visible
      ownerDetails.querySelectorAll("input, select").forEach((input) => {
        if (input.name !== "owner_suffix") { // Suffix is optional
          input.setAttribute("required", "required");
        }
      });
    } else {
      ownerDetails.style.display = "none";
      // Clear values and remove required attribute when hidden
      ownerDetails.querySelectorAll("input, select").forEach((input) => {
        input.value = "";
        input.removeAttribute("required");
      });
    }
  };

  const validateForm2 = () => {
    const ownerRadio = $('input[name="owner"]:checked');
    const ownerDetails = $("#owner-details");
    const nextBtn = $("#form2-next-btn");

    let isValid = !!ownerRadio;

    // Check if "No" is selected and owner details are required
    if (ownerRadio && ownerRadio.value === "no" && ownerDetails) {
      const requiredInputs = ownerDetails.querySelectorAll("input[required], select[required]");
      isValid = isValid && [...requiredInputs].every((input) => input.value.trim() !== "");
    }

    if (nextBtn) nextBtn.disabled = !isValid;
  };

  const handleForm2Submit = (e) => {
    const ownerRadio = $('input[name="owner"]:checked');
    const ownerDetails = $("#owner-details");

    if (!ownerRadio) {
      e.preventDefault();
      alert("Please select whether you are the owner of the vehicle.");
      return;
    }

    if (ownerRadio.value === "no" && ownerDetails) {
      const requiredInputs = ownerDetails.querySelectorAll("input[required], select[required]");
      const isValid = [...requiredInputs].every((input) => input.value.trim() !== "");
      
      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required owner information fields.");
        return;
      }
    }
  };

  // Step 3 validation
  const validateForm3 = () => {
    const input = $(".form3-form-group input[type='url'], input[name='google_drive_link']");
    const nextBtn = $(".form3-btn, .btn[type='submit']");

    if (!input || !nextBtn) return;

    const errorId = `${input.id || "drive_url"}_error`;
    let errorEl = document.getElementById(errorId);

    if (!errorEl) {
      errorEl = document.createElement("div");
      errorEl.id = errorId;
      errorEl.style.color = "red";
      errorEl.style.fontSize = "0.8rem";
      errorEl.style.marginTop = "5px";
      input.insertAdjacentElement("afterend", errorEl);
    }

    const value = input.value.trim();
    const isValidDriveLink = value === "" || /^https:\/\/drive\.google\.com\/(file\/d\/|open\?id=|uc\?id=)[\w-]+/.test(value);

    input.classList.toggle("invalid", !isValidDriveLink);
    errorEl.textContent = !isValidDriveLink 
      ? "Please enter a valid Google Drive link." 
      : "";

    nextBtn.disabled = !isValidDriveLink;
  };

  // Initialize all functionality
  const init = () => {
    setProgressBar();
    addRealTimeValidation();

    const currentPath = window.location.pathname;

    // Step 1 - Personal Information Form
    if (currentPath.includes("step_1") || currentPath.includes("vehicle_registration") && !currentPath.includes("step_2") && !currentPath.includes("step_3")) {
      const form = $("form");
      const nextBtn = $("#form1-next-btn");
      
      if (form && nextBtn) {
        // Add event listeners to all form inputs
        const inputs = form.querySelectorAll("input, select");
        inputs.forEach((input) => {
          input.addEventListener("input", validateForm1);
          input.addEventListener("change", validateForm1);
        });

        form.addEventListener("submit", handleForm1Submit);
        validateForm1(); // Initial validation
      }
    }

    // Step 2
    const form2Inputs = $$(".form2-form-group input");
    if (form2Inputs.length) {
      form2Inputs.forEach((input) =>
        input.addEventListener("input", validateForm2)
      );
      $$('input[name="owner"]').forEach((radio) => {
        radio.addEventListener("change", () => {
          toggleOwnerDetails();
          validateForm2();
        });
      });
      toggleOwnerDetails(); // Initial call
      validateForm2();
    }

    // Prevent Step 2 submission if invalid
    const form2 = document.querySelector("form");
    if (form2 && window.location.pathname.includes("step_2")) {
      form2.addEventListener("submit", (e) => {
        validateForm2(); // Re-check before submit
        const nextBtn = $(".form2-btn");
        if (nextBtn.disabled) {
          e.preventDefault();
          alert("Please fill in all required fields correctly before proceeding.");
        }
      });
    }

    // Step 3 - Document Upload Form
    if (currentPath.includes("step_3")) {
      const input = $("input[type='url'], input[name='google_drive_link']");
      
      if (input) {
        input.addEventListener("input", validateForm3);
        validateForm3(); // Initial validation
      }
    }
  };

  init();
});