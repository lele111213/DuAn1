new Vue({
    name:'home',
    delimiters: ["[[", "]]"],
    el: '.content',
    data: {
        user: {
            'uaddressId': null,
            'ugender': null,
            'uage': null
        },
        open: false,
        start: false,
        option: 3,
        errored: null,
        message: null,
        styleColor: null
    },
    created() {
    },
    methods: {
        openGhep (){
            this.open = true
            this.backgroundOpacity = true
        },
        startGhep (){
            let data = {
                option: this.option
            }
            if (this.option==3)
                data.user = this.user
            axios
            .post(
                'http://localhost:8000/api/start_ghep/',data,
                {
                    headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                }
            )
            .then(response => {
                if(response.data.status){
                    this.start = true
                    this.message = "Đang chờ..."
                    this.styleColor = "#aeb900"
                     //handle start
                }
                else{
                    this.errored = true
                    this.styleColor = "red"
                    this.message = response.data.message
                }
            })
            .catch(error => {
                console.log(error)
                this.errored = true
            })
            .finally(() => this.loading = false)
        },
        stopGhep (){
            axios
            .post(
                'http://localhost:8000/api/stop_ghep/',
                {
                    option: this.option
                },
                {
                    headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                }
            )
            .then(response => {
                if(response.data.status){
                    this.start = false
                    this.message = ""
                    //handle stop
                }
                else{
                    this.errored = true
                    this.message = response.data.message   
                }
            })
            .catch(error => {
                console.log(error)
                this.errored = true
            })
            .finally(() => this.loading = false)
        },
        exitGhep (){
            if(this.start){
                confirm("Thoát sẽ dừng ghép cặp, bạn có chắc muốn thoát?")
                this.stopGhep()
            }
            this.open = false
        }
    },
    components:{
    }
})