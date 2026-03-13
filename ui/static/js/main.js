async function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const msgDiv = document.getElementById('message');
    const resultContainer = document.getElementById('result-container');
    const analysisText = document.getElementById('analysis-text');
    const token = localStorage.getItem('userToken');

    if (!fileInput.files[0]) {
        alert("Будь ласка, виберіть файл!");
        return;
    }

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    msgDiv.innerText = "⏳ Завантаження фото...";
    resultContainer.style.display = 'none';

    try {
        // КРОК 1: Завантажуємо фото
        const response = await fetch('/api/analysis/upload/', {
            method: 'POST',
            headers: { 'Authorization': `Token ${token}` },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            const instanceId = data.id; // Отримуємо ID створеного запису
            msgDiv.innerText = "🤖 Штучний інтелект аналізує (зачекайте)...";

            // КРОК 2: Починаємо опитування (Polling)
            pollResult(instanceId, token);
        } else if (response.status === 401) {
            alert("Сесія закінчилася. Увійдіть знову.");
            logout();
        } else {
            msgDiv.innerText = "❌ Помилка завантаження: " + (data.error || "Щось пішло не так");
        }
    } catch (error) {
        msgDiv.innerText = "🔌 Помилка з'єднання";
    }
}

// Нова функція для перевірки результату
async function pollResult(id, token) {
    const msgDiv = document.getElementById('message');
    const resultContainer = document.getElementById('result-container');
    const analysisText = document.getElementById('analysis-text');

    const checkStatus = async () => {
        try {
            // Робимо GET запит на деталі об'єкта за ID
            const response = await fetch(`/api/analysis/upload/${id}/`, {
                headers: { 'Authorization': `Token ${token}` }
            });
            const data = await response.json();

            if (data.analysis_result) {
                // Якщо текст з'явився - показуємо його і зупиняємо цикл
                msgDiv.innerText = "✅ Аналіз завершено!";
                analysisText.innerText = data.analysis_result;
                resultContainer.style.display = 'block';
                clearInterval(pollingInterval);
            }
        } catch (e) {
            console.error("Помилка при опитуванні:", e);
        }
    };

    // Запускаємо перевірку кожні 2 секунди
    const pollingInterval = setInterval(checkStatus, 2000);

    // Тайм-аут: зупиняємо через 60 секунд, щоб не зациклилось вічно
    setTimeout(() => {
        if (clearInterval(pollingInterval)) {
            msgDiv.innerText = "⏳ Час очікування вийшов. Спробуйте оновити сторінку.";
        }
    }, 60000);
}