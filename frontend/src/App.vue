<template>
  <div class="container">
    <a-row type="flex">
      <a-col flex="480px">
        <MainMenu></MainMenu>
      </a-col>
      <a-col flex="auto">
        <template v-if="CurrentStateStore.global_datarefresh">
          <Graph :autoResize="true" @ready="ready">
            <!-- <VueShape
          primer="rect"
          :id="librarynode"
          :x="10"
          :y="10"
          :width="160"
          :attrs="{ rect: { fill: '#ddd' } }"
          @added="added"
          @cell:change:zIndex="changed"
          :zIndex="9999"
        ></VueShape> -->
            <template v-for="(node, nkey) in ObserverablesStore" :key="nkey">
              <VueShape primer="rect" :id="nkey" :x="node.location.x" :y="node.location.y"
                :width="node.location.boxWidth" :height="node.location.boxHeight" :attrs="{ rect: { fill: '#ddd' } }"
                @cell:change:zIndex="changed">
                <div>
                  <ObserverableCard :ObservableItem="node"></ObserverableCard>
                </div>
                <template #port>

                  <PortGroup name="in" position="top" :attrs="{ circle: { r: 6, magnet: true, stroke: '#31d0c6' } }">
                    <template v-for="(port, port_index) in inPorts(node)" :key="port_index">

                      <Port :id="port.port_id" />
                    </template>
                  </PortGroup>

                  <PortGroup name="out" position="bottom"
                    :attrs="{ circle: { r: 6, magnet: true, stroke: '#C1693C' } }">
                    <template v-for="(port, port_index) in outPorts(node)" :key="port_index">
                      <Port :id="port" />
                    </template>
                  </PortGroup>
                </template>
              </VueShape>
            </template>

            <template v-for="(edge, ekey) in CurrentStateStore.edges" :key="ekey">
              <template v-if="edge">
                <Edge :id="ekey" :source="edge.source" :target="edge.target"
                  :router="{ name: 'metro', args: { padding: 10 } }" :label="ekey" />
              </template>
            </template>
            <Scroller :width="graphWidth" :height="graphHeight" />
            <Background />
            <Grid :visible="true" />

            <Snapline />

            <MouseWheel />
            <MiniMap />

            <Connecting :validateEdge="validateEdge" :allowBlank="false" allowMulti="withPort" :allowLoop="false"
              :allowEdge="false" :allowPort="true" />
            <TeleportContainer />
          </Graph>
        </template>

      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts">


import { defineComponent, ref, h, toRefs, computed, shallowRef, onMounted } from "vue";
import { Port, PortGroup, TeleportContainer } from "antv-x6-vue";
import Graph, {
  Node,
  Edge,
  VueShape,
  useVueShape,
  VueShapeProps,
  GraphContext,
  useCellEvent,
  Grid,
  Background,
  Clipboard,
  Snapline,
  Selection,
  Keyboard,
  Scroller,
  MouseWheel,
  MiniMap,
  Connecting,
} from "antv-x6-vue";

import _ from 'lodash'
// import Observerable from "./components/ObservableCard.vue";
import ObserverableCard from "./components/ObserverableCard.vue";
// import { Menu } from "ant-design-vue";
// import {useStore} from 'vuex';
import "ant-design-vue/es/menu/style/css";
// import demo from '../src/components/demo.vue'
// import VueDemo from "./components/VueDemo.vue";
import MainMenu from "./components/MainMenu.vue";
import {
  initStore,
  ObserverablesStore,
  RXFunctionsStore,
  CurrentStateStore,
  persistStore,
  ViewStore,
} from "@/store";
import type { Observerable } from "./store/Observers";

const App = defineComponent({
  name: "App",
  setup(props, context) {

    const bodyWidth = ref(document.body.clientWidth);
    const graphWidth = computed(() => bodyWidth.value - 480);

    onMounted(async () => {
      await initStore();
      window.onresize = () => {
        return (() => {
          bodyWidth.value = document.documentElement.clientWidth;
        })()
      }

    });

    const outPorts = computed(() => (node: Observerable) => {
      // console.log('outports index', node.subscribe.cast_value)
      if (typeof node.subscribe.cast_value == 'number') {
        //最大长度为this.subscribe.cast_value 的列表
        const result = Array.from({ length: node.subscribe.cast_value }, (_, i) => `${node.uuid}_out_${i}`)
        // console.log('outPorts', result)
        return result
      } else {
        return []
      }
    })
    type InPort = {
      name: string,
      port_id: string,
      index: number,
    }
    const inPorts = computed(() => (node: Observerable) => {
      const port = node.upstream.extraInPorts
      const result: InPort[] = []
      if (port) {
        Object.keys(port).forEach(
          (key) => {
            const value = port[key]
            if (value > 0) {
              for (let i = 0; i < value; i++) {
                result.push({ name: key, index: i, port_id: `${node.upstream.uuid}_${key}_${i}` })
              }
            } else {
              result.push({ name: key, index: 0, port_id: `${node.upstream.uuid}_${key}_${0}` })
            }
          }
        )
        // console.log('input ports', result)
        return result
        // return Array.from({ length: this.upstream.extraInPorts.index }, (_, i) => `${this.uuid}_in_${i}`)
      } else {
        return []
      }
    })
    const removedEdge = async ({ edge }) => {
      console.log("removedEdge", edge);
      delete CurrentStateStore.edges[edge.id];
      persistStore()
    };
    const changedEdge = async ({ edge }) => {
      console.log("changedEdge", edge);
      CurrentStateStore.edges[edge.id] = { source: edge.source, target: edge.target };
      persistStore()
    };


    const ready = ({ graph }) => {
      graph.on("edge:connected", ({ isNew, edge }) => {
        changedEdge({ edge })

      })
      graph.on("edge:dblclick", removedEdge);

    }
    return {
      // stencil,
      // addedEdge,
      graphWidth,
      ready,
      inPorts,
      outPorts,
      // global_library,
      ObserverablesStore,
      RXFunctionsStore,
      CurrentStateStore,
      ViewStore,
      // computedBoxSize,
      graphHeight: ref(document.body.clientHeight),
    };
  },
  components: {
    Graph,
    Node,
    Edge,
    // VueDemo,
    MainMenu,
    Grid,
    Background,
    ObserverableCard,
    // Clipboard,
    Snapline,
    // demodata,
    // Selection,
    Scroller,
    // Keyboard,
    MouseWheel,
    Connecting,
    MiniMap,
    VueShape,
    // CustomNode,
    // Stencil,
    // StencilGroup,
    // ContextMenu,
    // Menu,
    // MenuItem,
    Port,
    PortGroup,
    TeleportContainer,
  },
});

export default App;
</script>

<style lang="less">
.container {

  // display: flex;
  // height: 99vh;
  .x6-graph-scroller {
    height: 100%;
  }

  // .stencil {
  //   width: 100%;
  //   height: 100%;
  //   position: relative;
  // }
  // #graph-contaner {
  //   flex: 1;
  // }
}
</style>
