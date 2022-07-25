import {ref,shallowReactive, reactive, toRaw,type ShallowReactive} from "vue";

type LogType = {
    type:string,
    visible:boolean,
    name:string,
    args:any,
    kwargs:any,
    ret:any,
}

export class ViewState{
    logs:LogType[]

    constructor(){
        this.logs = shallowReactive([])

    }

    addLog(log:LogType){
        this.logs.push(log)
    }

    cleanLogs(){
        this.logs.splice(0,this.logs.length)
    }
}