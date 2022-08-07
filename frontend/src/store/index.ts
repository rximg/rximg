import axios from 'axios'
import { reactive,computed, ref, toRaw, shallowRef, shallowReactive } from 'vue'
import type { Ref, ShallowReactive } from "vue"
import { RXFunction,LambdaFunction } from './RxLibrary'
import { Observerable } from './Observers'
import _ from 'lodash'
import { CurrentState } from './CurrentState'
import { ViewState } from './View'
import { useLocalStorage } from '@vueuse/core'

export const libraryStore: Record<string, any> = shallowRef({})

export const RXFunctionsStore: ShallowReactive<Record<string, RXFunction>> = shallowReactive({})

export const ObserverablesStore: ShallowReactive<Record<string, Observerable>> = shallowReactive({})

export const CurrentStateStore: CurrentState = new CurrentState()

export const ViewStore: ViewState = new ViewState()


export const localStorage = useLocalStorage('current', { taskName: 'undefined'})

export const initStore = async () => {

    let response = await axios.get('api/elements')
    // console.log('response library',response.data)
    libraryStore.value = response.data
    // response = await axios.get('api/config')

    response = await axios.get(`api/observers/${localStorage.value.taskName}`)
    // console.log('response:',localStorage.value.taskName,response.data,response.data.observers,response.data.relations)
    Object.values(response.data.observers).forEach(
        (item) => {
            if (item.type=='lambda'){
                RXFunctionsStore[item.uuid] = new LambdaFunction(item)
            }else{
                
                RXFunctionsStore[<string>item.uuid] = new RXFunction(<Record<string, any>>item)
            }
            // rxfunc.fromjson()
        }
    )
    Object.values(response.data.relations).forEach(
        (item) => {
            let observerable = new Observerable()
            observerable.fromjson(<Record<string, any>>item, toRaw(RXFunctionsStore))
            ObserverablesStore[item.uuid] = observerable
        }
    )
    CurrentStateStore.edges = reactive(response.data.edges)
    CurrentStateStore.global_datarefresh.value += 1
    // console.log(localStorage,localStorage.value.taskName)
    response = await axios.get('api/config')
    CurrentStateStore.updateTaskNames(response.data.names)
    // ObserverablesStore.value = response.data
    return true

}

// export const reloadStore = async (name:string)=>{
//     let response = await axios.put(`api/config/${name}`)
//     Object.keys(RXFunctionsStore).forEach(key => RXFunctionsStore[key] = undefined);
//     Object.keys(RXFunctionsStore).forEach(key => ObserverablesStore[key] = undefined);
//     await initStore()
// }

export const persistStoreFunc = async () => {
    const observer_data = {}
    let temp: any
    const observer_raw = toRaw(ObserverablesStore)
    const rxfunction_raw = toRaw(RXFunctionsStore)
    console.log("persist", observer_raw, rxfunction_raw)
    for (const k in observer_raw) {
        if (observer_raw) {
            // console.log('to json', observer_raw[k].tojson())
            observer_data[k] = observer_raw[k].tojson()
        }
    }
    const rx_data = {}

    for (const k in rxfunction_raw) {
        // temp = rxfunction_raw
        if (rxfunction_raw) {
            // console.log('to json', rxfunction_raw[k].tojson())
            rx_data[k] = rxfunction_raw[k].tojson()
        }
    }
    const edges ={}
    for (const edgek in CurrentStateStore.edges) {
        edges[edgek] = CurrentStateStore.edges[edgek]
    }
    await axios.post(`api/observers/${localStorage.value.taskName}`, {
        observers: rx_data,
        relations: observer_data,
        parameters: {},
        edges: edges
    })
}

export const persistStore = _.throttle(persistStoreFunc, 500)


// export const addMulticast = (item:Observerable,)=>{
//     item.addMulticast()
// }


// export function useGraph(): {
//     const x = 10
//     let y = 10
//     const stride = 300
//     console.log('get_graph', ObserverablesStore,toRaw(ObserverablesStore),ObserverablesStore['@fa6e5b9a878d810d288ac9ed3cb817a5'])

//     // const nodes:Record<string,unknown>=shallowReactive({})
//     // const computed_nodes = computed(
//     //     () => {
//     //         // const nodes = shallowReactive({})
//     //         for (const key in ObserverablesStore) {
//     //             console.log('key', key)
//     //             ObserverablesStore[key] = {
//     //                 type: 'obserable',
//     //                 x: x,
//     //                 y: y,
//     //             }
//     //             // x+=stride
//     //             y += stride
//     //         }
//     //         return nodes
//     //     }

//     // )

//     return { nodes: ObserverablesStore, edges: [] }
// }