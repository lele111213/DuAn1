var user_name = JSON.parse(document.getElementById('username').textContent)
var rightNav = new Vue({
    delimiters: ["[[", "]]"],
    el: '.right-nav',
    data: {
        username: user_name ? user_name : "",
        logged: user_name ? true : false
    }
})