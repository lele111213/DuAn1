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
            success_message: "",
            next: window.location.href.indexOf('next=')
        }
    },
    mounted(){
        document.querySelector('#TenDangNhap').focus()
        if (localStorage.success_message){
            this.success = true
            this.success_message = localStorage.success_message
            localStorage.success_message = ""
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
                            if(this.next != -1){
                                window.location.href = 'http://localhost:8000'+window.location.href.slice(this.next+5).replace('%3F','?').replace('%3D','=')
                            }else{
                                window.location.href = 'http://localhost:8000';
                            }
                        }else{
                            this.errored = true
                            this.error_message = response.data.message
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        this.errored = true
                        this.error_message = error
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
