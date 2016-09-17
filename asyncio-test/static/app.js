'use strict';

let loc = document.location
let ws = new WebSocket('ws://' + loc.host + loc.pathname + 'websocket/')

ws.onopen = () => {
  console.log('Websocket opened');
}

ws.onclose = () => {
  console.log('Websocket closed');
}

ws.onmessage = (evt) => {
  let obj = JSON.parse(evt.data)
  let para = $('<p>')
  if (obj.type === 'name') {
    para.text('Your assigned name is ' + obj.value)
  } else if (obj.type === 'message') {
    para.text(obj.value)
  }
  let messages = $('#messages')
  para.appendTo(messages)
  messages.scrollTop(para.offset().top - messages.offset().top + messages.scrollTop())
}


$('button.start').on('click', () => {
  let data = JSON.stringify({
    command: 'start',
    stop: parseInt($('input').val())
  })
  console.log(data);
  ws.send(data)
})

$('input').keypress((evt) => {
    if(evt.keyCode === 13) {
        $('button.start').click();
    }
})
