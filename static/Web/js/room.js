
new Vue({
    name:'room',
    delimiters: ["[[", "]]"],
    el: '.section',
    data: {
        user: {
            'uname': null,
            'room_id': null,
            'image': null,
            'room_title': null,
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
                    room_id: window.location.pathname.split('/')[2],
                },
                {
                    headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                }
            ).then(response => {
                this.messages = response.data.messages
                this.user.uname = response.data.username
                this.user.room_id = window.location.pathname.split('/')[2]
                this.user.image = response.data.image
                this.user.room_title = response.data.room_title

                this.chatSocket = new WebSocket('ws://' + window.location.host + '/ws/' + this.user.room_id + '/')
                var ms = {}
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
            }).catch(error => {
                console.log(error)
                this.errored = true
            })
    

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