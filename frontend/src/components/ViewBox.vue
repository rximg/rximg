<template>
  <div class="main" ref="ViewBoxRef" id="viewbox">
    <h1>Viewer</h1>
    <!-- <div></div> -->
    <!-- <img :src="ndimgurl(1)" > -->
    <a-card
      title=""
      class="card"
      style="width: 100% margin-bottom:16px"
      :hoverable="false"
      :headStyle="headTools"
    >
      <template #extra href="#">
        <a-button style="margin-right: 4px" @click="persistStore()"
          >Save
          <a-icon type="play-circle" />
        </a-button>
        <a-button style="margin-right: 4px" @click="execute"
          >Execute
          <a-icon type="play-circle" />
        </a-button>
        <!-- <a-button @click="cleanLogs"
          >Clean
          <a-icon type="delete" />
        </a-button> -->
      </template>
      <!-- <a-row v-for="(item, index) in parameters" :key="index">
        <a-col :span="22">
          <parameter
            :type="item.args.input_.type"
            :name="item.tag"
            :value="item.args.input_.value"
            :viewType="true"
            @emitValue="parameterChange"
          />
        </a-col>
        <a-col :span="2">
          <a-button icon="delete" @click="parameterDel(item.tag)"></a-button>
        </a-col>
      </a-row> -->
    </a-card>
    <div style="margin-top: 16px overflow-y: auto">
      <a-timeline>
        <div v-for="(item, index) in ViewStore.logs" :key="index" > 
        <a-timeline-item  v-if="item.type == 'result' && item.visible==true">
          <div>
            <li>
              {{ item.name }}
            </li>
            <span>
              <a-tag v-for="(text, index) in item.args" :key="index">{{
                text
              }}</a-tag>
              <a-tag v-for="(text, index) in item.kwargs" :key="index">{{
                text
              }}</a-tag>
            </span>

            <a v-if="item.ret.type == 'imshow'">
              <div class="box">
                <img :src="CurrentStateStore.getNdarrayUrl(item.ret.imname)" />
              </div>
            </a>
            <a v-else-if="item.ret.type == 'print'">
              {{ item.ret.show }}
            </a>
            <a v-else-if="item.ret.type == 'NDARRAY'">
              <NDArray
                :title="item.ret.repr"
                :id="item.ret.id"
                :winWidth="width"
                :apiurl="CurrentStateStore.apiurl"
              />
            </a>

            <a v-else>
              <a-tag
                >{{ item.ret }}{{ item.ret.type
                }}{{ item.ret.type == "imshow" }}</a-tag
              >
            </a>
          </div>

        </a-timeline-item>
          <div v-if="item.type == 'exception'">
            <a-button type="danger" style="width=100%" @click="handleTraceVisible(true)"> traceback</a-button>
          </div>
        </div>
      </a-timeline>
      <a-modal 
          :visible="traceModalVisibleFlag" 
          title="traceback" 
          :destroyOnClose="true"
          @ok="handleTraceVisible(false)"
          @cancel="handleTraceVisible(false)">
        <div style="word-break: break-all;" v-for="(text) in traceback">
          {{ text }}
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang='ts'>
//TODO view缩略，缩略args
//TODO 考虑显示最后一个card的subscribe的结果
// import Parameter from "./stateless/Parameter.vue";
// import NDArray from "./stateless/NDArray.vue";
import { onMounted,computed,ref,type Ref } from "vue";
import axios from "axios";
import {ViewStore,CurrentStateStore,persistStore}  from "@/store";
import { useElementSize } from '@vueuse/core'
const headTools = {
        background: "#348498",
        color: "white",
        "font-size": "x-large",
      }
const traceModalVisible = ref(false)
const ViewBoxRef:Ref<any> = ref(null)
// const domWidth = computed(()=>{
//   return ViewBoxRef.value.$el.clientHeight;
// })
// let apiurl = ""
const { width } = useElementSize(ViewBoxRef)
onMounted(
    ()=>{
        // console.log('view this',ViewBoxRef)
        // console.log('get dom',document.getElementById("viewbox"),this.$refs)
        // ViewBoxRef.value.$el.clientHeight;
    }
)
    // ...mapState("views", { allViews: "data", viewResult: "results" }),
    // ...mapGetters("relations", ["relationChange"]),
    // ...mapGetters("views",["traceback",]),
    // // ...mapState("relations", { allRelations: "data" }),
    // ...mapState("views", { resultsLog: "logs", 
    //     parameters: "parameters", }),
const traceModalVisibleFlag = computed(()=>{
      return traceModalVisible.value && traceback.length!=0
    })

    // ...mapActions(["save"]),
    // ...mapMutations("views", ["cleanLogs", "addParameter", "delParameter"]),
// const imgurl= (item)=> {
//       return CurrentStateStore.apiurl + "/ndarray/" + item;
//     }

const traceback = computed(()=>{
        const traces =[]
        for (var i in ViewStore.logs) {
            var item = ViewStore.logs[i]
            if (item.type == 'exception'){
                item.trace.forEach(element => {
                  traces.push(element)
                });
            }
        }
        return traces
    }
)
const handleTraceVisible = (flag:boolean)=>{
      traceModalVisible.value = flag
    }
const  execute = async ()=> {
      ViewStore.cleanLogs()
      await persistStore()
      await axios.get('api/execute')
    //   this.$socket.emit("execute_event",);
      traceModalVisible.value = false
    }
// const parameterChange=(item)=> {
//       this.addParameter(item);
//       this.save();
//     }
// const  parameterDel=(name)=> {
//       // console.log('para:',name)
//       // let {type,value,type } = item.args.input_
//       this.delParameter(name);
//       this.save();
//     }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div.ant-comment-nested {
  margin-left: 15px;
}

/* .box {
  position: relative;
  padding-top: 100%;
  overflow: hidden;
  width: 100%;
  float: left;
}
.box img {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
} */
.box {
  background-size: contain;
}
.box img {
  object-fit: contain;
}
</style>
