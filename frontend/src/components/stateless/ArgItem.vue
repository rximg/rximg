<template>
  <div>
    <a-row>
      <a-col :span="6"> {{ name }}: </a-col>
      <a-col :span="12">
        <div v-if="type == 'bool'">
          <a-switch v-model:checked="arg_value" />
        </div>
        <div v-else-if="type == 'int'">
          <a-input-number style="width: 100%" v-model:value="arg_value" />
        </div>
        <div v-else-if="type == 'float'">
          <a-input-number
            style="width: 100%"
            v-model:value="arg_value"
            :step="0.1"
          />
        </div>
        <div v-else-if="type == 'choices'">
          <a-select
            style="width: 100%"
            :options="options"
            v-model:value="arg_value"
          >
            <!-- <a-select-option
              v-for="(value, label) in get_choices(arg)"
              :key="label"
            >
              {{ label }}[{{ value }}]
            </a-select-option> -->
          </a-select>
        </div>
        <div v-else-if="type == 'list'">
            <List @update:valueModel="(value)=> arg_value=value" />
          </div>
        <div v-else-if="type == 'tuple'">
          <a-input v-model:value="arg_value" style="width: 100%" />
        </div>
        <div v-else-if="type == 'ref'">
          <a-select style="width: 100%" v-model="arg_value">
            <a-select-option
              v-for="(value, index) in allRXfunctions"
              :key="index"
            >
              {{ value.toString() }}
            </a-select-option>
          </a-select>
        </div>
        <div v-else>
          <a-input v-model:value="arg_value" style="width: 100%" />
        </div>
        <!-- <a-alert v-if="alertValue" :message="alertValue" banner /> -->
      </a-col>
      <a-col :span="2">
        <a-select v-model:value="type">
          <a-select-option
            v-for="(value, index) in types"
            :key="index"
            :value="value"
          >
            {{ value }}
          </a-select-option>
        </a-select>
        <!-- <a-button
            @mouseover="setValueFromRefs(true)"
            @mouseleave="clearTimeout"
            ><paper-clip-outlined /></a-button> -->
      </a-col>
    </a-row>
  </div>
</template>

<script lang='ts' setup>
import List from "./List.vue";
import { PaperClipOutlined, EditOutlined } from "@ant-design/icons-vue";
import type { RXArg, ChoiceArg, CommonValueType } from "@/store/RxLibrary";
import { RXFunctionsStore } from "@/store";
import { computed, ref, toRaw, isProxy } from "vue";

type PropsType = {
  arg: RXArg | ChoiceArg;
  types?: string[];
};
const {
  arg,
  types = ["bool", "int", "float", "choices", "list", "tuple", "ref"],
} = defineProps<PropsType>();

const name = arg.name;
const type = ref(arg.type);
const arg_value = arg.value;
const allRXfunctions = computed(() => {
  return Object.values(RXFunctionsStore);
});
const get_choices = (arg: ChoiceArg) => {
const choices = []
  Object.keys(arg.choices).forEach(
    (key) => choices.push({ label:`${key}[${arg.choices[key]}]`, value:arg.choices[key]})
  );  
  console.log(choices);
  return choices
};
let options = []
if (arg.type == 'choices'){
  options = get_choices(arg);
}
const emits = defineEmits<(e: "emitValue", value: any) => void>();
</script>