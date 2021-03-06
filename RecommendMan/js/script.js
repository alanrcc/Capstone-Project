
var ws=new WebSocket('ws://127.0.0.1:10083');
var messageBody = document.querySelector('#chat-wrapper');
function send(){
    if(document.getElementById("chat-input").value){
        var date = new Date();
        document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">'+ document.getElementById("chat-input").value +'</div><span>'+date+'</span></div></div>';
        if(ws){
             ws.send(document.getElementById("chat-input").value);
        }
         ws.onmessage=function(evt){
             console.log("fdsa");
             isUrl = isValidHttpUrl(evt.data)
             if (isUrl) {
                 //var img = new Image();
                 document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box" style="width:310px;height:390px;"><img src="' + evt.data + '" style="width:230px;height:370px;"></div><span>' + date + '</span></div></div>';
             }
             else {
                 document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">' + evt.data + '</div><span>' + date + '</span></div></div>';
             }
             messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
        };
    }else{
        alert("Empty message is not allowed!");
    }
    document.getElementById("chat-input").value = "";
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
}

function isValidHttpUrl(string) {
    let url;

    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }

    return url.protocol === "http:" || url.protocol === "https:";
}

function clear_his(){
    document.getElementById('chat-wrapper').innerHTML = '';
}

function show_actor(){
    if(ws){
             ws.send("list");
        }
         ws.onmessage=function(evt){
             console.log("fdsa");
             isUrl = isValidHttpUrl(evt.data)
             if (isUrl) {
                 //var img = new Image();
                 document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box" style="width:310px;height:390px;"><img src="' + evt.data + '" style="width:230px;height:370px;"></div><span>' + date + '</span></div></div>';
             }
             else {
                 document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">' + evt.data + '</div><span>' + date + '</span></div></div>';
             }
             messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
        };
}

function quickie() {
    var date = new Date();
    document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">' + "GO!" + '</div>';
    if (ws) {
        ws.send("QUICK");
    }
    ws.onmessage = function (evt) {
        console.log("fdsa");
        isUrl = isValidHttpUrl(evt.data)
        if (isUrl) {
            //var img = new Image();
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box" style="width:310px;height:390px;"><img src="' + evt.data + '" style="width:230px;height:370px;"></div><span>' + date + '</span></div></div>';
        }
        else {
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">' + evt.data + '</div><span>' + date + '</span></div></div>';
        }
        messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
    };
}

function changeBot(id){
    var date = new Date();
    switch(id){
        case "movieBot":
            document.getElementById("movieBot").className = "chat-list-item active";
            document.getElementById("actorBot").className = "chat-list-item";
            document.getElementById("preferBot").className = "chat-list-item";
            document.getElementById("profileImage").src = "img/1.jpg";
            document.getElementById("rightProfileImage").src = "img/1.jpg";
            document.getElementById("botName").textContent = "Movie Recommend-Man";
            document.getElementById("botInstruction").textContent = "Movie Recommend-Man Introduction";
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">'+"Welcome! I am Movie Recommend-Man! I can recommend you movies based on your input!"+'</div><span>'+date+'</span></div></div>';
            break;
        case "actorBot":
            document.getElementById("movieBot").className = "chat-list-item";
            document.getElementById("actorBot").className = "chat-list-item active";
            document.getElementById("preferBot").className = "chat-list-item";
            document.getElementById("profileImage").src = "img/2.jpg";
            document.getElementById("rightProfileImage").src = "img/2.jpg";
            document.getElementById("botName").textContent = "Actor Recommend-Man";
            document.getElementById("botInstruction").textContent = "Actor Recommend-Man Introduction";
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">'+"Welcome! I am Actor Recommend-Man! I can recommend you actors based on your input!"+'</div><span>'+date+'</span></div></div>';
            break;
        case "preferBot":
            document.getElementById("movieBot").className = "chat-list-item";
            document.getElementById("actorBot").className = "chat-list-item";
            document.getElementById("preferBot").className = "chat-list-item active";
            document.getElementById("profileImage").src = "img/3.jpg";
            document.getElementById("rightProfileImage").src = "img/3.jpg";
            document.getElementById("botName").textContent = "Preference Manager";
            document.getElementById("botInstruction").textContent = "Preference Manager Introduction";
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">'+"Welcome! I am your preference manager! I can help you to modify your preferences!"+'</div><span>'+date+'</span></div></div>';
            break;
        default:

    }
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
}

const themeColors = document.querySelectorAll('.theme-color');

themeColors.forEach(themeColor => {
  themeColor.addEventListener('click', e => {
    themeColors.forEach(c => c.classList.remove('active'));
    const theme = themeColor.getAttribute('data-color');
    document.body.setAttribute('data-theme', theme);
    themeColor.classList.add('active');
  });});

