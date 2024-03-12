var fs = require("fs");
var addr = "D:\\MyWork2\\tracelog.txt";
var myDate = new Date();

var cache = []  //用于消除字符串序列化时的循环引用
function ClearLoop(key, value){
    if (typeof value === 'object' && value !== null) {
        if (cache.indexOf(value) !== -1) {
            // 移除
            return "";
        }
        // 收集所有的值
        cache.push(value);
    }
    return value;
}

function Print(...args){
    fs.appendFileSync(addr, "["+myDate.toLocaleString()+"]"+": ", () => {});
    for (let count = 0; count < args.length; count ++) {
        fs.appendFileSync(addr, JSON.stringify(args[count], ClearLoop, 2) + " ", () => {});
    }
    fs.appendFileSync(addr, "\n", () => {});
    cache = [];
}
exports.Print = Print;

function PrintObj(obj){
    fs.appendFileSync(addr, "["+myDate.toLocaleString()+"]"+": ", () => {});
    fs.appendFileSync(addr, JSON.stringify(obj, ClearLoop, 2), () => {});
    fs.appendFileSync(addr, "\n", () => {});
    cache = [];
}
exports.PrintObj = PrintObj;

function GetStack() {
    let err = new Error;
    err.name = 'Trace';
    let stack = err.stack.split("\n    ");
    return stack;
}

function TraceMsg(){
    let traceText = GetStack();
    fs.appendFileSync(addr, "["+myDate.toLocaleString()+"]"+":"+"========================================="+"\n", () => {});
    traceText.forEach(function(element){
        fs.appendFileSync(addr, JSON.stringify(element), () => {
            console.log(element);
        });
        fs.appendFileSync(addr, "\n", () => {});
    })
}
exports.TraceMsg = TraceMsg;