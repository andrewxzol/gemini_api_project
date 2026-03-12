async function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('message');

    msgDiv.innerText = "Перевірка...";
    msgDiv.className = "loading-alert"; // Додаємо сірий клас

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
            msgDiv.className = "success-alert"; // Додаємо зелений клас

            // Через 1 секунду перекидаємо на головну
            setTimeout(() => {
                window.location.href = '/dashboard/';
            }, 1000);
        } else {
            msgDiv.innerText = "Введено невірний логін або пароль";
            msgDiv.className = "error-alert"; // Додаємо червоний клас
        }
    } catch (error) {
        msgDiv.innerText = "🔌 Помилка з'єднання з сервером";
        msgDiv.style.color = "#dc3545";
    }
}
