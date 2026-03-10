async function registerUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('message');

    try {
        const response = await fetch('/api/registration/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (response.ok) {
            msgDiv.innerText = "Успіх! Користувача створено.";
            msgDiv.style.color = "green";
        } else {
            const data = await response.json();
            msgDiv.innerText = "Помилка: " + JSON.stringify(data);
            msgDiv.style.color = "red";
        }
    } catch (error) {
        msgDiv.innerText = "Помилка мережі";
        msgDiv.style.color = "red";
    }
}