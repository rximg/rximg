import { describe, test, expect } from "@jest/globals";
import { RXArg, RXFunction,ChoiceArg } from "./RxLibrary";

const init_im_show = { "args": 
    { "mat": { 
        "index": 0, 
        "kind": "POSITIONAL_OR_KEYWORD", 
        "name": "mat", 
        "type": "NDArray", 
        "value": null } }, 
    "from": "custom", 
    "name": "imshow", 
    "returnType": "Any", 
    "type": "callable" }

const im_show_function = {
    "args": {
      "mat": {
        "index": 0,
        "kind": "POSITIONAL_OR_KEYWORD",
        "name": "mat",
        "type": "NDArray",
        "value": null
      }
    },
    "from": "custom",
    "name": "imshow",
    "op": "map",
    "output": [],
    "type": "func",
    "uuid": "655a88619c120280de0d1f2b7430522c"
  }

describe("rxarg init", () => {
    test("rxarg init be 1", () => {
        const rxarg = new RXArg(0, 'str', "",)
        console.log("rxarg toString", rxarg.toString())
        expect(rxarg.toString()).toBe("");
        rxarg.value.value = 2
        expect(rxarg.toString()).toBe("2");
    });

    test("rxarg init be None", () => {
      const rxarg = new RXArg(0, '',)
      console.log("rxarg toString", rxarg.toString())
      expect(rxarg.toString()).toBe("null");
      rxarg.value.value = 2
      expect(rxarg.toString()).toBe("2");
      rxarg.value.value = null
      expect(rxarg.toString()).toBe("null");
      
  });
});


describe("rxarg init", () => {

});

describe("rxfunction init", () => {
    test("rxfunction init and assign", () => {
        const rxfunction = new RXFunction(init_im_show)
        console.log("rxfunction toString", rxfunction.toString(),rxfunction)
        expect(rxfunction.toString()).toBe("imshow(mat=null,)");
        // rxfunction.fromjson(im_show_function)
        const rxfunction2 = new RXFunction(im_show_function)
        console.log("rxfunction toString", rxfunction)
        expect(rxfunction2.toString()).toBe("map:imshow(mat=null,)");
        rxfunction2.args.mat.value.value = "abcd"
        expect(rxfunction2.toString()).toBe("map:imshow(mat=abcd,)");
        console.log("rxfunction tojson", rxfunction2.tojson())
    });
})


const choice_data = {
    "choices": {
      "THRESH_BINARY": 0,
      "THRESH_BINARY_INV": 1,
      "THRESH_MASK": 7,
      "THRESH_OTSU": 8,
      "THRESH_TOZERO": 3,
      "THRESH_TOZERO_INV": 4,
      "THRESH_TRIANGLE": 16,
      "THRESH_TRUNC": 2,
      "default": 0
    },
    "index": 3,
    "kind": "POSITIONAL_OR_KEYWORD",
    "type": "choices",
    "value": 0
  }

describe("rxarg choices init", () => {
    test("rxarg int choices init", () => {
        let { choices, index, kind,  type, value } = choice_data
        const rxarg = new ChoiceArg(index,choices,kind)
        console.log("rxarg toString", rxarg)
        expect(rxarg.toString()).toBe("THRESH_BINARY");
        rxarg.value.value = 1
        expect(rxarg.toString()).toBe("THRESH_BINARY_INV");
    });
});