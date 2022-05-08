<template>
  <div class="main">
    <!-- <div> -->
    <div v-if="functionData.type">
      <a-divider class="fac-divider" orientation="left">
        {{ functionData.name }}
      </a-divider>
      <p
        style="
          display: flex;
          flex-flow: row nowrap;
          justify-content: space-between;
        "
      >
        <!-- <span v-if="functionData.returns">
        <span v-for="(item, index) in functionData.returns" :key="index">
          <a-button
            :type="funcOutputs[index] ? '' : 'dashed'"
            @click="setFuncOutputIndex(index)"
            >{{ item }}[{{ index }}]</a-button
          >
        </span>
      </span>
      <span v-else>
        <a-button>return[0]</a-button>
      </span> -->
        <span
          ><a-button>{{ functionData.returnType }}</a-button></span
        >
        <span>
          <a-select default-value="" style="width: 120px" @change="setOp">
            <a-select-option value=""> direct </a-select-option>
            <a-select-option value="map"> map </a-select-option>
          </a-select>
        </span>
        <span
          style="display: flex; flex-wrap: nowrap; justify-content: flex-end"
        >
          <a-button v-if="lockedStatus" @click="setLocked(false)">
            <a-icon type="lock" />
          </a-button>
          <a-button style="background: @red-1" @click="submitFunction"
            >Submit</a-button
          >
        </span>
      </p>
      <div @mouseenter="mouseenterDom">
        <div v-if="functionData.type === 'callable'">
            <div
              v-for="(arg, key) in sortObj(functionData.args)"
              :label="arg.name"
              :key="key"
            >
              <!-- {{key}},{{arg.index}} -->
              <arg-item
                :name="arg.name"
                :defaultValue="arg.value"
                :type="arg.type"
                :args="arg"
                :ranges="arg.ranges"
                @emitValue="setArgValue($event, arg.name)"
              />
              <!-- </div> -->
            </div>
            <div
              v-for="rt in functionData.return"
              :label="rt.name"
              :key="rt.name"
            >
              <a-switch v-model="rt.value" />
            </div>
        </div>
        <div v-else-if="functionData.type == 'lambda'">
          <span>
            <a-select
              v-model="lambda.argValue"
              mode="multiple"
              style="width: 100%"
              placeholder="x0"
              option-label-prop="label"
            >
              <a-select-option
                v-for="arg in lambda.argLists"
                :key="arg"
                :value="arg"
                :label="arg"
              >
                {{ arg }}
              </a-select-option>
            </a-select>
            <a-mentions v-model="lambda.line">
              <a-mentions-option
                v-for="arg in lambda.argLists"
                :key="arg"
                :value="arg"
              >
                <span>{{ arg }}</span>
              </a-mentions-option>
            </a-mentions>
          </span>
        </div>
        <div v-else-if="functionData.type == 'parameter'">
          <parameter :viewType="false" @emitValue="setParameter" />
        </div>
        <div v-else-if="functionData.type == 'file'">
          <FileBox @sendArgData="setArgValue($event, 'dirs')" />
        </div>
      </div>
    </div>
    <div v-else><a-empty :description="false" /></div>
    <!-- </div> -->
  </div>
</template>

<script>
// const deepcopy = require('deepcopy');
import { mapGetters, mapMutations, mapActions } from "vuex";
import ArgItem from "./stateless/ArgItem.vue";
import FileBox from "./toolbox/FileBox.vue";
import Parameter from "./stateless/Parameter.vue";
export default {
  data() {
    return {
      lambda: {
        argValue: [],
        argLists: ["x0", "x1", "x2", "x3", "x4"],
        line: "",
      },
      argData: {},
      funcOutputs: {},
      op: "",
      parameterValue: {},
    };
  },
  name: "Factory",
  components: { ArgItem, FileBox, Parameter },
  computed: {
    ...mapGetters("factory", ["lockedStatus", "functionData"]),
    // ...mapGetters(["allRefable"]),
  },
  //
  methods: {
    ...mapActions(["save"]),
    ...mapMutations("observers", [
      "addObserverByFunction",
      "addObserverByLambda",
      "addObserverByFileCreator",

    ]),
    ...mapMutations("relations", ["newRelation"]),
    ...mapMutations("factory", ["delCurrentFunction", "setLocked"]),
    ...mapMutations("views", { setParameterStore: "addParameter" }),

    setFuncOutputIndex(index) {
      index = String(index);
      // console.log("is include",Object.keys(this.funcOutputs).includes(index))
      if (Object.keys(this.funcOutputs).includes(index)) {
        this.funcOutputs[index] = !this.funcOutputs[index];
      } else {
        for (let i = 0; i < this.functionData.returns.length; i++) {
          this.funcOutputs[i] = false;
        }
        this.funcOutputs[index] = true;
      }
      this.funcOutputs = { ...this.funcOutputs };
    },
    mouseenterDom() {
      let not_emputy = Object.keys(this.functionData).length !== 0;
      if (not_emputy) {
        this.setLocked(true);
      }
    },
    submitFunction() {
      switch (this.functionData.type) {
        case "lambda":
          this.addObserverByLambda({ ...this.lambda, op: this.op });
          break;
        case "file":
          this.addObserverByFileCreator(this.argData.dirs);
          break;
        case "parameter":
          // var {type,value } = this.parameterValue.args.input_
          // this.setParameterStore({type:type,name:this.parameterValue.tag,value:value})
          this.setParameterStore(this.parameterValue);
          break;
        default:
          // console.log('funcout',this.funcOutputs);

          // this.functionData.outputs = Object.keys(this.funcOutputs).filter(
          // (k)=>{return this.funcOutputs[k]}
          // ).map(parseInt)
          this.functionData.outputs = this.funcOutputs;
          // console.log("new relation", this.functionData);
          var uuid = this.addObserverByFunction({
            funcData: this.functionData,
            args: this.argData,
            op: this.op,
          });
          console.log("new relation", uuid,this.functionData);

          //TODO 直接提交到observable
          // if (this.functionData.returnType=='Observable'){

          //   this.newRelation(uuid);
          // }
          // this.save();
          break;
      }
      // if (this.functionData.type == "lambda") {
      //   this.addObserverByLambda(this.lambda);
      // } else {``
      //   console.log("submit functionData",this.functionData)

      // }
      this.delCurrentFunction();
      this.setLocked(false);
    },
    sortObj(obj) {
      return Object.values(obj).sort((a, b) => a.index - b.index);
    },
    setArgValue(event, key) {
      console.log("get arg event", key, event);
      this.argData[key] = event;
    },
    setOp(value) {
      this.op = value;
    },
    setParameter(value) {
      this.parameterValue = value;
    },

    // setDirArgData(event){
    //   this.argData=event
    // }
  },
};
</script>

<style scoped>
.fac-divider {
  font-size: 20px;
}
</style>
