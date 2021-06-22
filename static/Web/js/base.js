new Vue({
    name:'home',
    delimiters: ["[[", "]]"],
    el: '.header',
    methods: {
        loadPageInfo () {
            localStorage.view = 'info'
            window.location.href = "http://localhost:8000/user_info"
        },
        loadPageLichSu () {
            localStorage.view = 'lichsu'
            window.location.href = "http://localhost:8000/user_info"
        },
    }
})