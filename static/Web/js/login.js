new Vue({
    delimiters: ["[[", "]]"],
    el: '#formLogin',
    data () {
        return {
            form: {
                TenDangNhap: null,
                MatKhau: null
            },
            error_message: "",
            info: null,
            errored: false,
            success: false,
            success_message: ""
        }
    },
    mounted(){
        if (localStorage.success_message){
            this.success = true
            this.success_message = localStorage.success_message
            setTimeout(()=>localStorage.success_message = "", 3000)
        }
    },
    methods: {
        submitLogin () {
            const tenDangNhapIsValid = !!this.form.TenDangNhap
            const matKhauIsValid = !!this.form.MatKhau
            const formIsValid = tenDangNhapIsValid && matKhauIsValid
            this.errored = false
            this.success = false
            if(formIsValid){
                this.error_message = ""
                axios
                    .post(
                            'http://localhost:8000/login/',
                            {
                                username: this.form.TenDangNhap,
                                password: this.form.MatKhau
                            },
                            {
                                headers: {'X-CSRFToken': window.$cookies.get('csrftoken')}
                            }
                        )
                    .then(response => {
                        if(response.data.status){
                            this.success = true
                            this.success_message = response.data.message
                            setTimeout(() => window.location.href = "http://localhost:8000", 1000);
                        }else{
                            this.errored = true
                            this.error_message = response.data.message
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        this.errored = true
                        this.error_message = response.data.message
                    })
            }
            else{
                this.errored = true
                this.error_message = "Hãy nhập hết các trường!"
            }
        },
        onFocus () {
            this.error_message = ""
        }
    }
})
