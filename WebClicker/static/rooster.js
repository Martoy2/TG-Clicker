var count = 0;
var WebApp = window.Telegram.WebApp;
if (WebApp) {
    WebApp.ready();
} else {
    console.error("Telegram WebApp is not available");
}
WebApp.expand()
const api_url = 'https://tiutour.ru/api/v1/click/';
const ticket_url = 'https://tiutour.ru/api/v1/ticket/';
const userName = WebApp.initDataUnsafe.user.username;
const userId = WebApp.initDataUnsafe.user.id;
const userUrl = WebApp.initDataUnsafe.user.photo_url;
const round = (num) => Math.round(num * 100) / 100;

document.getElementById('number').textContent = round(count);
function preloadImagesAndFonts() {
    const fonts = ['/static/Oldtimer-GOPpg.ttf', '/static/IntroHeadR-Base.otf']; // URL вашего шрифта
    const backgroundImages = ['/static/1.svg', '/static/2.svg', '/static/ticket.png']; // URL фоновых изображений

    let loadedCount = 0;

    fetch(api_url + userId + "/")
    .then(response => response.json())
    .then(data => {
        count = round(data['click']);
        updateLoader();
        updateContent();
    });

    fetch(ticket_url)
    .then(response => response.json())
    .then(data => {
        price = data['price'];
        price_text.textContent = price;
        updateLoader();
    });

    const totalCount = fonts.length + backgroundImages.length + 2;

    function updateLoader() {
        loadedCount++;
        const progress = (loadedCount / totalCount) * 100;
        const loaderInner = document.getElementById('loader-inner');
        if (loaderInner) {
            loaderInner.style.width = progress + '%';
        } else {
            console.error('Element with ID loader-inner not found');
        }
        if (loadedCount === totalCount) {
            // Все ресурсы загружены
            setTimeout(() => {
                const loadingText = document.getElementById('loading-text');
                if (loadingText) {
                    loadingText.textContent = 'Загрузка завершена';
                } else {
                    console.error('Element with ID loading-text not found');
                }
                setTimeout(() => {
                    const loaderContainer = document.getElementById('loader-container');
                    const content = document.getElementById('content');
                    document.getElementById('loader-inner').style.opacity = '0';
                    if (loaderContainer && content) {
                        loaderContainer.style.display = 'none';
                        content.style.display = 'block';
                        spiner.style.display = 'none';
                    } else {
                        console.error('Element with ID loader-container or content not found');
                    }
                }, 500);
            }, 500);
        }
    }

    // Загрузка фоновых изображений
    for (let i = 0; i < backgroundImages.length; i++) {
        const bgImage = new Image();
        bgImage.onload = updateLoader;
        bgImage.onerror = updateLoader;
        bgImage.src = backgroundImages[i];
    }

    // Загрузка шрифта
    for (let i = 0; i < fonts.length; i++) {
        const font = new FontFace(fonts[i].name, `url(${fonts[i]})`);
        font.load().then(function(loadedFont) {
            document.fonts.add(loadedFont);
            updateLoader();
        }).catch(function(error) {
            console.error('Ошибка загрузки шрифта:', error);
            updateLoader();
        });
    }
}

// Вызов функции загрузки ресурсов при загрузке страницы
window.onload = preloadImagesAndFonts;

const coin = document.getElementById('coin');
const number = document.getElementById('number');
const progress = document.getElementById('progress');
const menu = document.getElementById('menu');
const change_menu = document.getElementById('change');
const plus = document.getElementById('plus');
const minus = document.getElementById('minus');
const count_text = document.getElementById('count_text');
const price_text = document.getElementById('price_text');
const change_button = document.getElementById('change_button');
const button1 = document.getElementById('button1');
let ticket_count = 1;
var click_sk = 0;
var price = 0;



button1.addEventListener('click', () =>{
    ticket_count = 1;
    count_text.textContent = ticket_count;
    coin.style.display = 'none';
    menu.style.display = 'none';
    change_menu.style.display = 'flex';
    WebApp.BackButton.show();
});

WebApp.onEvent('backButtonClicked', function(){
    coin.style.display = 'block';
    menu.style.display = 'block';
    change_menu.style.display = 'none';
    WebApp.BackButton.hide();
});

plus.addEventListener('click', () =>{
    if(ticket_count === 10){
        WebApp.showPopup({title: "Предупреждение!", message: "Нельзя обменять более 10 билетов за раз."});
    } else {
        ticket_count++;
        count_text.textContent = ticket_count;
    }
});

minus.addEventListener('click', () =>{
    if(ticket_count <= 1){
        WebApp.showPopup({title: "Предупреждение!", message: "Нельзя обменять менее 1 билета."});
    } else {
        ticket_count--;
        count_text.textContent = ticket_count;
    }
});

change_button.addEventListener('click', async function(e){
    await getPrice();
    await updateCount();
    if(ticket_count >10 || ticket_count <1){
        WebApp.showPopup({title: "Ошибка", message: "Количество биллетов должно быть от 1 до 10."});
    } else if (ticket_count * price > count){
        WebApp.showPopup({title: "Ошибка", message: "Вам не хватает Petuch Coin."});
    } else{
        WebApp.showPopup({title: "Подтверждение", message: "Вы собираетесь обменять " + round(ticket_count*price) + " Petuch Coin на " + ticket_count + " биллет(a/ов).", buttons:[{type: "cancel", text: "Отмена", id: 'cancel'}, {type: 'ok', text: "Ok", id: 'ok'}]})
    }
});

WebApp.onEvent('popupClosed', async function(event) {
    if (event.button_id === 'ok') {
        await sendTicket();
        await updateCount();
    } else if (event.button_id === 'cancel') {
        await updateCount();
    }
});


coin.addEventListener('click', function(e) {
    click_sk++;
    count++;
    number.textContent = round(count);

    createPlusOneElement(e.clientX, e.clientY);

    if (click_sk % 3 === 0) {
        click_sk=0;
        sendDataToServer();
    }
});

async function getPrice(){
    fetch(ticket_url)
    .then(response => response.json())
    .then(data => {
        price = data['price'];
        price_text.textContent = price;
        return price;
    });
}

setInterval(getPrice, 60000);


async function sendDataToServer() {
    const data = {
        user_id: userId,
        clicks: 3,
    };

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('Success:', response);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function sendTicket() {
    //await getPrice();
    const data = {
        user_id: userId,
        ticket: ticket_count,
        coin: round(ticket_count*price),
    };

    try {
        const response = await fetch(ticket_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const responseData = await response.json();
            console.log('Response Data:', responseData);
            console.log(data['coin']);
            throw new Error('Network response was not ok.');
        }
        console.log('Success:', response);
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateContent() {
    document.getElementById('number').textContent = round(count);
    //progressPercentage = (count % 100) + '%';
    //progress.style.width = progressPercentage;
}

document.body.addEventListener('touchmove', function(e) {
    e.preventDefault();
}, { passive: false });

document.body.addEventListener('wheel', function(e) {
    e.preventDefault();
}, { passive: false });

function createPlusOneElement(x, y) {
    const existingPlusOnes = document.querySelectorAll('.plus-one');
    if (existingPlusOnes.length > 10) {
        existingPlusOnes[0].remove();
    }

    const plusOne = document.createElement('div');
    plusOne.textContent = '+1';
    plusOne.className = 'plus-one';
    plusOne.style.left = x + 'px';
    plusOne.style.top = y + 'px';
    document.body.appendChild(plusOne);

    setTimeout(() => {
        plusOne.remove();
    }, 1000);
}

async function updateCount(){
    fetch(api_url + userId + "/")
    .then(response => response.json())
    .then(data => {
        count = data['click'];
        updateContent();
    });
    return count;
}