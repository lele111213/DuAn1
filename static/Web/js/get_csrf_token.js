// (function set_cookie(){
//     var xhr = new XMLHttpRequest();
//     var url = 'http://localhost:8000/get_csrf_token/';
//     xhr.open('GET', url , true);
//     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//     xhr.onreadystatechange = function() {
//         if (this.status == 200 && this.readyState == 4){
//             data = JSON.parse(this.response);
//             console.log(data);
//         }
//     }
//     xhr.send();
// })()