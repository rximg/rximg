import { RXArg, RXFunction, createArgs } from "./RxLibrary";
import type { RXFunctionInterface, RXArgInterface } from "./RxLibrary";
import { ref, reactive, computed, watch, isProxy, toRaw, readonly, } from "vue"
import type { Ref, ComputedRef } from "vue"
import { unHatAt, hatAt,getUuid } from "./utils";
import md5 from 'md5'

//TODO ref系统需要开发了 不能用裸@了




type SubscribeValue = {
    value: string
    cast_value: string | number
    type: string
}

type Location = {
    x: number,
    y: number,
    readonly type: 'obserable'
    boxWidth: number,
    boxHeight: number
}


export class Observerable {
    name: string
    type: string
    from: string
    uuid: string
    pipes: Ref<string[]>
    subscribe: SubscribeValue
    upstream: RXFunctionInterface
    location: Location
    // inPorts: ComputedRef<InPort[]>

    // outPorts: ComputedRef<string[]>
    // isMultiCast: ComputedRef<boolean>

    constructor(upstream?: RXFunction) {

        this.name = "build_observerable"
        this.type = "Observerable"
        this.from = "core"
        // this.returnType = defined_data.returnType ? defined_data.returnType : 'Callable'
        this.uuid = <string>getUuid()
        if (upstream) {
            this.upstream = upstream
        } else {
            this.upstream = new RXFunction({})
        }
        // this.upstream.extraInPorts = reactive<Record<string, InPort>>({})
        this.pipes = ref([])
        this.subscribe = reactive<SubscribeValue>({ value: '', cast_value: "", type: 'SingleCast' })
        this.location = reactive<Location>({ x: 0, y: 0, type: 'obserable', boxWidth: 420, boxHeight: 240 })

    }

    fromjson(data: Record<string, any>, rxfunctions: Record<string, RXFunction>): void {
        this.type = data.type
        this.from = data.from
        this.uuid = <string>data.uuid
        this.name = data.name
        const upstreamuuid = unHatAt(<string>(data.args.head.value))
        if (rxfunctions[upstreamuuid]) {
            this.upstream = rxfunctions[upstreamuuid]
            // this.upstream.extraInPorts = reactive({})
        } else {
            throw new Error(`${upstreamuuid} not found`);
        }

        for (const tmp of data.args.pipe.value) {
            this.pipes.value.push(tmp)
        }
        let { type, value, cast_value } = data.args.subscribe
        if (type == 'SingleCast') {
            this.subscribe.type = type
            this.subscribe.cast_value = unHatAt(cast_value)
        } else {
            this.subscribe.type = type
            this.subscribe.cast_value = cast_value
        }
        if (data.location) {
            const { x, y, type, boxWidth, boxHeight } = data.location
            this.location.x = x
            this.location.y = y
            // this.location.type = type
            this.location.boxWidth = boxWidth ? boxWidth : 420
            this.location.boxHeight = boxHeight ? boxHeight : 240
        }
    }

    addUpStreamPort(name: string) {
        if (this.upstream.extraInPorts == undefined) {
            throw new Error(`upstream.extraInPorts at [${this.uuid},${this.upstream.uuid}] is undefined`)
        }
        if (this.upstream.extraInPorts[name] == undefined) {
            this.upstream.extraInPorts[name] = 0
        }
        if (this.upstream.args[name].type == 'list') {
            this.upstream.extraInPorts[name]++
        }
    }

    tojson(): any {
        //upstreamuuid 是否以@开头 以@开头赋值，不以@开头添加@
        let upstreamuuid_ = hatAt(<string>this.upstream.uuid)
        //TODO type和returnType需要梳理
        let subscribevalue: string | number = ""
        if (this.subscribe.type == 'SingleCast') {
            subscribevalue = hatAt(this.subscribe.cast_value)
        } else {
            subscribevalue = `@core.get_subject('${this.uuid}')`
        }
        let json = {
            type: this.type,
            from: this.from,
            uuid: this.uuid,
            name: this.name,
            op: this.op,
            returnType: this.returnType,
            location: this.location,
            args: {
                "head": {
                    value: upstreamuuid_
                },
                "pipe": {
                    type: 'list',
                    value: this.pipes.value
                },
                "subscribe": {
                    type: this.subscribe.type,
                    value: subscribevalue,
                    cast_value: this.subscribe.cast_value
                }

            }
        }
        return json
    }

    swapSubscribeType(): void {
        //判断this.subscribe类型是否是SingleCast
        console.log('swap subscribe', this.subscribe, this.subscribe.type, this.subscribe.cast_value)
        if (this.subscribe.type == 'SingleCast') {
            this.subscribe.type = 'MultiCast'
            this.subscribe.cast_value = 0
        } else {
            this.subscribe.type = 'SingleCast'
            this.subscribe.cast_value = ""
        }

    }
    incrementMulticast(): void {
        if (this.subscribe.type == 'MultiCast') {
            if (typeof this.subscribe.cast_value == 'number') {
                this.subscribe.cast_value = this.subscribe.cast_value + 1
            }
        } else {
            throw new Error(`Type error. ${this.subscribe.type}`);
        }
    }
    decrementMulticast(): void {
        if (this.subscribe.type == 'MultiCast') {
            //TODO check inports
            if (typeof this.subscribe.cast_value == 'number') {
                this.subscribe.cast_value = this.subscribe.cast_value + 1
            }
        } else {
            throw new Error(`Type error. ${this.subscribe.type}`);
        }
    }

    setSubscribe(value: string): void {
        console.log('setSubscribe', value, this.subscribe, this.subscribe.type)
        if (this.subscribe.type == 'SingleCast') {
            this.subscribe.cast_value = hatAt(value)
            // console.log('setSubscribe', value, this.subscribe, this.subscribe.type, this.subscribe.value)
        } else {
            throw new Error(`Type error. ${this.subscribe.type}`);
        }
    }
    addPipe(uuid: string): void {
        this.pipes.value.push(hatAt(uuid))
    }
    removePipe(index: number): void {
        this.pipes.value.splice(index, 1)
    }
    swapPipe(oldIndex: number, newIndex: number): void {
        //在array中交换oldIndex和newIndex的位置
        let temp = this.pipes.value[oldIndex]
        this.pipes.value[oldIndex] = this.pipes.value[newIndex]
        this.pipes.value[newIndex] = temp

    }


    // md5(): string {
    //     return super.md5()
    // }

    // toString(): string {
    //     return super.toString()
    // }

}


