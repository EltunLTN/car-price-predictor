document.addEventListener('DOMContentLoaded', function() {
    const makeSelect = document.getElementById('marka');
    const modelSelect = document.getElementById('model');
    const priceForm = document.getElementById('price-form');
    const resultContainer = document.getElementById('result-container');
    const resultText = document.getElementById('result-text');

    // Marka seçiləndə modelləri gətir
    makeSelect.addEventListener('change', async function() {
        const selectedMake = this.value;
        modelSelect.innerHTML = '<option value="" disabled selected>Yüklənir...</option>';
        if (!selectedMake) return;

        try {
            const response = await fetch(`/get_models/${selectedMake}`);
            const models = await response.json();
            
            modelSelect.innerHTML = '<option value="" disabled selected>Model seçin</option>';
            models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
        } catch (error) {
            modelSelect.innerHTML = '<option value="" disabled selected>Xəta baş verdi</option>';
            console.error('Modelləri gətirmək mümkün olmadı:', error);
        }
    });

    // Form göndəriləndə təxmin et
    priceForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = {
            marka: document.getElementById('marka').value,
            model: document.getElementById('model').value,
            il: document.getElementById('il').value,
            yurus: document.getElementById('yurus').value,
            muherrik: document.getElementById('muherrik').value
        };

        resultContainer.classList.remove('hidden');
        resultText.textContent = 'Hesablanır...';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                const formattedPrice = new Intl.NumberFormat('az-AZ').format(data.prediction);
                resultText.textContent = `${formattedPrice} AZN`;
            } else {
                resultText.textContent = `Xəta: ${data.error || 'Naməlum xəta'}`;
            }
        } catch (error) {
            resultText.textContent = 'Server ilə əlaqə qurmaq mümkün olmadı.';
            console.error('Təxmin zamanı xəta:', error);
        }
    });
});