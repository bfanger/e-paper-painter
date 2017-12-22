const loader = require("@std/esm")(module, { esm: "js", cjs: true });
loader("./server.js");
