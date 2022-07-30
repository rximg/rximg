export function unHatAt(line:string):any{
    if (typeof line!='string'){
        return line
    }
    if (line.startsWith('@')){
        return line.substring(1)
    }else{
        return line
    }
}

export function hatAt(line:string){
    if (typeof line!='string'){
        return line
    }
    if (line==""){
        return line
    }
    if (line.startsWith('@')){
        return line
    }else{
        return '@' + line
    }
}

export function getUuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (Math.random() * 16) | 0,
            v = c == 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}