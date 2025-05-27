
const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');
const statusText = document.getElementById('status');
const messages = document.getElementById('messages');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const message = input.value;
    if (!message) return;

    statusText.innerText = "Enviando...";
    
    fetch('/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `message=${encodeURIComponent(message)}`
    })
    .then(res => {
        if (res.ok) {
            statusText.innerText = "Mensagem enviada!";
            input.value = '';
            updateMessages();
        } else {
            statusText.innerText = "Erro ao enviar";
        }
    })
    .catch(err => {
        statusText.innerText = "Erro de conexão";
    });
});

function updateMessages() {
    fetch('/messages')
        .then(res => res.json())
        .then(data => {
            messages.innerHTML = '';
            data.forEach(msg => {
                const newMsg = document.createElement('div');
                newMsg.innerHTML = `${msg.message} &nbsp;&nbsp;&nbsp; <sub>${msg.datetime}</sub>`;
                if (msg.sender === 'Eu'){
                    newMsg.classList.add('msg-sent');
                }
                else if (msg.receiver === 'Eu'){
                    newMsg.classList.add('msg-received');
                }
                else{
                    newMsg.classList.add('msg-system');
                }
                messages.appendChild(newMsg);
            });
            messages.scrollTop = messages.scrollHeight;
        });
}


setInterval(updateMessages, 1500);
