var userInfo = {
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            
        }
    },
    template: `
        <h1>[[ this.$root.user.ufullname ]]</h1>
    `
}
var userInfomation = {
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            selects: [
                {'title':"Thông tin tài khoản",'load':'thongtin'},
                {'title':"Lịch sử ghép cặp", 'load':'lichsu'}
            ]
            
        }
    },
    methods:{
        click(){
            
        }
    },
    template: `
    <div class="side-nav">
        <div v-for="select in selects" class="user-infomation">
            <a :title="select.title" v-on:click="$root.select=select" href="#">[[ select.title ]]</a>
        </div>
    </div>
    `
}

new Vue({
    name:'userinfo',
    delimiters: ["[[", "]]"],
    el: '.content',
    data: {
        user: {},
        image_update: null,
        errored: null,
        success: null,
        message: null,
        loading: null,
        select: {'title':"Thông tin tài khoản",'load':'thongtin'}
    },
    updated() {
        if(this.user.uaddressId){
            this.user.uaddressName = document.querySelector('option[value ="'+this.user.uaddressId+'"]').innerText
        }
    },
    created() {
        axios
            .get('http://localhost:8000/api/get_user_info/')
            .then(response => {
                if(response.data.status){
                    this.user = response.data.user
                }else{
                    this.errored = true
                    this.message = response.data.message
                }
            })
            .catch(error => {
                console.log(error)
            })
    },
    mounted(){
        if (localStorage.success_message){
            this.success = true
            this.message = localStorage.success_message
            localStorage.success_message = ""
        }
    },
    methods: {
        submitChangeUser () {
            if(this.image_update)
            {
                let formData = new FormData()
                formData.append('image', this.image_update)
                axios
                    .post(
                        'http://localhost:8000/api/update_user_image/',
                        formData,
                        {
                            headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                        }
                    ).catch(error => {
                        console.log(error)
                        this.errored = true
                    })
            }
            axios
                .post(
                        'http://localhost:8000/api/update_user/',
                        {
                            user: this.user
                        },
                        {
                            headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                        }
                    )
                .then(response => {
                    if(response.data.status){
                        localStorage.success_message = response.data.message
                        window.location.reload()
                    }
                    else
                        this.errored = true
                    this.message = response.data.message
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => this.loading = false)
        },
        handleImage (){
            let image = this.$refs.fileImage.files[0]
            console.log(image);
            let format = image.name.split('.',3)[1]
            if(image.size > 5242888)
            {
                this.message = "File quá lớn"
                this.errored = true
            }
            else if(format!='png' && format != 'jpg'){
                console.log(format);
                this.message = "Định dạng file không đúng!"
                this.errored = true
            }else{
                this.image_update = image
            }
        }
    },
    components:{
        'user-info': userInfo,
        'user-infomation': userInfomation
    }
})

