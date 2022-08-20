<template>
    <div>
        <span v-for=" ( text,index ) in texts " :key='index'>
            <template v-if="text.type=='text'">{{text.line}} </template>
            <template v-else-if="text.type=='formula'"><VueMathjax :formula="text.line"/></template>
            <template v-else-if="text.type=='br'"><br/> </template>
        </span>
    </div>
</template>

<script lang="ts" setup>
import VueMathjax from 'vue-mathjax-next';

// import {defineProps} from "vue"
const props = defineProps(['text'])
type SpanType = {
    type:string,
    line:string
};
const texts:SpanType[] = [{type:"text",line:""}]
if (props.text) {
    props.text.split('\n').forEach((text:string) => {
        var temp = ""
        var is_formula = false
        // console.log(text)
        var i = 0
        while (i < text.length-1) 
        {
            // console.log(text[i],text[i]=='\\f')
            const peer_char = text[i]+text[i+1]
            // console.log(peer_char)
            if (peer_char == '\\f'&& is_formula) {
                i++
                i++
                temp+=text[i]
                texts.push({type:'formula',line:temp})
                temp = ""
                // i++
            } else if (peer_char=='\\f' && !is_formula) {

                texts.push({type:'text',line:temp})
                i++
                temp = ""
                is_formula = true
            }
            else {
                temp += text[i]
            }
            i++
        }
        texts.push({type:'text',line:temp})
        texts.push({type:'br',line:'br'})
    })
}

// console.log('text',texts);
</script>