<template>
  <span >
    <!-- <a-tag v-if="pipe" closable @close="tagDeletePipe(index, pkey)"> -->
    <span>{{ breifTitleByUUID(item.uuid)}}- </span>
    <!-- <span>{{ item.name }}</span> -->
    <span> <a-icon   style="margin-left:2px" v-if="item.if_view" type="eye"/></span>
    <a-divider style="margin:0px" />

    <span>{{ item.uuid }}</span>
    <!-- </a-tag> -->
  </span>
</template>

<script>
import { mapGetters, mapMutations, mapState } from "vuex";

export default {
  name: "BriefTag",
  data() {
    return {};
  },
  props: {
    item: Object,
  },
  computed:{
    ...mapGetters("observers", ["breifTitleByUUID"]),
  }
};
</script>
