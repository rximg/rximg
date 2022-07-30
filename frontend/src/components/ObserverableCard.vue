<template>
  <a-card class="card" :ref="(el) => { currentDom = el }" style="width: 100%"
    :headStyle="getHeadStyle(ObservableItem.uuid)">
    <template #extra href="#">
      <a-button-group>
        <a-dropdown>
          <template #overlay>
            <a-menu @click="ObservableItem.addUpStreamPort($event.key)">
              <a-menu-item v-for="portname in inPortKeys" :key="portname">
                <right-square-outlined />{{ portname }}
              </a-menu-item>
            </a-menu>
          </template>

          <a-button >
            UpStream
            <plus-circle-outlined />
          </a-button>
        </a-dropdown>
        <a-dropdown>
          <template #overlay>
            <a-menu @click="ObservableItem.addPipe(onlyCallables[$event.key].uuid)">
              <a-menu-item v-for="(callable_item, pipe_index) in onlyCallables" :key="pipe_index">
                <right-square-outlined />{{ callable_item.toString() }}
              </a-menu-item>
            </a-menu>
          </template>

          <a-button>
            Pipe
            <plus-circle-outlined />
          </a-button>
        </a-dropdown>
        <a-dropdown>
          <template #overlay>
            <a-menu>
              <template v-if="ObservableItem.subscribe.type == 'MultiCast'">
                <a-menu-item @click="() => ObservableItem.swapSubscribeType()">
                  <swap-outlined /> SingleCast
                </a-menu-item>
                <a-menu-item @click="ObservableItem.incrementMulticast()">
                  <plus-square-outlined />ReplaySubject
                </a-menu-item>
                <a-menu-item @click="ObservableItem.decrementMulticast()">
                  <minus-square-outlined  />ReplaySubject
                </a-menu-item>
              </template>
              <template v-else>
                <a-menu-item @click="() => ObservableItem.swapSubscribeType()">
                  <swap-outlined /> MultiCast
                </a-menu-item>
                <a-menu-item @click="ObservableItem.setSubscribe('')">
                  <reload-outlined /> clean
                </a-menu-item>
                <a-menu-item v-for="(callable_item, nobkindex) in onlyCallables" :key="nobkindex"
                  :value="callable_item.uuid" @click="ObservableItem.setSubscribe(callable_item.uuid)">
                  <plus-outlined />{{ callable_item.toString() }}
                </a-menu-item>
              </template>
            </a-menu>
          </template>
          <a-button> Subscribe
            <plus-circle-outlined />
          </a-button>
        </a-dropdown>
        <a-button @click.once="deleteObserverable(ObservableItem.uuid)">
          <delete-outlined />
        </a-button>
      </a-button-group>
    </template>
    <div>
      <a-tag  :color="getColorByHex(ObservableItem.upstream.uuid)">
        <div style="word-break: break-all;word-wrap: break-word">
          {{ ObservableItem.upstream }}
        </div>
      </a-tag>
    </div>

    <div>
      <span v-if="!(ObservableItem.pipes.value.length == 0)">
        <draggable v-model="ObservableItem.pipes.value" group="people" @start="startDrag($event)" @end="endDrag($event)">
          <template #item="{ element, index }">
            <a-tag   class="argitems" :visible="true" closable @close="ObservableItem.removePipe(index)">
                {{ refTarget(element).toString() }}
            </a-tag>
          </template>
        </draggable>
      </span>
      <span v-else>
        <a-tag>...</a-tag>
      </span>
    </div>
    <div v-if="ObservableItem.subscribe.cast_value">
      <div v-if="ObservableItem.subscribe.type == 'SingleCast'">
        <a-tag color="#108ee9">
          {{ refTarget(ObservableItem.subscribe.cast_value as string).toString() }}
        </a-tag>
      </div>
      <!-- <div v-else-if="ObservableItem.subscribe.type == 'MultiCast'">
        <span v-for="(subindex, sublistindex) in ObservableItem.subscribe.cast_value" :key="sublistindex">
          <a-tag :color="getColorByHex(ObservableItem.uuid + '_' + subindex.toString())">
            <a-icon type="environment" /> {{ subindex }}
          </a-tag>
        </span>
      </div> -->
    </div>
    <div class="itemUuid">{{ ObservableItem.uuid }}</div>
  </a-card>
</template>



<script setup lang="ts">

import { computed, ref, watch, onMounted,toRef } from 'vue'
import { RXFunctionsStore, ObserverablesStore, persistStore,CurrentStateStore } from '@/store';
// import { isString } from '../store/utils.js'
import type { Observerable } from '@/store/Observers';
// import type {Observerable} from "@/types/Observers"
import { getColorByHex } from "@/components/toolbox/color.js";
import { useElementSize } from '@vueuse/core'
// import BriefTag from "./stateless/BriefTag.vue";
import draggable from "vuedraggable";
import {
  DeleteOutlined,
  PlusCircleOutlined,
  SwapOutlined,
  ReloadOutlined,
  PlusOutlined,
  RightSquareOutlined,
  MinusSquareOutlined,
  PlusSquareOutlined
} from "@ant-design/icons-vue";
import type { RXFunctionInterface } from '@/store/RxLibrary';
import { unHatAt } from '@/store/utils';

type Props = {
  ObservableItem: Observerable
}


const { ObservableItem } = defineProps<Props>()
const drag = ref(false)
let currentDom = ref<HTMLInputElement | null>(null)
const { width, height } = useElementSize(currentDom)
ObservableItem.location.boxHeight = height
onMounted(
  () => {
    // console.log('client height',observerableCardDom,observerableCardDom.value,observerableCardDom.value.clientHeight)
    // if (currentDom.value) {
      // const { width, height } = useElementSize(currentDom)
      // const height = <number>currentDom.value?.clientHeight
      // ObservableItem.location.boxHeight = height ? height : 240
    // }
  }
)
// const headTools = {
//   background: "#348498",
//   color: "white",
//   "font-size": "medium",
// }
// const headHead = {
//   background: "#8bc6af",
//   color: "white",
//   "font-size": "medium",
// }
// const headSubscribe = {
//   background: "#FFC329",
//   color: "white",
//   "font-size": "medium",
// }
// const ObservableItem = ObserverablesStore[uuid]

const getHeadStyle = (uuid: string) => {
  var color = getColorByHex(uuid);
  return {
    background: color,
    color: "white",
  };
}
const refTarget=(uuid:string):RXFunctionInterface=>{
  return RXFunctionsStore[unHatAt(uuid)]
}

const onlyCallables = computed(() => {
  return Object.values(RXFunctionsStore).filter(item => {
    return item.returnType != 'Observable'
  })
})
const deleteObserverable = (uuid: string) => {
  CurrentStateStore.deleteEdgeByCell(uuid)
  delete ObserverablesStore[uuid]
}

const startDrag=(e)=>{
  drag.value = true
}
const endDrag = (e) => {
  console.log('drag',e)
  drag.value = false;
  ObservableItem.swapPipe(e.oldIndex, e.newIndex)
}
const inPortKeys = computed(
  () => {
    const keys = []
      for (const key in ObservableItem.upstream.args){
        if (ObservableItem.upstream.args[key].type='list'){
          keys.push(key)
        }
      }
    return keys
  }
)
// const addUpStreamPort = (name: string) => {
//   if (ObservableItem.inPorts[name].length == 0) {
//     ObservableItem.inPorts[name].push({ port_id: `${ObservableItem.uuid}_0`, port_name: `${name}_0`, index: 0 })
//   } else {
//     const maxindex = ObservableItem.inPorts[name].reduce((max, item) => {
//       return Math.max(max, item.index)
//     }, 0)
//     ObservableItem.inPorts[name].push({ port_id: `${ObservableItem.uuid}_${maxindex + 1}`, port_name: `${name}_${maxindex + 1}`, index: maxindex + 1 })
//   }
// }

watch([ObservableItem.pipes, ObservableItem.subscribe], async (newpipe, newsubscribe) => {
  persistStore()
  // console.log('watch',newpipe, newsubscribe,observerableCardDom.value?.clientHeight)
  // if (currentDom.value) {
  //   const height = <number>currentDom.value?.clientHeight
  //   ObservableItem.location.boxHeight = height ? height : 240
  // }
})
</script>

<style scoped>

/* .card{ */
/* background: #348498; */
/* color: white; */
/* font-size: x-large; */
/* padding: 8px; */
/* border-radius: 2px; */
/* width: 300px */
/* } */
/* div.itemUuid {
  display: block;
  margin-top: 4px;
  color: #4289b9;
}

.argitems {
  margin-top: 2px;
  margin-bottom: 2px;
} */

/* div.subtitle {
  margin-top: 8px;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 18px;
} */
/* .card-tools {
  background: #348498;
  color: white;
  font-size: medium;
} */
</style>
