async function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('message');

    msgDiv.innerText = "Перевірка...";
    msgDiv.style.color = "#666";

    try {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Зберігаємо токен для подальших запитів
            localStorage.setItem('userToken', data.token);
            localStorage.setItem('username', data.username);

            msgDiv.innerText = "Успішний вхід! Перенаправлення...";
            msgDiv.style.color = "#28a745";

            // Через 1 секунду перекидаємо на головну
            setTimeout(() => {
                window.location.href = '/dashboard/';
            }, 1000);
        } else {
            msgDiv.innerText = "❌ Помилка: " + (data.non_field_errors || "Невірні дані");
            msgDiv.style.color = "#dc3545";
        }
    } catch (error) {
        msgDiv.innerText = "🔌 Помилка з'єднання з сервером";
        msgDiv.style.color = "#dc3545";
    }
}