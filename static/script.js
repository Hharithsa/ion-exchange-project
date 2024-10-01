document.getElementById('compute-button').addEventListener('click', function() {

    const algo = document.getElementById('algo-select').value;
    const target = document.getElementById('dropdown').value;

    fetch(`/values?algo=${algo}&target=${target}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            
            // Update the values
            document.getElementById('mse-value').textContent = data.mse;
            document.getElementById('mae-value').textContent = data.mae;
            document.getElementById('r2-value').textContent = data.r2;

            // Update the plot image
            const img = document.getElementById('image');
            img.src = 'data:image/png;base64,' + data.plot;
            img.style.display = 'block';  // Show image when it's ready
        })
        .catch(error => {
            console.error('Error fetching compute results:', error);
        });

});

document.getElementById('upload-file').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/data-files', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Clear the existing dropdown options
        const dropdown = document.getElementById('dropdown');
        dropdown.innerHTML = '';

        // Populate the dropdown with column names
        data.columns.forEach(column => {
            const option = document.createElement('option');
            option.value = column;
            option.textContent = column;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error uploading file:', error));
});
