var elems, eLen, i;
elems = document.getElementsByClassName("graphEdge")
eLen = elems.length;

function closeOverlay(event){
    relOver = document.getElementById("RelationshipOverlay");
    relUnder = document.getElementById("RelationshipUnderlay");
    relUnder.style.visibility='hidden';
    relOver.style.visibility='hidden';
}

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", function(event){
		event.preventDefault();
		relOver = document.getElementById("RelationshipOverlay");
        relUnder = document.getElementById("RelationshipUnderlay");
        relOver.innerHTML = '<div style="width:100%; height:5%;"><span style="position: absolute; cursor: pointer; right:0px; color: red; font-family: sans-serif; font-size:2em;" onclick="closeOverlay()">X</span></div><object type="text/html" style="width:100%; height:95%" data="'+this.href+'"></object>';
        relUnder.style.visibility='visible';
		relOver.style.visibility='visible';
    });
}
document.getElementById("RelationshipUnderlay").addEventListener("click", closeOverlay);

var elems, eLen, i;
elems = document.getElementsByClassName("showRels")
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", function(event){
        event.preventDefault();
        document.getElementById("relationship").setAttribute('data', event.currentTarget.href);
    });
}