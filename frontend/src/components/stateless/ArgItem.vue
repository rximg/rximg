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
            show-search
            :options="choicesOptions"
            :filter-option="choicesFilterOption"
            v-model:value="arg_value"
          >
          </a-select>
        </div>
        <div v-else-if="type == 'list'">
            <List @update:valueModel="(value)=> arg_value=value" />
          </div>
        <div v-else-if="type == 'tuple'">
          <a-input v-model:value="arg_value" style="width: 100%" />
        </div>
        <div v-else-if="type == 'None'">
          <a-input v-model:value=None disabled="true" style="width: 100%" />
        </div>
        <div v-else-if="type == 'ref'">
          <a-select
            style="width: 100%"
            :options="refOptions"
            v-model:value="arg_value"
          >
          </a-select>
        </div>
        <div v-else>
          <a-input v-model:value="arg_value" style="width: 100%" />
        </div>
        <!-- <a-alert v-if="alertValue" :message="alertValue" banner /> -->
      </a-col>
      <a-col :span="3">
        <a-switch v-model:checked="mutable" checked-children="var" un-checked-children="const">
          
        </a-switch>
      </a-col>
      <a-col :span="2">
        <a-select v-model:value="type" >
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
import { computed, ref, toRaw, isProxy,watch } from "vue";

type PropsType = {
  arg: RXArg | ChoiceArg;
  types?: string[];
};
const {
  arg,
  types = ["bool", "int", "float", "choices", "list", "tuple", "ref","None"],
} = defineProps<PropsType>();

const name = arg.name;
const type = ref(arg.type);
const arg_value = arg.value;
const mutable = ref(arg.mutable)
const allRXfunctions = computed(() => {
  return Object.values(RXFunctionsStore);
});
watch(type, (newValue, oldValue) => {
  // if (newValue !== oldValue) {
    console.log('arg type watch',newValue,oldValue);
    if (newValue === "None") {
      arg.type = newValue
      arg.value.value = null
    }else{
      arg.type = newValue;
    }
  // }  
});
watch(mutable, (newValue, oldValue) => {
  arg.mutable = newValue;
});
const get_choices = (arg: ChoiceArg) => Object.keys(arg.choices).map(
  (key) => ({ label:`${key}[${arg.choices[key]}]`, value:arg.choices[key]}) );

const choicesOptions = arg.type=='choices'?get_choices(arg):[]
const choicesFilterOption = (input: string, option: any) => {
      return option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };
// if (arg.type == 'choices'){
  // choicesOptions = get_choices(arg);
// }
const refOptions = computed(
  ()=> allRXfunctions.value.map(
    (value) => ({ label:value.toString(), value:`@${value.uuid}`})
  )
) 
// const refOptions = get_refchoices
// console.log('ref',refOptions);
const emits = defineEmits<(e: "emitValue", value: any) => void>();
</script>