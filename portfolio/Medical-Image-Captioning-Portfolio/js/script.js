// Demo functionality for image upload and caption generation (simulated)
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const generateBtn = document.getElementById('generateBtn');
    const captionOutput = document.getElementById('captionOutput');
    const imagePreview = document.getElementById('imagePreview');

    // Image preview functionality
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
            };
            reader.readAsDataURL(file);
        } else {
            imagePreview.innerHTML = '';
        }
    });

    generateBtn.addEventListener('click', function() {
        const file = imageInput.files[0];
        if (!file) {
            captionOutput.textContent = 'Please select an image first.';
            return;
        }

        // Show loading state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        captionOutput.textContent = 'Analyzing image...';

        // Simulate processing delay
        setTimeout(() => {
            const fileName = file.name.toLowerCase();

            // Simulate image type detection based on file name
            let imageType = null;
            if (fileName.includes('xray') || fileName.includes('chest') || fileName.includes('x-ray')) {
                imageType = 'X-ray';
            } else if (fileName.includes('mri') || fileName.includes('magnetic')) {
                imageType = 'MRI';
            } else if (fileName.includes('ct') || fileName.includes('computed')) {
                imageType = 'CT Scan';
            } else if (fileName.includes('ultrasound') || fileName.includes('sono')) {
                imageType = 'Ultrasound';
            }

            if (imageType) {
                // Medical image detected
                const mockCaptions = {
                    'X-ray': [
                        'This chest X-ray reveals bilateral pneumonia with consolidation in the lower lobes.',
                        'X-ray shows a fractured rib on the left side with no pneumothorax.'
                    ],
                    'MRI': [
                        'MRI scan indicates a benign tumor in the frontal lobe with no surrounding edema.',
                        'Brain MRI demonstrates normal anatomy with no focal lesions.'
                    ],
                    'CT Scan': [
                        'CT image shows a fractured tibia with proper alignment and no vascular compromise.',
                        'Abdominal CT reveals appendicitis with periappendiceal fat stranding.'
                    ],
                    'Ultrasound': [
                        'Ultrasound depicts a healthy fetal heartbeat and normal placental position.',
                        'Pelvic ultrasound shows normal ovarian follicles and endometrial thickness.'
                    ]
                };

                const captions = mockCaptions[imageType];
                const randomCaption = captions[Math.floor(Math.random() * captions.length)];
                captionOutput.innerHTML = `Image Type: ${imageType}<br>Generated Caption: ${randomCaption}`;
            } else {
                // Not a medical image
                captionOutput.textContent = 'This does not appear to be a medical image. Please upload a relevant medical scan (X-ray, MRI, CT, Ultrasound).';
            }

            // Reset button
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-robot"></i> Generate Caption';

            // Add a fade-in animation to the caption
            captionOutput.style.animation = 'fadeIn 0.5s ease-in';
        }, 2000); // 2 second delay to simulate processing
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add fade-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);



// Fade-in on scroll
function handleScroll() {
    const fadeInElements = document.querySelectorAll('.fade-in');
    fadeInElements.forEach(element => {
        const rect = element.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            element.classList.add('visible');
        }
    });
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll); // Trigger on load in case elements are already in view
