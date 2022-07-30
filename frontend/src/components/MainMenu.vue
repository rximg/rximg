<template>
  <div class="mainMenu" :style="hHeight">
  <EditSelect/>
    <a-menu v-model:selectedKeys="current" mode="horizontal" :multiple=false>
      <a-menu-item key="library">
        <template #icon>
          <mail-outlined />
        </template>
        Library
      </a-menu-item>
      <a-menu-item key="factory">
        <template #icon>
          <appstore-outlined />
        </template>
        Factory
      </a-menu-item>
      <a-menu-item key="observer">
        <template #icon>
          <appstore-outlined />
        </template>
        Observers
      </a-menu-item>
      <a-menu-item key="view">
        <template #icon>
          <appstore-outlined />
        </template>
        View
      </a-menu-item>
    </a-menu>
        <draggable v-model="testlist" group="people" @start="startDrag($event)" @end="endDrag($event)">
          <template #item="{ element, index }">
            <a-tag   class="argitems" :visible="true" closable >
                {{ element }}
            </a-tag>
          </template>
        </draggable>
    <div v-show="current[0] === 'library'"><LibraryBox></LibraryBox></div>
    <div v-show="current[0] === 'factory'"><Factory></Factory></div>
    <div v-show="current[0] === 'observer'"><Observer></Observer></div>
    <div v-show="current[0] === 'view'"><ViewBox></ViewBox></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref,reactive, toRef, computed, onMounted} from "vue";
// import {useStore} from "vuex";
import draggable from "vuedraggable";

import {  CurrentStateStore } from "@/store";
import LibraryBox from "./LibraryBox.vue";
import Factory from "./FactoryBox.vue";
import Observer from "./ObserversBox.vue";
import ViewBox from "./ViewBox.vue";
import EditSelect from "./stateless/EditSelect.vue";

export default defineComponent({
  name: "MainMenu",
  components: {
    LibraryBox,
    Observer,
    Factory,
    ViewBox,
    EditSelect,
    draggable
},
  setup() {
    // const store = useStore()
    const current = CurrentStateStore.main_menu;
    const testlist = reactive(['1', '2', '3']);
    const drag = ref(false)
    const startDrag=(e)=>{
      drag.value = true
    }
    const endDrag = (e) => {
      console.log('drag',e)
      drag.value = false;
    }
    // onMounted(
    //     ()=>store.dispatch('initStore') 
    // )
    const winHeight = computed(() => {
      return window.innerHeight;
    });
    const hHeight = {
      height: winHeight.value - 5 + "px",
    };
    return {
      current,
      hHeight,
      testlist,
      startDrag,
      endDrag
    };
  },
});
</script>

<style scoped>
.mainMenu {
  width: 480px;
  background-color: white;
  overflow-y: hidden;
}
</style>