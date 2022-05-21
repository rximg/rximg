<template>
  <div class="main" ref="viewbox" id="viewbox">
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
      <a slot="extra" href="#">
        <a-button style="margin-right: 4px" @click="execute"
          >Execute
          <a-icon type="play-circle" />
        </a-button>
        <!-- <a-button @click="cleanLogs"
          >Clean
          <a-icon type="delete" />
        </a-button> -->
      </a>
      <a-row v-for="(item, index) in parameters" :key="index">
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
      </a-row>
    </a-card>
    <div style="margin-top: 16px overflow-y: auto">
      <a-timeline>
        <div v-for="(item, index) in resultsLog" :key="index" > 
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
                <img :src="imgurl(item.ret.imname)" />
              </div>
            </a>
            <a v-else-if="item.ret.type == 'print'">
              {{ item.ret.show }}
            </a>
            <a v-else-if="item.ret.type == 'NDARRAY'">
              <NDArray
                :title="item.ret.repr"
                :id="item.ret.id"
                :winWidth="domWidth"
              />
              <!-- {{ item.ret.show }} -->
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
          @ok="handleTraceVisible(false)">
        {{ traceback }}
      </a-modal>
    </div>
  </div>
</template>

<script>
//TODO view缩略，缩略args
import Parameter from "./stateless/Parameter.vue";
import NDArray from "./stateless/NDArray.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  name: "Viewer",
  props: {
    msg: String,
  },
  components: { Parameter, NDArray },
  data() {
    return {
      headTools: {
        background: "#348498",
        color: "white",
        "font-size": "x-large",
      },
      domWidth: null,
      traceModalVisible:false

    };
  },
  mounted: function () {
    // console.log('get dom',document.getElementById("viewbox"),this.$refs)
    this.domWidth = this.$refs.viewbox.clientWidth;
  },
  computed: {
    // ...mapState("views", { allViews: "data", viewResult: "results" }),
    // ...mapGetters("relations", ["relationChange"]),
    ...mapGetters("views",["traceback",]),
    // ...mapState("relations", { allRelations: "data" }),
    ...mapState("views", { resultsLog: "logs", 
        parameters: "parameters", }),
    traceModalVisibleFlag() {
      return this.traceModalVisible && this.traceback.length!=0
    },
    // viewWidth:function () {
    //   return this.
    // }
    // ...mapGetters("views", ["allParameters"]),
    // getViews: function() {
    //   var change = this.relationChange;
    //   console.log("view get change time", change);
    //   this.flushViews(this.allRelations);
    //   return this.allViews;
    // },
  },
  // watch
  methods: {
    ...mapActions(["save"]),
    ...mapMutations("views", ["cleanLogs", "addParameter", "delParameter"]),
    imgurl(item) {
      return this.$apiurl + "/ndarray/" + item;
    },
    handleTraceVisible(flag){
      this.traceModalVisible = flag
    },
    execute() {
      this.cleanLogs()
      this.$socket.emit("execute_event",);
      this.traceModalVisible = true
    },
    parameterChange(item) {
      // console.log('para:',item)
      // let {type,value,type } = item.args.input_
      this.addParameter(item);
      this.save();
    },
    parameterDel(name) {
      // console.log('para:',name)
      // let {type,value,type } = item.args.input_
      this.delParameter(name);
      this.save();
    },
  },
};
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
