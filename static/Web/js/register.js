new Vue({
    delimiters: ["[[", "]]"],
    el: '#formRegister',
    data () {
        return {
            form: {
                TenDangNhap: "",
                HoTen: "",
                SoDT: "",
                MatKhau: "",
                MatKhau2: "",
                DiaChi: "",
                GioiTinh: ""
            },
            error_message: "",
            errored: false,
            info: null,
            loading: true,
        }
    },

    methods: {
        submitRegister () {
            const tenDangNhapIsValid = !!this.form.TenDangNhap
            const matKhauIsValid = !!this.form.MatKhau
            const matKhau2IsValid = this.form.MatKhau2 == this.form.MatKhau
            const hoTenIsValid = !!this.form.HoTen
            const soDienIsThoaiValid = !!this.form.SoDT
            const diaChiIsValid = !!this.form.DiaChi
            const gioiTinhIsValid = !!this.form.GioiTinh

            const formIsValid = tenDangNhapIsValid && matKhauIsValid && matKhau2IsValid && hoTenIsValid && soDienIsThoaiValid && diaChiIsValid && gioiTinhIsValid
            if(formIsValid){
                axios
                    .post(
                            'http://localhost:8000/register/',
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
                            localStorage.success_message = response.data.message
                            setTimeout(() => window.location.href = "http://localhost:8000/login", 1000);
                        }else{
                            this.errored = true
                            this.error_message = response.data.message
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        this.errored = true
                    })
                    .finally(() => this.loading = false)
            }
            if(!this.errored)
                this.error_message = formIsValid ? "" : matKhauIsValid && !matKhau2IsValid ? "Nhập lại mật khẩu không chích xác!" : "Hãy nhập hết các trường!"
        },
    }
})