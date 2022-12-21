var screen;
var imageUrl;
function convert_coordinate(x, y){
    console.log(x,y)
    x = x/document.body.clientWidth  * 1920;
    y = y/document.body.clientHeight * 1080;
//    console.log()
    return {x:x,y:y}
}

var regex = /.*csrftoken=([^;.]*).*$/ ;
var xCSRFToken = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]

//request
function refresh(){
/*     var x = 0;
    var y = 0;
    var data = {x,y,click = False}; */
    var xhr = new XMLHttpRequest();
    xhr.open('POST', document.URL + 'server_connected')
    xhr.responseType = "blob";
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", xCSRFToken)
    xhr.onload = update_img
    xhr.send(null)
/*     $.ajax({type:'GET', url: document.URL + 'server_connected', data: data, success: update_img}) ajax quan jia bao bi
 */} 
//respond 
function update_img(){
    var blob = this.response;
//    console.log(imageUrl)
    if(imageUrl != null){window.URL.revokeObjectURL(imageUrl)}
//    console.log(imageUrl)

    imageUrl = (window.URL || window.webkitURL).createObjectURL(blob);
//    screen.style.backgroundImage = imageUrl;
//    document.body.appendChild(screen);
    $(document.body).css("background-image","url("+imageUrl+")")
//    console.log(imageUrl)
}
function load_server(){
//    screen = document.createElement('img')
//    screen.classList.add('screen');
    document.body.onclick = click_event
//    document.body.appendChild(screen)
    refresh()
    setInterval(refresh,3000);
}

function click_event(event){
    var cordinates = convert_coordinate(event.clientX , event.clientY)
    var Http = new XMLHttpRequest();
    var url=document.URL+'server_click' + '/'  +
        String(Math.round(cordinates.x)) + '/' + String(Math.round(cordinates.y));
//    console.log(url)
    Http.open("GET", url);
    Http.send();
}