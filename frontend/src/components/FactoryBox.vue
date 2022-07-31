<template>
  <div class="main">
    <!-- <div> -->
    <div v-if="functionData.name">
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
        <span><a-button>{{ functionData.returnType }}</a-button></span>
        <span>
          <a-select
            default-value=""
            style="width: 120px"
            @change="setOp($event)"
          >
            <a-select-option value=""> direct </a-select-option>
            <a-select-option value="map"> map </a-select-option>
          </a-select>
        </span>
        <span
          style="display: flex; flex-wrap: nowrap; justify-content: flex-end"
        >
          <!-- <a-button v-if="lockedStatus" @click="setLocked(false)">
            <a-icon type="lock" />
          </a-button> -->
          <a-button style="background: @red-1" @click="submitFunction">Submit</a-button>
        </span>
      </p>
      <div>

        <div v-if="functionData.type == 'lambda'">
          <!-- <span> -->
            <a-select
              v-model:value="lambda.argValue"
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
            <a-input v-model:value="lambda.line"/>
            <!-- <a-input v-model:value="lambda_line" :allowClear="true" placeholder="Basic usage" /> -->
            {{toRaw(functionData).args.line.value}}
          <!-- </span> -->
        </div>
        <div v-else-if="functionData.type == 'parameter'">
          <parameter
            :viewType="false"
            @emitValue="(val) => (parameterValue = val)"
          />
        </div>
        <div v-else-if="functionData.type == 'file'">
          <FileBox @sendArgData="setArgValue($event, 'dirs')" />
        </div>
        <div v-else>
          <div
            v-for="(arg, key) in functionData.args"
            :key="functionData.name + key"
          >
              <arg-item
                :arg="arg"
              />
          </div>

        </div>
      </div>
    </div>
    <div v-else><a-empty :description="false" /></div>
    <!-- </div> -->
  </div>
</template>

<script setup lang="ts">
//TODO 修复parameters
//TODO 多余的ports可以作为parameters
// import { reactive } from '@vue/reactivity';
import { computed, reactive,ref,toRaw, type Ref,type ShallowRef } from "vue";
// import {  useStore } from "vuex";
import ArgItem from "./stateless/ArgItem.vue";
// import FileBox from "./toolbox/FileBox.vue";
import Parameter from "./stateless/Parameter.vue";
import { CurrentStateStore, RXFunctionsStore,persistStore,ObserverablesStore } from "@/store";
import { Observerable } from "@/store/Observers";
// import {LambdaFunction} from "@/store/RxLibrary";
import type { RXFunction, RXArg } from "@/store/RxLibrary";
// const store = useStore()
const lambda = reactive({
  argValue: ["x0"],
  argLists: ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"],
  line: "",
});

// const LAMBDAARGS = ref(["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]) 
const parameterValue = reactive({});
// const argData = reactive({});
// const functionData: Ref<RXFunction> = computed(
//   () => <RXFunction>CurrentStateStore.function_data.value
// );
// const functionData = <Ref<RXFunction>>CurrentStateStore.function_data;
const functionData = <ShallowRef<RXFunction>>CurrentStateStore.function_data;
// const save = function (params) {
  //   store.dispatch("save", params);
// }
// const lambda_line = ref("");
// const lambda_line = computed(
//   {
//     get() {
//       console.log('computed get ',functionData.value.args.line.value)
//       return functionData.value.args.line.value;
//     },
//     set(value){
//       console.log('set value',value,functionData.value.args.line,functionData.value.args.line.value)
//       functionData.value.args.line.value = value;
//     }
//   }
// );

function submitFunction() {
  console.log('functiondata:',functionData.value,functionData.value.op);
  switch (functionData.value.type) {
    case "parameter":
      console.log("parameter");
      break;
    case "lambda":
      // console.log("lambda", lambda.argValue, lambda.line,lambda);
      const { argValue, line } = lambda;
      functionData.value.args.line.value.value = line;
      functionData.value.args.args.value.value = argValue;
      functionData.value.onSubmit();
      // functionData.value.uuid = functionData.value.md5()
      RXFunctionsStore[functionData.value.uuid] = functionData.value;
      break;
    
    default:
      //以uuid作为唯一的实例，出现重复则报错
      // functionData.value.uuid = functionData.value.md5()
      functionData.value.onSubmit();
      RXFunctionsStore[functionData.value.uuid as string] =
        functionData.value;
      if (functionData.value.returnType=='Observable'){
            let observerable = new Observerable(functionData.value)
            ObserverablesStore[<string>observerable.uuid] = observerable
      }
  }
  CurrentStateStore.setMainMenu(["observer"]);
  CurrentStateStore.cleanFunction();
  persistStore()
}

function sortObj(obj: Record<string, RXArg>): RXArg[] {
  return Object.values(obj).sort((a, b) => a.index - b.index);
}
const setOp = (value)=>{
  // console.log('setOp',value,functionData.value.op)
  functionData.value.op = value
}
function setArgValue(event) {
  console.log("get arg event", event);
  // argData[key] = event;
}
</script>

<style scoped>
.fac-divider {
  font-size: 20px;
}
</style>
