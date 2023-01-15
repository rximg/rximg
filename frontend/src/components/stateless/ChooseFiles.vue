<template>
  <button type="button" @click="open()">
    Choose files
  </button>
  <button type="button" :disabled="!files" @click="reset()">
    Reset
  </button>
  <template v-if="files">
    <p>You have selected: <b>{{ files.length }} files</b></p>
    <li v-for="file of files" :key="file.name">
      {{ file.name }}
    </li>
  </template>
</template>


// Component
<script setup lang="ts">
import { useFileDialog } from '@vueuse/core'
import {watch} from 'vue'
const { files, open, reset } = useFileDialog()
const emit = defineEmits(["update:valueModel"]);
// vue use filedialog 应该不用了

watch(

    files,(items,old)=>{
        console.log('get files',items,old);
//         emit(
//             "update:valueModel",
//             items.map(function (item) {
//                 return item.name;
//     })
//   );
}
)
  
</script>