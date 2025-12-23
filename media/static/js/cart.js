// Получаем CSRF-токен из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Закрытие уведомления
function closeNotification() {
    document.getElementById('add-to-cart-notification').style.display = 'none';
}

// Добавление товара в корзину (мгновенно показывает кнопки + / –)
function addToCart(productId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            if (data && data.success) {
                document.getElementById('notification-message').innerText = data.message;
                document.getElementById('add-to-cart-notification').style.display = 'block';

                // Показываем кнопки + / – с количеством 1
                const container = document.querySelector(`div[data-product-id="${productId}"]`);
                if (container) {
                    container.querySelector('.quantity-buttons').style.display = 'inline-flex';
                    container.querySelector('.qty-number').innerText = '1';
                    container.querySelector('.add-to-cart-btn').style.display = 'none';
                }
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

// Изменение количества (кнопки + / –)
function changeQty(button, delta) {
    const container = button.closest('[data-product-id]');
    const qtyNumber = container.querySelector('.qty-number');
    let current = parseInt(qtyNumber.innerText) || 0;
    let newQty = current + delta;

    if (newQty < 1) {
        // Если стало 0 — удаляем строку из корзины
        container.remove();
        newQty = 0;
    } else {
        qtyNumber.innerText = newQty;
    }

    const productId = container.getAttribute('data-product-id');
    const csrftoken = getCookie('csrftoken');

    fetch(`/cart/update/${productId}/${newQty}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('notification-message').innerText = `Количество: ${newQty} шт.`;
            document.getElementById('add-to-cart-notification').style.display = 'block';
        })
        .catch(error => console.error('Ошибка:', error));
}

// Функция для удаления товара (если нужна отдельная)
function removeItem(productId) {
    const container = document.querySelector(`[data-product-id="${productId}"]`);
    changeQty(container.querySelector('button'), -999); // Удаляем все количество
}