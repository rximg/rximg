function getDefatulByType(type) {
    if (type=='bool'){
        return true
    }else if(type=='int'){
        return 0
    }else if(type=='float'){
        return 0.0
    }else {
        return ""
    }
} 

function isString(s){
    return Object.prototype.toString.call(s).slice(8, -1)=="String"
}

function isEmputy(value) {
    var type;
    if(value == null) { 
        return true;
    }
    type = Object.prototype.toString.call(value).slice(8, -1);
    switch(type) {

    case 'Array':
        return !value.length;
    case 'Object':
        return Object.keys(value).length==0;
    default:
        return false; 
    }
}

function sortObj(obj){
    return Object.values(obj).sort((a,b)=>a.index-b.index)
  }

export {getDefatulByType, isEmputy,isString,sortObj};