<template>
  <div class="main">
    <h1>Operators</h1>
      <div v-for="(item, index) in allObserver" :key="index">
        <a-space direction="vertical" style="width: 100%">
          <a-card
            :title="repr(item.uuid)"
            class="card"
            style="width: 100%; display: block"
            :hoverable="true"
          >
            <a slot="extra" href="#">
              <a-button @click="deleteItem(item)"
                ><a-icon type="delete"
              /></a-button>
            </a>

            <template v-if="item.type == 'lambda'">
              <div>
                <a-tag style="background-color: #ebb471"
                  >{{ item.line }}
                </a-tag>
              </div>
            </template>
            <template v-else>
              <a-tag
                class="argitems"
                v-for="(data, index) in sortObj(item.args)"
                :key="index"
                :style="tagStyle[viewValue(data.value)]"
                @click="tagToTitile(item.uuid, data.name)"
              >
                <a>{{ data.index }}</a>
                <a-divider type="vertical"></a-divider>
                <a>{{ data.name }}</a>
                <a-divider type="vertical"></a-divider>
                <a>{{ viewValue(data.value) }}</a>
                <a-divider type="vertical"></a-divider>
                <a>{{ data.type }}</a>
              </a-tag>
              <span v-if="item.output">
                <span v-for="(item, rindex) in item.output" :key="rindex">
                  <a-tag>return[{{ item }}]</a-tag>
                </span>
              </span>
              <span v-else>
                <a-tag>return[0]</a-tag>
              </span>
            </template>
            <div class="itemUuid">{{ item.uuid }}</div>
          </a-card>
        </a-space>
      </div>
    </div>
</template>
<script>
import { mapGetters, mapActions, mapState, mapMutations } from "vuex";
import { isString } from "../store/utils.js";
import { sortObj } from "../store/utils";
//TOP 显示优化：判断head是否是observable，是否能作为head添加
//TODO 剪枝，将没有用到的分支删除
//TODO 显示优化：状态called callable observer
//TODO 显示优化：在arg中被引用后下高亮一会。

export default {
  name: "Observer",
  data() {
    return {
      tagStyle: {
        "-": {
          background: "#FFC329",
        },
        "parse error": {
          background: "red",
        },
      },
    };
  },

  props: {
    msg: String,
  },
  computed: {
    ...mapGetters("observers", ["allObserver", "breifTitleByUUID"]),
    ...mapState("relations", { allRelations: "data" }),
    ...mapGetters(["repr"]),
  },
  methods: {
    sortObj:sortObj,
    ...mapMutations("observers", ["deleteObservers", "editArgInObservers"]),
    ...mapMutations("relations", ["addRelation", "addRelationOn"]),
    ...mapMutations("views", ["flushViews"]),
    viewValue(item) {
      if (item == null || item == undefined) {
        return "-";
      } else if (isString(item)) {
        if (item[0] == "@") {
          return this.repr(item);
        }
      } else if (item instanceof Array) {
        let line = "[";
        for (let index in item) {
          // console.log("list loop", item[index]);
          line = line + item[index] + ",";
        }
        line = line + "]";
        return line;
      } else {
        return item.toString();
      }
    },

    addHead(item) {
      console.log("head item", item);
      let newItem = {
        head: item.uuid,
        name: item.name,
        pipe: [],
        subscribe: null,
        // subscribe_view: null,
      };
      this.addRelation(newItem);
    },

    addPipe(item) {
      this.addRelationOn({ type: "pipe", item: item });
      // this.flushViews(this.allRelations);
    },
    setSubscribe(item) {
      this.addRelationOn({ type: "subscribe", item: item });
      // this.flushViews(this.allRelations);
    },
    deleteItem(item) {
      this.deleteObservers(item);
    },
    tagToTitile(obindex, name) {
      this.editArgInObservers({
        index: obindex,
        argname: name,
        key: "title_tag",
        value: true,
      });
    },
  },
};
</script>

<style scoped>
div.main {
  padding: 10px;
}

div.itemUuid {
  display: block;
  margin-top: 4px;
  /* background-color: black; */
  color: #4289b9;
}
.argitems {
  margin-top: 8px;
  margin-bottom: 8px;
}
.card >>> .ant-card-head {
  background-color: #00704f;
  color: white;
  font-size: x-large;
}
</style>
