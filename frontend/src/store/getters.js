const md5 = require('md5');
import { isString } from "../store/utils.js";

const getters = {
    allElements: (state) => state.elements,

    allRefable:(state)=>{
      let res = []
      for (let uuid in state.observers.data){
        res.push(uuid)
      }
      for (let uuid in state.relations.data){
        res.push(uuid)
      }
      for (let uuid in state.views.parameters){
        res.push(uuid)
      }
      for (let root in state.elements){
        for (let fname in state.elements[root]){
          res.push(root+'.'+fname)
        }
      }
      return res
    },
    repr:(state)=>(uuid)=>{
      if (isString(uuid) ){
        if (uuid.includes('.')){
          return uuid
        }
        if (uuid[0]=="@"){
          uuid = uuid.slice(1)
        }
      }
      if (Object.keys(state.observers.data).includes(uuid)){
        var item = state.observers.data[uuid]
        var op_head = ""
        if (item.op){
          op_head =  item.op + ":"
        }
        
        if (item.type=="lambda"){
          let value = item.args.args.value
          if (value){
            value = value.join(",")
          }
          return op_head + "λ ("+ value +")=>" + item.line 
        }
        else if (item.type != "func") {
          return op_head + item.name;
        }
        var titles = [];
        for (var k in item.args) {
          let { type, name, value, title_tag } = item.args[k];
          var title;
          if (title_tag) {
            if (type == "list") {
              title = `${name}=${value.length}`;
            } 
            else if (isString(value) && value[0]=="@" )
              {
                let ref = state.observers.data[value.slice(1)]
                if (ref){
                  title = `${name}=${ref.name}`
                }else{
                  title = `${name}=${value}`
                }
              } 
            else {
              title = `${name}=${value}`;
            }
            titles.push(title);
          }
        }
        if (titles){
          return op_head + item.name+":"+titles.join("")
        }else{
          return op_head + item.name
        }
      }
      else if (Object.keys(state.views.parameters).includes(uuid)){
        item = state.views.parameters[uuid]
        return uuid
      }
      else if (Object.keys(state.relations.data).includes(uuid)){
        item = state.relations.data[uuid]
        return uuid
      }
      else{
        return "parse error"
      }
    },


    briefKeys:(state) => {
      let res = []
      for (let uuid in state.observers.data){
        res.push(uuid.slice(0,5))
      }
      for (let root in state.elements){
        for (let fname in state.elements[root]){
          res.push(root+'.'+fname)
        }
      }
      return res
    },
  };

  export default getters;