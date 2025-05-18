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
        regex: /^\d{15}$/,
        message: "Driver license number must be exactly 15 digits"
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
        regex: /^\d+$/,
        message: "OR number must be numeric"
      },
      crNumber: {
        el: $("#id_cr_number"),
        regex: /^\d+$/,
        message: "CR number must be numeric"
      },
      ownersContactNumber: {
        el: $("#id_owner_contact_number"), // corrected ID
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
    const requiredFields = container.querySelectorAll("input[required]");
    return [...requiredFields].every(
      (input) => input.name === "middleName" || input.value.trim()
    );
  };

  const validateForm1 = () => {
    const form = $("#vehicle-form");
    const nextBtn = $("#form1-next-btn");
    if (!form || !nextBtn) return;

    nextBtn.disabled = !validateRequiredInputs(form);
  };

  const handleForm1Submit = (e) => {
    const form = $("#vehicle-form");
    if (!form) return;

    if (!validateRequiredInputs(form)) {
      e.preventDefault();
      alert("Please fill in all required fields before proceeding.");
    }
  };

  const toggleOwnerDetails = () => {
    const ownerDetails = $("#owner-details");
    const selected = $('input[name="owner"]:checked');

    if (!ownerDetails || !selected) return;

    if (selected.value === "no") {
      ownerDetails.style.display = "block";
    } else {
      ownerDetails.style.display = "none";
      ownerDetails.querySelectorAll("input").forEach((input) => (input.value = ""));
    }
  };

  const validateForm2 = () => {
    const ownerRadio = $('input[name="owner"]:checked');
    const ownerDetails = $("#owner-details");
    const nextBtn = $(".form2-btn");

    let isValid = !!ownerRadio;

    if (ownerRadio?.value === "no" && ownerDetails) {
      const requiredInputs = ownerDetails.querySelectorAll("input[required]");
      isValid = [...requiredInputs].every((input) => input.value.trim());
    }

    if (nextBtn) nextBtn.disabled = !isValid;
  };

  const validateForm3 = () => {
    const input = $(".form3-form-group input[type='url']");
    const nextBtn = $(".form3-btn");

    if (nextBtn && input) {
      nextBtn.disabled = !input.value.trim();
    }
  };

  // Register all listeners
  const init = () => {
    setProgressBar();
    addRealTimeValidation();

    // Step 1
    const form1 = $("#vehicle-form");
    if (form1 && window.location.pathname.includes("step_1")) {
      form1.addEventListener("input", validateForm1);
      form1.addEventListener("submit", handleForm1Submit);
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

    // Step 3
    const form3Input = $(".form3-form-group input[type='url']");
    if (form3Input) {
      form3Input.addEventListener("input", validateForm3);
    }
  };

  init();
});
