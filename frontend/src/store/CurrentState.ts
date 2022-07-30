import type { RXFunction } from "./RxLibrary";
import { ref,shallowReactive,shallowRef,reactive, type ShallowRef, type ShallowReactive } from "vue";
import type {Ref} from "vue"
type Edge ={
    cell:string,
    port:string
}
type Port={
    source:Edge,
    target:Edge
}
type Config = {
    names:string[],
    current:string,
}
export class CurrentState {
    function_data:Ref<RXFunction|any>
    main_menu:Ref<string[]>
    edges:ShallowReactive<Record<string,Port>>
    apiurl:string
    global_datarefresh:Ref<number>
    config:Config

    constructor() {
        this.function_data = shallowRef({})
        this.main_menu = ref(['library'])
        this.edges = shallowReactive({})
        this.apiurl = ""
        this.global_datarefresh = ref(0)
        this.config = reactive<Config>({names:[],current:''})
    }
    setFunction(function_data:RXFunction){
        this.function_data.value = function_data
    }
    setMainMenu(main_menu:string[]){
        this.main_menu.value = main_menu
    }
    cleanFunction(){
        this.function_data.value = {}
    }

    getNdarrayUrl(ndarray_uuid:string){
        return this.apiurl + "/ndarray/" + ndarray_uuid;
    }
    deleteEdgeByCell(cell:string){
        for (const key in this.edges){
            if (this.edges[key].source.cell == cell || this.edges[key].target.cell == cell){
                delete this.edges[key]
            }
        }
    }
    updateConfigNames(data:Config){
        this.config.current = data.current
        data.names.forEach(
            (value)=>{
                this.config.names.push(value)
            }
        )
    }
}