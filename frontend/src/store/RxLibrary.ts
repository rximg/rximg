/*eslint prefer-const: 2*/
import { isProxy, reactive, ref } from "vue"
import type { Ref, ComputedRef } from "vue"
import {getUuid} from "./utils"
// import { array, number } from "vue-types"
import md5 from 'md5'
export type CommonValueType = string | number | string[] | boolean | null
export type RefCommonValueType = Ref<CommonValueType>//Ref<string> | Ref<number> | Ref<string[]> | Ref<boolean> | Ref<null>
// 引用类型string_type_ref
// type InPort = {
//     port_id: string,
//     port_name: string,
//     index: number,
// }
/**
 * value有这么些情况
 * type=[str,int,float,bool,ref,list] value有default或者没有default。
 * type=[types] value=undefined 表示这是个多输入的函数。
 * type=[types] value=变量 
 */
export interface RXArgInterface {
    index: number
    kind?: string
    type: string
    value: RefCommonValueType
    name?: string
    mutable?: string|boolean
    toString(): string
    tojson(): any//stringify
    md5(): string
    // fromjson(data:Record<string,any>):void

}
// library => function
// json => recover function 

export interface ChoiceArgInterface extends RXArgInterface {
    choices: Record<string, number | string>
}
// function init_value_by_type(type: string,): RefCommonValueType {
//     let value: any
//     switch (type) {
//         case 'bool':
//             value = false
//             break;
//         case 'int':
//             value = 0
//             break;
//         case 'float':
//             value = 0.0
//             break;
//         case 'tuple':
//             value = [0, 0]
//             break;
//         case 'list':
//             value = []
//             break;
//         case 'str':
//             value = ''
//             break;
//         case 'ref':
//             value = ""
//             break;
//         default:
//             value = null
//             break;
//     }

//     return ref(value)
// }
export class RXArg implements RXArgInterface {
    index: number
    kind?: string
    readonly type: string
    name?: string
    mutable?: string|boolean
    // extraInPorts?:Ref<InPort[]>
    value: RefCommonValueType

    constructor(index: number, type: string, kind?: string, value?: CommonValueType, name?: string, mutable?: string) {
        this.index = index
        this.type = type
        if (kind) {
            this.kind = kind
        }
        if (value == undefined) {
            this.value = ref(undefined)

        }
        // else if (typeof (value) == 'string' && value == 'None') {
        //     this.value = ref(undefined)
        // }
        else {
            // this.value = init_value_by_type(type)
            this.value = ref(value)
        }
        this.name = name ? name : undefined
        this.mutable = mutable ? mutable : undefined

    }



    toString(): string {
        const isplaceholder = this.value == undefined || this.value.value == undefined
        if (isplaceholder) {
            return '#'
        }
        if (this.type in ['bool', 'int', 'float', 'tuple']) {
            return `${this.value.value}`
        } else if (this.type == 'list') {
            return `list-${(<string[]>this.value.value).length}`

        }
        else {
            return `${this.value.value}`
        }
    }

    tojson() {
        // const value = this.value.value == undefined ? 'None' : this.value.value

        return {
            name:this.name,
            index: this.index,
            kind: this.kind,
            type: this.type,
            value: this.value.value,
            mutable:this.mutable?this.mutable:undefined,
            // extraInPorts:this.extraInPorts?.value
        }
    }

    md5(): string {
        return md5(`${this.type}${this.value.value}${this.mutable}`)
    }
}

export class ChoiceArg implements ChoiceArgInterface {
    index: number
    kind?: string
    type: string
    name?: string
    value: RefCommonValueType
    choices: Record<string, number | string>
    mutable?: string|boolean



    constructor(index: number,
        choices: Record<string, number | string>,
        kind?: string,
        value?: CommonValueType,
        name?: string,
        mutable?: string|boolean
    ) {
        this.index = index
        this.type = "choices"
        if (kind) {
            this.kind = kind
        }
        if (value) {
            this.value = ref(value)
        } else {
            this.value = ref(0)
        }
        this.name = name ? name : undefined
        this.choices = choices
        this.mutable = mutable ? mutable : undefined
    }



    toString(): string {
        for (const key in this.choices) {
            if (this.value.value == this.choices[key]) {
                return `${key}`
            }
        }
        return "default"
    }
    tojson() {
        return {
            name:this.name,
            index: this.index,
            kind: this.kind,
            type: this.type,
            value: this.value.value,
            mutable:this.mutable?this.mutable:undefined
        }
    }
    md5(): string {
        return md5(`${this.type}${this.value.value}`)
    }


}

export interface RXFunctionInterface {
    uuid: string | ComputedRef<string>
    args: Record<string, RXArg>
    op: string
    name: string
    type: string
    from: string
    returnType?: string
    extraInPorts?: Record<string, number>
    toString(): string
    tojson(): any//stringify
    md5(): string
    onSubmit():void
    // createArgs(data: any):RXArgInterface
    // fromjson(data:Record<string,unknown>):void
}

// interface LambdaInterface extends RXFunctionInterface{
// line:string
// constructor(argvalue: string[],line: string)
// }

export const createArgs = (data: Record<string, any>): RXArgInterface => {
    const { index, type, kind, value, name ,mutable} = data
    if (data.type == 'choices') {
        return new ChoiceArg(index, data.choices, kind, value, name,mutable)
    } else {
        return new RXArg(index, type, kind, value, name,mutable)
    }
}

export class RXFunction implements RXFunctionInterface {
    uuid: string | ComputedRef<string>
    args: Record<string, RXArg>
    op: string
    name: string
    type: string
    from: string
    extraInPorts?: Record<string, number>
    returnType: string
    
    // constructor(data:Record<string,any>)
    // constructor(args:Record<string,RXArg>,op:string,name:string,type:string,)
    // 1、由defined_data 生成。
    // 2、由json 生成。
    constructor(defined_data: Record<string, any>) {
        this.args = {}
        for (const key in defined_data.args) {
            // console.log('show arg data',defined_data.args,defined_data.args[key])

            const arg = createArgs(defined_data.args[key])
            // console.log('arg',arg,arg.toString())
            this.args[key] = arg
            // this.args[key].name = key
        }
        this.op = defined_data.op
        this.name = defined_data.name
        this.type = defined_data.type
        this.from = defined_data.from
        this.returnType = defined_data.returnType ? defined_data.returnType : 'Callable'
        if (defined_data.uuid) {
            this.uuid = defined_data.uuid
        } else {
            this.uuid = md5(this.toString())
        }
        // console.log('extraInPorts',defined_data.extraInPorts)
        if (defined_data.extraInPorts) {
            this.extraInPorts = reactive(defined_data.extraInPorts)
        } else {
            this.extraInPorts = reactive({})
        }
    }

    // fromjson(data:Record<string,any>){
    //     console.log('from json',data)
    //     this.uuid = data.uuid
    //     // this.args = {}
    //     if (this.args){
    //         for (const key in data.args){
    //             console.log(this.args[key],key)
    //             this.args[key].fromjson(data.args[key])

    //         }
    //     }
    //     this.op = data.op
    //     this.name = data.name
    //     this.type = data.type
    //     this.from = data.from
    //     this.returnType = data.returnType ? data.returnType : 'Callable'
    // }

    toString(): string {
        let argstr = ""
        for (const key in this.args) {
            argstr = argstr + `${key}=${this.args[key].toString()},`
        }
        let tempop = ""
        if (this.op) {
            tempop = `${this.op}:`
        }
        return `${tempop}${this.name}(${argstr})`
    }
    tojson() {
        const argsjson = {}
        for (const k in this.args) {
            argsjson[k] = this.args[k].tojson()
        }
        return {
            type: this.type,
            from: this.from,
            uuid: this.uuid,
            name: this.name,
            // output: outputIndexs,
            op: this.op,
            returnType: this.returnType,
            // func_name:
            //return_view: funcData.return_view,
            args: argsjson,
            extraInPorts: this.extraInPorts ? this.extraInPorts : undefined
        }
    }
    md5(): string {

        let argstr = ""
        for (const key in this.args) {
            argstr = argstr + `${key}=${this.args[key].md5()},`
        }
        let tempop = ""
        if (this.op) {
            tempop = `${this.op}:`
        }
        return md5(`${tempop}${this.name}(${argstr})`)
    }

    onSubmit(): void {
        for (const key in this.args) {
            if (this.args[key].mutable==true){
                this.args[key].mutable=getUuid()
            }
        }
        this.uuid = this.md5()
    }

}



export class LambdaFunction extends RXFunction {



    constructor(defined_data: Record<string, any>) {
        super(defined_data)
    }

    toString(): string {
        let args = ""
        const arg_value = this.args.args.value.value
        // console.log('args', arg_value)
        for (const i in arg_value) {
            args = args + ',' + arg_value[i]
        }
        let tempop = ""
        if (this.op) {
            tempop = `${this.op}:`
        }
        return `${tempop}λ(${args})=>${this.args.line.value.value}`
    }

    md5(): string {
        return md5(<string>this.args.line.value.value)
    }

}
