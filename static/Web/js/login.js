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
            success_message: "",
            info: null,
            errored: false,
            success: false
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
                        this.success = true
                        this.success_message = response.data.message
                        setTimeout(() => window.location.href = "http://localhost:8000", 1000);
                    })
                    .catch(error => {
                        console.log(error)
                        this.errored = true
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
