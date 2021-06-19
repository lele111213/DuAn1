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
            info: null,
            loading: true,
            errored: false
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
                        this.info = response.data
                    })
                    .catch(error => {
                        console.log(error)
                        this.errored = true
                    })
                    .finally(() => this.loading = false)
            }
            this.error_message = formIsValid ? "" : matKhauIsValid && !matKhau2IsValid ? "Nhập lại mật khẩu không chích xác!" : "Hãy nhập hết các trường!"
        },
    }
})