<template>
  <div class="main">
    <h1>Observerables</h1>
    <div style="overflow-y: auto">
      <a-card
        title=""
        class="card"
        style="width: 100%"
        :hoverable="false"
        :headStyle="headTools"
      >
        <a slot="extra" href="#">
          <a-dropdown>
            <a-menu
              slot="overlay"
              @click="newRelation(onlyObserverKeys[$event.key])"
            >
              <a-menu-item v-for="(text, index) in onlyObserverKeys" :key="index">
                <a-icon type="swap-right" />{{ repr(text) }}
              </a-menu-item>
            </a-menu>
            <a-button style="margin-left: 8px">
              New <a-icon type="plus-circle" />
            </a-button>
          </a-dropdown>
          <a-dropdown>
            <a-menu
              slot="overlay"
              @click="newSubject(relationKeys[$event.key])"
            >
              <a-menu-item v-for="(text, index) in relationKeys" :key="index">
                <a-icon type="swap-right" />{{ repr(text) }}
              </a-menu-item>
            </a-menu>
            <a-button style="margin-left: 8px">
              Subject <a-icon type="plus-circle" />
            </a-button>
          </a-dropdown>
          <a-dropdown>
            <a-menu
              slot="overlay"
              @click="newSubscribe(relationKeys[$event.key])"
            >
              <a-menu-item v-for="(text, index) in relationKeys" :key="index">
                <a-icon type="swap-right" />{{ repr(text) }}
              </a-menu-item>
            </a-menu>
            <a-button style="margin-left: 8px">
              Subscirbe <a-icon type="plus-circle" />
            </a-button>
          </a-dropdown>
        </a>
        <!-- </a> -->
      </a-card>
      <div v-for="(item, index) in relationsData" :key="index">
        <a-space direction="vertical" style="width: 100%">
          <div v-if="item.type == 'observerable' || item.type == 'subject'">
            <a-card
              :title="repr(item.args.head.value)"
              class="card"
              style="width: 100%"
              :headStyle="headHead"
            >
              <a slot="extra" href="#">
                <a-button-group>
                  <a-dropdown v-if="item.type == 'observerable'">
                    <a-menu
                      slot="overlay"

                      
                      @click="
                        addPipe({
                          key: index,
                          pipe_uuid: onlyCallableKeys[$event.key],
                        })
                      "
                    >
                      <a-menu-item
                        v-for="(text, index) in onlyCallableKeys"
                        :key="index"
                      >
                        <a-icon type="swap-right" />{{ repr(text) }}
                      </a-menu-item>
                    </a-menu>
                    <a-button style="margin-left: 8px">
                      Pipe <a-icon type="plus-circle" />
                    </a-button>
                  </a-dropdown>
                  <a-button @click="newRelation(index)"
                    ><a-icon type="copy" /></a-button>
                  <!-- <a-button @click="newSubject(index)"
                    ><a-icon type="branches" /></a-button> -->
                  <a-button @click="deleteRelation(index)"
                    ><a-icon type="delete"
                  /></a-button>
                </a-button-group>
              </a>
              <div v-if="item.type == 'observerable'">

              <!-- <div class="subtitle">pipe:</div> -->
              <span v-if="!isEmputy(item.args.pipe.value)">
                <draggable
                  v-model="item.args.pipe.value"
                  group="people"
                  @start="drag = true"
                  @end="endDrag($event, index)"
                >
                  <span
                    v-for="(pipe, pkey) in item.args.pipe.value"
                    :key="pkey"
                  >
                    <a-tag
                      v-if="pipe"
                      closable
                      @close="tagDeletePipe(index, pkey)"
                    >
                      {{ repr(pipe) }}
                    </a-tag>
                  </span>
                </draggable>
              </span>
              <span v-else>
                EmputyPipe
              </span>
              </div>

                <div class="itemUuid">{{ index }}</div>
            </a-card>
          </div>
          <div v-if="item.type == 'subscribe'">
            <a-card
              :title="repr(item.args.head.value)"
              class="card"
              style="width: 100%"
              :headStyle="headSubscribe"
            >
              <a slot="extra" href="#">
                <a-button-group>
                  <a-button @click="deleteRelation(index)"
                    ><a-icon type="delete"
                  /></a-button>
                </a-button-group>
              </a>
              <a-select
                :default-value="repr(item.args.subscribe.value)"
                style="width: 60%"
                @change="setSubscribe({ key: index, subscribe_uuid: $event })"
              >
                <a-select-option
                  v-for="(text, nobkindex) in onlyCallableKeys"
                  :key="nobkindex"
                  :value="text"
                >
                  {{ repr(text) }}
                </a-select-option>
              </a-select>
            </a-card>
          </div>
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
export default {
  name: "Relations",
  data() {
    return {
      headTools: {
        background: "#348498",
        color: "white",
        "font-size": "x-large",
      },
      headHead: {
        background: "#8bc6af",
        color: "white",
        "font-size": "x-large",
      },
      headSubscribe: {
        background: "#FFC329",
        color: "white",
        "font-size": "x-large",
      },
    };
  },
  components: { draggable },
  computed: {
    ...mapGetters("relations", { relationKeys: "keys" }),
    ...mapGetters("observers", { allObserverKeys: "keys",}),
    ...mapGetters(["repr"]),
    ...mapState("relations", {
      relationsData: "data",

      // activateIndex: "index",
      changeTimes: "contentChangeTimes",
    }),
    ...mapState("observers",{
      observersData:"data",
    }),
    onlyObserverKeys:function () {
      return this.allObserverKeys.filter(
          (key)=>this.observersData[key].returnType == "Observable"
      )
    },
    onlyCallableKeys:function () {
      return this.allObserverKeys.filter(
          (key)=>this.observersData[key].returnType != "Observable"
      )
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
      "newRelation",
      "newSubscribe",
      "addPipe",
      "setSubscribe",
      "deletePipe",
      "cleanSubscribe",
      "swapPipes",
      "deleteRelation",
      "newSubject",
      "IdentityObserverable"
    ]),
    tagDeletePipe(headindex, pipeindex) {
      this.deletePipe({ key: headindex, pipe_index: pipeindex });
    },
    isEmputy,
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
.a-card {
  margin: 20px;
}
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
div.subtitle {
  margin-top: 8px;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 18px;
}
.card-tools {
  background: #348498;
  color: white;
  font-size: x-large;
}
</style>
