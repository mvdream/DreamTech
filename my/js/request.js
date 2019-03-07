function slot(){
var url="slot.php";
if(window.XMLHttpRequest){
request=new XMLHttpRequest();
}
else if(window.ActiveXObject){
request=new ActiveXObject("Microsoft.XMLHTTP");
}
try
{
request.open("GET",url,true);
request.send();
}
catch(e)
{
alert("Unable to connect to server");
}
}
