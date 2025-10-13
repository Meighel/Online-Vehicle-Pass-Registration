document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('signature-canvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clear-signature');
    const saveBtn = document.getElementById('save-signature');
    const fileInput = document.getElementById('id_e_signature');
    const previewDiv = document.getElementById('signature-preview');
    
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Set canvas background to white
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Drawing settings
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Mouse events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    // Touch events for mobile
    canvas.addEventListener('touchstart', handleTouchStart);
    canvas.addEventListener('touchmove', handleTouchMove);
    canvas.addEventListener('touchend', stopDrawing);

    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function draw(e) {
        if (!isDrawing) return;
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        lastX = touch.clientX - rect.left;
        lastY = touch.clientY - rect.top;
        isDrawing = true;
    }

    function handleTouchMove(e) {
        if (!isDrawing) return;
        e.preventDefault();
        
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        const x = touch.clientX - rect.left;
        const y = touch.clientY - rect.top;
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.stroke();
        
        lastX = x;
        lastY = y;
    }

    // Clear signature
    clearBtn.addEventListener('click', function() {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        previewDiv.innerHTML = '';
        fileInput.value = '';
    });

    // Save signature
    saveBtn.addEventListener('click', function() {
        canvas.toBlob(function(blob) {
            const file = new File([blob], 'signature.png', { type: 'image/png' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            
            // Show preview
            const img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            previewDiv.innerHTML = '<p>Signature saved:</p>';
            previewDiv.appendChild(img);
            
            alert('Signature saved successfully!');
        });
    });

    // Validate signature before form submission
    const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        if (!fileInput.files || fileInput.files.length === 0) {
            e.preventDefault();
            alert('Please draw and save your signature before submitting.');
            return false;
        }
    });
});