var showEvent = new Event('show');

function textClicked(event){
    me = event.currentTarget;
    sibs = me.parentNode.childNodes;
    sibLen = sibs.length;
    iFSib = 0;
    for (j=0; j<sibLen; j++){
        if(sibs[j].className===me.className+'Field'){
            iFSib = sibs[j];
            break;
        }
    }
    if(iFSib!=0){
        iFSib.style.width=me.offsetWidth+'px';
        me.style.display='none';
        iFSib.style.display='inline';
        iFSib.focus();
    }
}

function boxFilled(event){
    me = event.currentTarget;
    if(event.keyCode === 13){
        sibs = me.parentNode.childNodes;
        sibLen = sibs.length;
        iSib = 0;
        for (j=0; j<sibLen; j++){
            if(sibs[j].className===me.className.slice(0, -5)){
                iSib = sibs[j];
                break;
            }
        }
        if(iSib!=0){
            me.style.display='none';
            if(parseFloat(me.value)>1.0){
                me.value = '1.0';
            } else if(me.className==='relValField' && parseFloat(me.value)<-1.0){
                me.value = '-1.0';
            } else if(me.className==='importanceField' && parseFloat(me.value)<0){
                me.value = '0.0';
            }
            iSib.innerHTML=me.value;
            iSib.style.display='inline';
            me.dataset['value'] = me.value;
            var xhttp = new XMLHttpRequest();
            xhttp.open("get", '/cgi-bin/setRel.py?src='+me.dataset['src']+'&dest='+me.dataset['dest']+'&rel='+me.dataset['rel']+'&'+me.className.slice(0, -5)+'='+me.value);
            xhttp.send();
            console.log('/cgi-bin/setRel.py?src='+me.dataset['src']+'&dest='+me.dataset['dest']+'&rel='+me.dataset['rel']+'&'+me.className.slice(0, -5)+'='+me.value);
        }
    }
}

function boxLeft(event){
    me = event.currentTarget;
    sibs = me.parentNode.childNodes;
    sibLen = sibs.length;
    iSib = 0;
    for (j=0; j<sibLen; j++){
        //console.log(me.className.slice(0, -5))
        if(sibs[j].className===me.className.slice(0, -5)){
            iSib = sibs[j];
            break;
        }
    }
    if(iSib!=0){
        me.style.display='none';
        iSib.style.display='inline';
        me.value = me.dataset['value'];
    }
}

function showSibs(event){
    me = event.currentTarget;
    sibs = me.parentNode.childNodes;
    sibLen = sibs.length;
    iSib = 0;
    for (j=0; j<sibLen; j++){
        //console.log(me.className.slice(0, -5))
        if(sibs[j].tagName==='UL'){
            iSib = sibs[j];
            break;
        }
    }
    if(iSib!=0){
        iSib.dispatchEvent(showEvent);
    }
}

function showList(event){
    me = event.currentTarget;
    me.dataset['vis']=1-me.dataset['vis'];
    children = me.childNodes;
    childLen = children.length;
    for(j=0; j<childLen; j++){
        if (children[j].dataset['vis']=='visible'){
            if(me.dataset['vis']==1){
                children[j].style.display='list-item';
            } else {
                children[j].style.display='none';
            }
        }
    }
}

/*var elems, eLen, i;
elems = document.getElementsByClassName("importance")
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", textClicked);
}

elems = document.getElementsByClassName("importanceField")
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("keyup", boxFilled);
    elems[i].addEventListener("focusout", boxLeft);
}

elems = document.getElementsByClassName("relVal")
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", textClicked);
}

elems = document.getElementsByClassName("relValField")
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("keyup", boxFilled);
    elems[i].addEventListener("focusout", boxLeft);
}*/

elems = document.getElementsByClassName("relView");
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", showSibs);
    me = elems[i];
    sibs = me.parentNode.childNodes;
    sibLen = sibs.length;
    iSib = 0;
    for (j=0; j<sibLen; j++){
        if(sibs[j].tagName==='UL'){
            iSib = sibs[j];
            break;
        }
    }
    if(iSib!=0){
        iSib.addEventListener('show', showList);
    }
}

elems = document.getElementsByClassName("roleView");
eLen = elems.length;

for (i=0; i<eLen; i++){
    elems[i].addEventListener("click", showSibs);
    me = elems[i];
    sibs = me.parentNode.childNodes;
    sibLen = sibs.length;
    iSib = 0;
    for (j=0; j<sibLen; j++){
        if(sibs[j].tagName==='UL'){
            iSib = sibs[j];
            break;
        }
    }
    if(iSib!=0){
        iSib.addEventListener('show', showList);
    }
}
