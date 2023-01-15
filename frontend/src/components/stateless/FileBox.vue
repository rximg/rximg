<template>
  <div>

    <a-modal :visible="modalVisible" titile="FileManage" @ok="handleOk" @cancel="setVisible(false)">
      <!-- <a>{{ currentDir }}</a> -->
      <a-divider orientation="left">Files</a-divider>

      <a-input-group style="width: 100%" compact>
        <a-input v-model:value="currentDir" style="width: calc(100% - 32px)" />
        <a-tooltip title="current dir">
          <a-button>
            <template #icon>
              <EnterOutlined />
            </template>
          </a-button>
        </a-tooltip>
      </a-input-group>
      <!-- <div> Files </div> -->

      <a-list item-layout="horizontal" :data-source="items" :pagination="pagination">
        <template #renderItem="{ item }">
          <a-list-item>

            <a-button @click="fetchFiles(item.value, item.type)" class="style100" type="text">
              {{ item.value }}
            </a-button>
            <a-button @click="addDirTexts(item.value)">
              <template #icon>
                <PlusOutlined />
              </template>
            </a-button>


          </a-list-item>
        </template>
      </a-list>
      <a-divider orientation="left">Return</a-divider>
      <!-- <div v-for="(text,index) in retDirTexts">
        <a-input-group style="width: 100%" compact>
              <a-input :value="text" @change="changeRetDir($event,index)" style="width: calc(100% - 100px)" />
              <a-tooltip title="current dir">
                <a-button @click="delRetDirByIndex(index)">
                  <template #icon>
                    <CloseOutlined />
                  </template>
                </a-button>

              </a-tooltip>
            </a-input-group>
      </div> -->
          <a-list item-layout="horizontal" :data-source="retDirTexts" :pagination="retPagination">
            <template #renderItem="{ item,index }">
              <a-list-item>
                <a-input-group style="width: 100%" compact>
                  <a-input :value="item" @change="changeRetDir($event,index)" style="width: calc(100% - 40px)" />
                  <a-tooltip title="current dir">
                    <a-button @click="delRetDirByIndex(index)">
                  <template #icon>
                    <CloseOutlined />
                  </template>
                </a-button>
                  </a-tooltip>
                </a-input-group>
              </a-list-item>
            </template>
          </a-list>
    </a-modal>
    <a-button style="width: 100%" @click="setVisible(true)">File[{{ currentDir }}][{{ retDirTexts.length }}]</a-button>
  </div>
</template>

<script lang='ts' setup>
// import infiniteScroll from 'vue-infinite-scroll'
// import { RecycleScroller } from 'vue-virtual-scroller'
// import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
// import { mapActions, mapGetters } from 'vuex'
// TODO 1. 单个文件的模式 2.文件夹模式 3.文件夹搭配glob模式  
// TODO 需要和glob结合起来
// TODO 返回值应该是一个glob的list
import { EnterOutlined, PlusOutlined,CloseOutlined } from '@ant-design/icons-vue'
import { getFiles, initFiles } from '@/store/filesapi.ts'
import { ref, reactive, onMounted, computed, watch } from 'vue'
type itemType = {
  value: string
  type: string
}
const emit = defineEmits(["update:valueModel"]);

const currentDir = ref('~')
const filename = ref("")
const files = ref([] as itemType[]) //ref(<itemType>[])

const retDirTexts = ref([] as string[])
const modalVisible = ref(false);

const items = computed(() => {
  let allFiles = files.value
    allFiles = files.value.filter(function (item) {
      if ((item.value[0] != '.') || (item.value == '..')) {
        return true
      }
    })
  // console.log('len allFiles', allFiles.length, allFiles)
  return allFiles
})
const pagination = {
  pageSize: 10,
}

const retPagination = {
  pageSize: 3,
}
// watch(retDirTexts, (val) => {
//   console.log('update:valueModel', val)
//   // this.$emit('valueModel', val)
//   emit("update:valueModel", val);
// })
// const filenameType = function (text:string) {
//   if (text==filename.value) {
//     return "primary"
//   }else{
//     return ""
//   }
// }


const handleOk = function (e) {
  // console.log('update:value',items)
  emit(
    "update:valueModel",
    retDirTexts.value
  );
  modalVisible.value = false;
};
onMounted(
  () => {
    initFiles().then((res) => {
      files.value = res["data"]
      currentDir.value = res["origin"]
      // console.log("files", files.value, res)
    })
  }
)

const fetchFiles = async function (dir_: string, type: string) {
  if (type != 'file') {
    const { data, origin } = await getFiles(
      dir_,
      currentDir.value,
    )
    // console.log('fetchFiles', data, origin)
    files.value = data
    currentDir.value = origin
  }
}
// const handleInfiniteOnLoad = function () {
//   if (index.value < items.value.length) {
//     index.value += page.value
//   }
// }
// const setDirText = function (text: string) {
//   // this.dirText = this.currentDir + '/' + text
//   filename.value = text
//   console.log('set dir', filename.value)
//   dirText.value = currentDir.value + '/' + text
// }

const changeRetDir = function (e:InputEvent,index:number) {
  // console.log(e,e.target.value)
  retDirTexts.value[index] = e.target.value
}

const delRetDirByIndex = function (index:number) {
  retDirTexts.value.splice(index,1)
}

const addDirTexts = function (text: string) {
  // this.retDirTexts.push(text)

  retDirTexts.value.push(currentDir.value+'/'+text)
}

const setVisible = function (value: boolean) {
  modalVisible.value = value;
};

</script>

<style scoped>
.scroller {
  height: 100%;
}

.user {
  height: 32%;
  padding: 0 12px;
  display: flex;
  align-items: center;
}

/* .style100 {
  width: 100%;
  height: 100%;
} */
</style>