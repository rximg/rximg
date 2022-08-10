<template>
  <div class="main" :style="{ height: bodyHeight + 'px' }">
    <div v-for="(item, index) in rxfunctionItems" :key="index">
      <a-space direction="vertical" style="width: 100%">
        <a-card :title="item.toString()" :hoverable="true" :headStyle="getHeadStyle(item.uuid)">
          <template v-slot:extra>
            <a href="#">
              <a-button @click="deleteItem(item)">
                <delete-outlined />
              </a-button>
            </a>
          </template>

          <template v-if="item.type == 'lambda'">
            <div>
              <a-tag style="background-color: #ebb471">{{ item.toString() }}
              </a-tag>
            </div>
          </template>
          <template v-else>
            <template v-for="(data, name) in item.args" :key="data.index">
              <template v-if="data.mutable">
                <arg-item :arg="data"></arg-item>
              </template>
              <template v-else>
                <a-tag class="argitems">
                  <a>{{ name }}</a>
                  <a-divider type="vertical"></a-divider>
                  <a>{{ data.toString() }}</a>
                  <a-divider type="vertical"></a-divider>
                  <a>{{ data.type }}</a>
                </a-tag>
              </template>
            </template>

          </template>
          <div class="itemUuid">{{ item.uuid }}</div>
        </a-card>
      </a-space>
    </div>
  </div>
</template>

<script setup lang="ts">
// import { mapGetters, mapState, mapMutations } from 'vuex'
//FIXME bug添加args时候变成两个
//TODO 部分函数不需要显示在view里。
//TODO 检查一下输入是否是placeholder，而不是""
import { computed, toRaw, ref } from "vue";
import type { ShallowReactive } from "vue";
import {
  CurrentStateStore,
  RXFunctionsStore,
  ObserverablesStore,
} from "@/store";
import ArgItem from "./stateless/ArgItem.vue";

// import { isString } from '../store/utils.js'
// import { sortObj } from '../store/utils'
import { getColorByHex } from "@/components/toolbox/color.js";

import { DeleteOutlined } from "@ant-design/icons-vue";
// import { Observerable } from "@/store/Observers";
import { persistStore } from '@/store'
// import type {ObserverableInterface} from "@/types/Observers.ts";
import type { RXFunctionInterface, RXArgInterface } from "@/store/RxLibrary";
const getHeadStyle = (uuid: string) => {
  var color = getColorByHex(uuid);
  return {
    background: color,
    color: "white",
    "font-size": "medium",
  };
}
const tagStyle = {
  "-": {
    background: "#FFC329",
  },
  "parse error": {
    background: "red",
  },
};
const rxfunctionItems: ShallowReactive<Record<string, RXFunctionInterface>> = RXFunctionsStore;
// const repr = (uuid:string) => {
//   return uuid.substring(0, 8)
// }
const bodyHeight = ref(document.body.clientHeight-68);
const deleteItem = (item: RXFunctionInterface) => {
  delete rxfunctionItems[item.uuid as string];
  persistStore()
};

function sortObj(obj: Record<string, RXArgInterface>): RXArgInterface[] {
  return Object.values(obj).sort((a, b) => a.index - b.index);
}
//@vue/compiler-sfc] the >>> and /deep/ combinators have been deprecated. Use :deep() instead
</script>

<style scoped>
div.main {
  padding: 10px;
  overflow-y: scroll;
  overflow-x: hidden;
}

div.itemUuid {
  display: block;
  margin-top: 4px;
  color: #4289b9;
}

.argitems {
  margin-top: 2px;
  margin-bottom: 2px;
}

.card :deep(.ant-card-head) {
  background-color: #bf6766;
  color: white;
  font-size: medium;
}

.card-ob :deep(.ant-card-head) {
  background-color: #00704f;
  color: white;
  font-size: medium;
}
</style>
