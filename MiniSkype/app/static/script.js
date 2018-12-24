
var data;
var session_id;

var username;
var password;
var email;
var session_id;
var roomID;

var audienceUsername = document.getElementById('calleeUsername').value;
var caller;



function login(){

    username = document.getElementById('username').value;
    password = document.getElementById('password').value;

    var ajax_post= function(url, callback) {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                    var data = JSON.parse(xmlhttp.responseText);
                    callback(data); }
        };
 
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ "username": username, "password": password}));
    };
 
    ajax_post('api/login', function(data) {
        
        document.getElementById('login').innerHTML = data['status']+' '+ data['message'];
        session_id = data['session_id']
        
    });

}



function signin(){

    username = document.getElementById('username0').value;
    password = document.getElementById('password0').value;
    email = document.getElementById('email0').value;

    var ajax_post = function(url, callback) {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                    var data = JSON.parse(xmlhttp.responseText);
                    callback(data); }
        };
 
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ "username": username, "password": password, 'email':email}));
    };
 
    ajax_post('api/signin', function(data) {
        
        document.getElementById('signin').innerHTML = data['status']+' '+ data['message'];
        session_id = data['session_id']
        
    });

}







function createRoom(){

        calleeUsername = document.getElementById('calleeUsername').value;

        var ajax_post = function(url, callback) {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                    var data = JSON.parse(xmlhttp.responseText);
               
                callback(data);
            }
        };
 
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ "calleeUsername": calleeUsername, "session_id": session_id}));
    };
 
    ajax_post('api/createRoom', function(data) {
        
        document.getElementById('createRoom').innerHTML = data['status']+' '+ data['message']+ " and yor roomID is "+data['roomID'];
        roomID = data['roomID']
        
    });
    
}






function join(){

        var caller2 = document.getElementById('caller').getAttribute('value');
        var ajax_get = function(url, callback) {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                    var data = JSON.parse(xmlhttp.responseText);
               
                callback(data);
            }
        };
 
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ "session_id": session_id, "callerUsername": caller}));
    };
 
    ajax_get('api/join', function(data) {
        
        document.getElementById('info2').innerHTML = JSON.stringify(data, null, '   ');
        var chatRoomID = data['chatRoomID']
        
    });
    
}
