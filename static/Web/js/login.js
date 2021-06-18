var username = JSON.parse(document.getElementById('username').textContent)
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        message: 'Hello ' + username + "!"
    }
})
