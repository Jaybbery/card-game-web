const tg = window.Telegram.WebApp;

// Инициализация
tg.expand();
tg.BackButton.hide();

// Загрузка данных игрока
async function loadData() {
    const user = tg.initDataUnsafe.user;
    const response = await fetch(`https://ваш-хостинг.herokuapp.com/api/user?id=${user.id}`);
    const data = await response.json();
    
    document.getElementById('coins').textContent = data.coins;
    renderCards(data.cards);
}

// Открытие бустера
async function openBooster(type) {
    const user = tg.initDataUnsafe.user;
    const response = await fetch(`https://ваш-хостинг.herokuapp.com/api/open_booster`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, type: type })
    });

    const result = await response.json();
    if (result.success) {
        tg.showAlert(`🎉 Вы получили карту: ${result.card.name}`);
        loadData(); // Обновляем интерфейс
    } else {
        tg.showAlert(`❌ Ошибка: ${result.error}`);
    }
}

// Отображение карт
function renderCards(cards) {
    const grid = document.getElementById('cards');
    grid.innerHTML = cards.map(card => `
        <div class="card">
            <h3>${card.name}</h3>
            <img src="${card.image_url}" width="100">
        </div>
    `).join('');
}

// Запуск при загрузке
loadData();
