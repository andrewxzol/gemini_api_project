// Відображаємо ім'я користувача
document.getElementById('display-username').innerText = localStorage.getItem('username') || 'Друже';

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

    msgDiv.innerText = "⏳ Завантаження та аналіз (це може зайняти до 10 сек)...";
    resultContainer.style.display = 'none';

    try {
        const response = await fetch('/api/upload/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}` // ПЕРЕДАЄМО ТОКЕН ТУТ
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            msgDiv.innerText = "✅ Готово!";
            analysisText.innerText = data.analysis_result;
            resultContainer.style.display = 'block';
        } else if (response.status === 401) {
            alert("Сесія закінчилася. Увійдіть знову.");
            logout();
        } else {
            msgDiv.innerText = "❌ Помилка: " + (data.error || "Щось пішло не так");
        }
    } catch (error) {
        msgDiv.innerText = "🔌 Помилка з'єднання";
    }
}

function logout() {
    localStorage.clear(); // Видаляємо токен та ім'я
    window.location.href = '/login/';
}