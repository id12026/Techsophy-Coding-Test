document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patient-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            let valid = true;
            
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                    field.focus();
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            const ageInput = document.getElementById('age');
            if (ageInput) {
                const age = parseInt(ageInput.value);
                if (isNaN(age) || age < 1 || age > 120) {
                    valid = false;
                    ageInput.style.borderColor = '#e74c3c';
                    if (valid) ageInput.focus();
                } else {
                    ageInput.style.borderColor = '#ddd';
                }
            }

            const numberInputs = form.querySelectorAll('input[type="number"]');
            numberInputs.forEach(input => {
                if (input.value !== '') {
                    const value = parseFloat(input.value);
                    const min = parseFloat(input.min);
                    const max = parseFloat(input.max);

                    if (isNaN(value) || (input.hasAttribute('min') && value < min) || (input.hasAttribute('max') && value > max)) {
                        valid = false;
                        input.style.borderColor = '#e74c3c';
                        if (valid) input.focus();
                    } else {
                        input.style.borderColor = '#ddd';
                    }
                } else {
                    input.style.borderColor = '#ddd';
                }
            });
            
            if (!valid) {
                event.preventDefault();
                alert('Please correct the highlighted fields with valid values.');
            }
        });
    }
    
    window.addDisease = function(disease) {
        const conditionsInput = document.getElementById('conditions');
        if (conditionsInput) {
            const currentValue = conditionsInput.value.trim();
            
            if (currentValue === '') {
                conditionsInput.value = disease;
            } else {
                const diseases = currentValue.split(',').map(d => d.trim().toLowerCase());
                if (!diseases.includes(disease.toLowerCase())) {
                    conditionsInput.value = currentValue + ', ' + disease;
                }
            }
            conditionsInput.focus();
        }
    };
    
    const textareas = ['conditions', 'medications', 'allergies'];
    textareas.forEach(id => {
        const textarea = document.getElementById(id);
        if (textarea) {
            textarea.addEventListener('input', function() {
                this.value = this.value.replace(/\s+/g, ' ').split(',').map(s => s.trim()).filter(s => s).join(', ');
            });
        }
    });

    // --- New Modal/Contact Form Functionality ---
    const contactButtons = document.querySelectorAll('.contact-btn');
    const modal = document.getElementById('contactModal');
    const closeButton = document.querySelector('.close-button');
    const modalTrialTitle = document.getElementById('modalTrialTitle');
    const modalTrialId = document.getElementById('modalTrialId');
    const modalContactEmail = document.getElementById('modalContactEmail');
    const modalContactPhone = document.getElementById('modalContactPhone');

    if (contactButtons && modal) {
        contactButtons.forEach(button => {
            button.addEventListener('click', function() {
                const card = this.closest('.trial-card');
                const trialTitle = card.querySelector('h3').textContent;
                const trialId = card.querySelector('.trial-details div:first-child').textContent.replace('Trial ID: ', '').trim();
                
                const contactEmail = 'contact@clinicaltrials.in';
                const contactPhone = '+91 98765 43210'; 

                modalTrialTitle.textContent = trialTitle;
                modalTrialId.textContent = trialId;
                modalContactEmail.href = `mailto:${contactEmail}?subject=Inquiry about Trial ${trialId}: ${trialTitle}`;
                modalContactEmail.textContent = contactEmail;
                modalContactPhone.textContent = contactPhone;

                modal.style.display = 'flex'; 
            });
        });

        closeButton.addEventListener('click', function() {
            modal.style.display = 'none';
        });

        window.addEventListener('click', function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        });
    }
});