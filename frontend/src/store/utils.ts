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
    if (line.startsWith('@')){
        return line
    }else{
        return '@' + line
    }
}