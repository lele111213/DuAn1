new Vue({
    name:'home',
    delimiters: ["[[", "]]"],
    el: '.content',
    data: {
        user: {
            'uaddressId': 999,
            'ugender': null,
            'uage': ''
        },
        open: false,
        start: false,
        option: 3,
        errored: null,
        message: null,
        styleColor: null,
        homeSocket: null
    },
    created() {
    },
    methods: {
        openGhep (){
            axios.get(
                'http://localhost:8000/api/open_ghep/'
            ).then(response => {
                if(response.data.status){
                    this.open = true
                    this.backgroundOpacity = true
                }
                else{
                    window.location.href = 'http://localhost:8000/login/?next=/'
                }
            })
        },
        startGhep (){
            this.start = true
            this.message = "Đang chờ."
            this.styleColor = "#aeb900"
            if (this.option == 3){
                this.homeSocket = new WebSocket('ws://' + window.location.host + '/ws/ghep/' + this.option + '/' + (this.user.uage || 999) + '/' + this.user.ugender + '/' + this.user.uaddressId + '/')
            }    
            else
                this.homeSocket = new WebSocket('ws://' + window.location.host + '/ws/ghep/' + this.option + '/')
            this.homeSocket.onmessage = (e) => {
                console.log(e);
                const data = JSON.parse(e.data)
                if (data.status==1){
                    alert("Ghép thành công!")
                    window.location.href = 'http://localhost:8000/room/' + data.room_id + '/'
                }
            }
            this.homeSocket.onclose = function(e) {
                if (e.code != 1000)
                    alert("Có lỗi xảy ra, hãy đăng nhập lại!")
            }
        },
        stopGhep (){

            this.homeSocket.close()
            this.start = false
            this.message = ""

        },
        exitGhep (){
            if(this.start){
                if(confirm("Thoát sẽ dừng ghép cặp, bạn có chắc muốn thoát?")){
                    this.stopGhep()
                    this.message = ""
                    this.open = false
                }
            }
            else
                this.open = false
        }
    },
    components:{
    }
})