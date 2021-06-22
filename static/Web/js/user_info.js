var userInfoTemplate = {
    delimiters: ["[[", "]]"],
    template: `
    <div class="content-form">
        <span v-if="success || errored" v-bind:class="{ success: success, 'errored': errored }" class="message">[[ message ]]</span>
        <form @submit.prevent="submitChangeUser" action="" method="POST">
            <div class="form-input">
                <div class="input-row">
                    <label class="input-lable">Tên đầy đủ</label>
                    <input v-if="user.ufullname || user.ufullname==''" v-model="user.ufullname" v-bind:placeholder="user.ufullname" v-once type="text" name="fullname">
                </div>
                <div class="input-row">
                    <label class="input-lable">Địa chỉ (tỉnh, thành phố)</label>
                    <select v-model="user.uaddressId" aria-label="Default select example">

                        <option value=1>Thành phố Hà Nội</option>
                    
                        <option value=2>Tỉnh Hà Giang</option>
                    
                        <option value=4>Tỉnh Cao Bằng</option>
                    
                        <option value=6>Tỉnh Bắc Kạn</option>
                    
                        <option value=8>Tỉnh Tuyên Quang</option>
                    
                        <option value=10>Tỉnh Lào Cai</option>
                    
                        <option value="11">Tỉnh Điện Biên</option>
                    
                        <option value="12">Tỉnh Lai Châu</option>
                    
                        <option value="14">Tỉnh Sơn La</option>
                    
                        <option value="15">Tỉnh Yên Bái</option>
                    
                        <option value="17">Tỉnh Hoà Bình</option>
                    
                        <option value="19">Tỉnh Thái Nguyên</option>
                    
                        <option value="20">Tỉnh Lạng Sơn</option>
                    
                        <option value="22">Tỉnh Quảng Ninh</option>
                    
                        <option value="24">Tỉnh Bắc Giang</option>
                    
                        <option value="25">Tỉnh Phú Thọ</option>
                    
                        <option value="26">Tỉnh Vĩnh Phúc</option>
                    
                        <option value="27">Tỉnh Bắc Ninh</option>
                    
                        <option value="30">Tỉnh Hải Dương</option>
                    
                        <option value="31">Thành phố Hải Phòng</option>
                    
                        <option value="33">Tỉnh Hưng Yên</option>
                    
                        <option value="34">Tỉnh Thái Bình</option>
                    
                        <option value="35">Tỉnh Hà Nam</option>
                    
                        <option value="36">Tỉnh Nam Định</option>
                    
                        <option value="37">Tỉnh Ninh Bình</option>
                    
                        <option value="38">Tỉnh Thanh Hóa</option>
                    
                        <option value="40">Tỉnh Nghệ An</option>
                    
                        <option value="42">Tỉnh Hà Tĩnh</option>
                    
                        <option value="44">Tỉnh Quảng Bình</option>
                    
                        <option value="45">Tỉnh Quảng Trị</option>
                    
                        <option value="46">Tỉnh Thừa Thiên Huế</option>
                    
                        <option value="48">Thành phố Đà Nẵng</option>
                    
                        <option value="49">Tỉnh Quảng Nam</option>
                    
                        <option value="51">Tỉnh Quảng Ngãi</option>
                    
                        <option value="52">Tỉnh Bình Định</option>
                    
                        <option value="54">Tỉnh Phú Yên</option>
                    
                        <option value="56">Tỉnh Khánh Hòa</option>
                    
                        <option value="58">Tỉnh Ninh Thuận</option>
                    
                        <option value="60">Tỉnh Bình Thuận</option>
                    
                        <option value="62">Tỉnh Kon Tum</option>
                    
                        <option value="64">Tỉnh Gia Lai</option>
                    
                        <option value="66">Tỉnh Đắk Lắk</option>
                    
                        <option value="67">Tỉnh Đắk Nông</option>
                    
                        <option value="68">Tỉnh Lâm Đồng</option>
                    
                        <option value="70">Tỉnh Bình Phước</option>
                    
                        <option value="72">Tỉnh Tây Ninh</option>
                    
                        <option value="74">Tỉnh Bình Dương</option>
                    
                        <option value="75">Tỉnh Đồng Nai</option>
                    
                        <option value="77">Tỉnh Bà Rịa - Vũng Tàu</option>
                    
                        <option value="79">Thành phố Hồ Chí Minh</option>
                    
                        <option value="80">Tỉnh Long An</option>
                    
                        <option value="82">Tỉnh Tiền Giang</option>
                    
                        <option value="83">Tỉnh Bến Tre</option>
                    
                        <option value="84">Tỉnh Trà Vinh</option>
                    
                        <option value="86">Tỉnh Vĩnh Long</option>
                    
                        <option value="87">Tỉnh Đồng Tháp</option>
                    
                        <option value="89">Tỉnh An Giang</option>
                    
                        <option value="91">Tỉnh Kiên Giang</option>
                    
                        <option value="92">Thành phố Cần Thơ</option>
                    
                        <option value="93">Tỉnh Hậu Giang</option>
                    
                        <option value="94">Tỉnh Sóc Trăng</option>
                    
                        <option value="95">Tỉnh Bạc Liêu</option>
                                                    
                        <option value="96">Tỉnh Cà Mau</option>
                    </select>
                </div>
                <div class="input-row">
                    <label class="input-lable">Giới tính</label>
                    <input v-model="user.ugender" type="radio" id="nam" name="gender" value="nam"><label>Nam</label>
                    <input v-model="user.ugender" type="radio" id="nu" name="gender" value="nu"><label>Nữ</label>
                    <input v-model="user.ugender" type="radio" id="another" name="gender" value="another"><label>Khác</label>
                </div>
                <div class="input-row">
                    <label class="input-lable">Chiều cao (cm)</label>
                    <input v-if="user.uheight || user.uheight==''" v-once v-model="user.uheight" v-bind:placeholder="user.uheight" type="number" name="height">
                </div>
                <div class="input-row">
                    <label class="input-lable">Sở thích</label>
                    <input v-if="user.uhobbies || user.uhobbies==''" v-once v-model="user.uhobbies" v-bind:placeholder="user.uhobbies" type="text" name="hobbies">
                </div>
                <div class="input-row">
                    <label class="input-lable">Số điện thoại</label>
                    <input v-if="user.uphonenumber || user.uphonenumber==''" v-once v-model="user.uphonenumber" v-bind:placeholder="user.uphonenumber" type="phone" name="phonenumber">
                </div>
                <div class="input-row">
                    <label class="input-lable">Hình đại diện</label>
                    <input v-on:change="handleImage" ref="fileImage" type="file" name="image" accept="image/png, image/jpeg" />
                </div>
                <div class="input-row">
                    <label class="input-lable">Năm sinh</label>
                    <input v-if="user.uage || user.uage==''" v-once v-model="user.uage" v-bind:placeholder="user.uage" type="date" name="age">
                </div>
            </div>
            <button class="btn-submit">Cập nhật</button>
        </form>
    </div>
    `,
    data: function() {
        return {
            user: {},
            image_update: null,
            errored: null,
            success: null,
            message: null,
            loading: null,
            select: "Thông tin tài khoản"
        }
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
                    this.$root.user['uimage'] = this.user.uimage
                    this.$root.user['ufullname'] = this.user.ufullname
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
}
var userLichSuTemplate = {
    delimiters: ["[[", "]]"],
    template: `
        <h1>abc</h1>
    `,
    data: function () {
        return {
            user: {}   
        }
    },
    created() {
        axios
            .get('http://localhost:8000/api/get_user_lichsu/')
            .then(response => {
                if(response.data.status){
                    this.user = response.data.user
                    this.$root.user['uimage'] = this.user.uimage
                    this.$root.user['ufullname'] = this.user.ufullname
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
        
    },
    methods:{
        click(){
            
        }
    }
}

new Vue({
    name:'userinfo',
    delimiters: ["[[", "]]"],
    el: '.content',
    data: {
        user: {
            'ufullname': null,
            'uimage': null
        },
        loadUserInfo: false,
        loadUserLichSu: false,
        select: "Thông tin tài khoản"
    },
    created() {
        if(localStorage.view == 'info')
            this.loadUserInfo = true
        else if (localStorage.view = 'lichsu')
            this.loadUserLichSu = true
    },
    methods: {
        loadPageInfo () {
            this.select = "Thông tin tài khoản"
            this.loadUserInfo = true
            this.loadUserLichSu = false
        },
        loadPageLichSu () {
            this.select = "Lịch sử ghép cặp"
            this.loadUserInfo = false
            this.loadUserLichSu = true
        },
    },
    components:{
        'user-info': userInfoTemplate,
        'user-lichsu': userLichSuTemplate
    }
})

