async function registerUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('message');

    // 1. Статус: Завантаження
    msgDiv.className = "loading-alert";
    msgDiv.innerText = "⏳ Creating account...";

    try {
        const response = await fetch('/api/auth/register/', { // ПЕРЕВІР СВІЙ URL
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // 2. Статус: Успіх
            msgDiv.className = "success-alert";
            msgDiv.innerText = "✅ Account created!";

            setTimeout(() => { window.location.href = '/login/'; }, 1500);
        } else {
            // 3. РОЗБИРАЄМО ПОМИЛКИ З JSON
            msgDiv.className = "error-alert";

            // Створюємо масив для гарних повідомлень
            let errorText = "";

            // Проходимось по кожному полю з помилкою (наприклад, "password", "username")
            for (const [field, messages] of Object.entries(data)) {
                // Перекладаємо системні назви полів на наші, людські
                let fieldName = field;
                if (field === 'username') fieldName = 'Login';
                if (field === 'email') fieldName = 'Email';
                if (field === 'password') fieldName = 'Password';
                if (field === 'non_field_errors') fieldName = 'Error';

                // Додаємо в текст (messages зазвичай це масив, тому беремо перший елемент)
                errorText += `${fieldName}: ${messages[0]}\n`;
            }

            // Виводимо красу на екран
            msgDiv.innerText = errorText.trim();
        }
    } catch (error) {
        msgDiv.className = "error-alert";
        msgDiv.innerText = "🔌 Помилка з'єднання з сервером";
    }
}