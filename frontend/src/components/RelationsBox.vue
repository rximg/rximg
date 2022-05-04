<template>
  <div class="main">
    <h1>Observerables</h1>
    <div style="overflow-y: auto">
      <div v-for="(item, uuid) in relationsData" :key="uuid">
        <a-space direction="vertical" style="width: 100%">
          <a-card
            :title="repr(item.args.head.value)"
            class="card"
            style="width: 100%"
            :headStyle="headHead"
          >
            <a slot="extra" href="#">
              <a-button-group>
                <a-dropdown>
                  <a-menu
                    slot="overlay"
                    @click="
                      addPipe({
                        key: uuid,
                        pipe_uuid: onlyCallableKeys[$event.key],
                      })
                    "
                  >
                    <a-menu-item
                      v-for="(text, pipe_index) in onlyCallableKeys"
                      :key="pipe_index"
                    >
                      <a-icon type="swap-right" />{{ repr(text) }}
                    </a-menu-item>
                  </a-menu>
                  <a-button style="margin-left: 8px">
                    Pipe <a-icon type="plus-circle" />
                  </a-button>
                </a-dropdown>
                <a-dropdown>
                  <a-menu slot="overlay">
                    <template v-if="isMultiCast(item)">
                      <a-menu-item 
                      :disabled="item.args.subscribe.extraData.value.length!=0"
                      @click="swapSubscribeType({uuid:uuid,flag:'multicast'})"
                      >
                        <a-icon type="swap" /> SingleCast
                      </a-menu-item>
                      
                      <a-menu-item
                       @click="addMulticast(uuid)">
                        <a-icon type="plus-circle" />AddReplaySubject
                      </a-menu-item>
                    </template>
                    <template v-else>
                      <a-menu-item
                      @click="swapSubscribeType({uuid:uuid,flag:'single'})"
                      >
                        <a-icon type="swap" /> MultiCast
                      </a-menu-item>
                      <a-menu-item @click="setSubscribe({uuid:uuid,value:null})">
                        <a-icon type="interaction" /> clean
                        </a-menu-item>
                      <a-menu-item
                        v-for="(text, nobkindex) in onlyCallableKeys"
                        :key="nobkindex"
                        :value="text"
                        @click="setSubscribe({uuid:uuid,value:text})"
                      >
                        <a-icon type="rocket" />{{ repr(text) }}
                      </a-menu-item>
                    </template>
                  </a-menu>
                  <a-button> Subscribe <a-icon type="plus-circle" /> </a-button>
                </a-dropdown>
                <a-button @click="deleteRelation(uuid)"
                  ><a-icon type="delete"
                /></a-button>
              </a-button-group>
            </a>
            <div>
              <span v-if="!isEmputy(item.args.pipe)">
                <draggable
                  v-model="item.args.pipe.value"
                  group="people"
                  @start="drag = true"
                  @end="endDrag($event, uuid)"
                >
                  <span
                    v-for="(pipe, pkey) in item.args.pipe.value"
                    :key="pkey"
                  >
                    <a-tag
                      class="argitems"
                      v-if="pipe"
                      closable
                      @close="tagDeletePipe(uuid, pkey)"
                    >
                      {{ repr(pipe) }}
                    </a-tag>
                  </span>
                </draggable>
              </span>
              <span v-else> <a-tag>...</a-tag> </span>
            </div>
            <div v-if="!isEmputy(item.args.subscribe)">
              <div v-if="item.args.subscribe.extraData.type == 'single'">
                <!-- 处理空的select -->
                <a-tag color="#108ee9">
                  {{ repr(item.args.subscribe.value) }}
                </a-tag>
              </div>
              <div v-if="item.args.subscribe.extraData.type == 'multicast'">
                <!-- 处理空的select -->
                <span
                  v-for="(subindex, sublistindex) in item.args.subscribe.extraData
                    .value"
                  :key="sublistindex"
                >
                  <a-tag color="purple">
                    {{ subindex }}
                  </a-tag>
                </span>
                <!-- <a-tag color="#108ee9">
                  {{repr(item.args.subscribe.value)}}
                </a-tag> -->
              </div>
            </div>
            <div class="itemUuid">{{ uuid }}</div>
          </a-card>
        </a-space>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState, mapActions } from "vuex";
import { isEmputy } from "../store/utils.js";
// import BriefTag from "./stateless/BriefTag.vue";
import draggable from "vuedraggable";

//TOP antdv实现以有向图的方式展示关系。显示在relation下方。
//TODO 需要保持一个顺序
export default {
  name: "Relations",
  data() {
    return {
      headTools: {
        background: "#348498",
        color: "white",
        "font-size": "medium",
      },
      headHead: {
        background: "#8bc6af",
        color: "white",
        "font-size": "medium",
      },
      headSubscribe: {
        background: "#FFC329",
        color: "white",
        "font-size": "medium",
      },
    };
  },
  components: { draggable },
  computed: {
    ...mapGetters("relations", { relationKeys: "keys" }),
    ...mapGetters("observers", { allObserverKeys: "keys" }),
    ...mapGetters(["repr"]),
    ...mapState("relations", {
      relationsData: "data",

      // activateIndex: "index",
      changeTimes: "contentChangeTimes",
    }),
    
    ...mapState("observers", {
      observersData: "data",
    }),
    onlyObserverKeys: function () {
      return this.allObserverKeys.filter(
        (key) => this.observersData[key].returnType == "Observable"
      );
    },
    onlyCallableKeys: function () {
      return this.allObserverKeys.filter(
        (key) => this.observersData[key].returnType != "Observable"
      );
    },
    nullHeadObserverKeys: function () {
      let arr = [];
      this.observerKeys.forEach((item) => {
        arr.push(item);
      });
      return arr;
    },
    // ...mapState("relations",["index"])
  },
  methods: {
    ...mapActions(["save"]),
    ...mapMutations("relations", [
      

      "swapSubscribeType",
      "addMulticast",
      "deleteMulticast",
      "setSubscribe",
      "deleteRelation",

      "addPipe",
      "deleteRelation",
      "deletePipe",
    ]),
    tagDeletePipe(headindex, pipeindex) {
      this.deletePipe({ key: headindex, pipe_index: pipeindex });
    },
    isEmputy,
    isMultiCast:(item) => {
      let subscribe = item.args.subscribe
      if (subscribe){
        let extraData = subscribe.extraData
        if (extraData){
          if (extraData.type=='multicast'){
            return true
          }
        }
      }
      return false

    },
    // switchMultiCast(flag){
    //   console.log('switch multicast',flag)   
    // },
    // setSubscribeSingle(item){
    //   console.log('set subscribe',item)
    // },
    // addReplaySubject(item){
    //   console.log('add replay subject',item)
    // },
    endDrag(e, index) {
      // console.log('drag',e,index)
      this.drag = false;
      this.swapPipes({
        relationIndex: index,
        oldIndex: e.oldIndex,
        newIndex: e.newIndex,
      });
    },
  },
  watch: {
    changeTimes: function (params) {
      this.save();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* .a-card {
  margin: 10px;
} */
/* .card{
    background: #348498;
    color: white;
    font-size: x-large;
    padding: 8px;
    border-radius: 2px;
} */
div.itemUuid {
  display: block;
  margin-top: 4px;
  color: #4289b9;
}
.argitems {
  margin-top: 2px;
  margin-bottom: 2px;
}
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
