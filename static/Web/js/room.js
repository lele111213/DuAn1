
new Vue({
    name:'room',
    delimiters: ["[[", "]]"],
    el: '.section',
    data: {
        user: {
            'uname': null,
            'room_id': 1,
            'image': null,
        },
        messages: [],
        chatSocket: null
    },
    mounted (){
        document.querySelector('#chat-message-input').focus()
    }
    ,
    created (){
        axios
            .post(
                'http://localhost:8000/api/get_room_chat/',
                {
                    'room_id': this.user.room_id
                },
                {
                    headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                }
            ).then(response => {
                this.messages = response.data.messages
                this.user.uname = response.data.username
                this.room_id = response.data.room_id
                this.user.image = response.data.image
            }).catch(error => {
                console.log(error)
                this.errored = true
            })
        var ms = {}
        this.chatSocket = new WebSocket('ws://' + window.location.host + '/ws/' + this.user.room_id + '/')
        this.chatSocket.onmessage = (e) => {
            
            const data = JSON.parse(e.data)
            if (data.message) {
                ms = data.message
                this.messages.push(ms)
            }
        }
            
        this.chatSocket.onclose = function(e) {
            alert("Có lỗi xảy ra, hãy đăng nhập lại!")
        }

    },
    updated (){
        this.scrollToBottom()
    },
    methods: {
        sendMessage() {
            const messageInputDom = document.querySelector('#chat-message-input')
            const message = messageInputDom.value
            if (!message) {
                alert('Không thể nhập khoảng trống')
                return
            }
            this.chatSocket.send(JSON.stringify({
                'message': message,
                'room': this.user.room_id,
                'image': this.user.image
            }))

            messageInputDom.value = ''
        },
        scrollToBottom() {
            let objDiv = document.getElementById("chat-messages")
            objDiv.scrollTop = objDiv.scrollHeight
        },
    },
    components:{
    }
})