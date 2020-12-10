


const roomName = JSON.parse(document.getElementById('room_id').textContent);
const userName = JSON.parse(document.getElementById('user_id').textContent);
const chatLog = JSON.parse(message_log.textContent);
const usersLog = JSON.parse(users_log.textContent);
console.log(usersLog.length);
const userpanel = document.querySelector("#usersinroom")
console.log(usersLog);
const textarea = document.querySelector(`#chat-log`);

function printToChat(message){
    document.querySelector('#chat-log').value += message;
}
for(var i = 0; i < chatLog.length; i++){

    printToChat((chatLog[i]['fields']['username'] + ':\n\t' + chatLog[i]['fields']['content'] +'\n'));
}
for(var i = 0; i < usersLog.length; i++){
    let element = document.createElement('div');
    let element2 = document.createElement('a');
    
    element2.href="/profile/" + usersLog[i]['fields']['user'];
    element2.innerHTML = usersLog[i]['fields']['username'];
    element.appendChild(element2);
    userpanel.appendChild(element)
}
let element = document.createElement('div');
element.innerHTML = userName;
userpanel.appendChild(element);


console.log(chatLog)
textarea.scrollTop = textarea.scrollHeight;
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    printToChat((userName + ':\n\t' + data.message + '\n'));
    textarea.scrollTop = textarea.scrollHeight;
    
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
        
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message' : message,
        'roomName' : roomName,
    }));
    messageInputDom.value = '';
    
};



