/**
 * 监听属性变化
 * 使用代理对象拦截对象set操作，打印变化的key和value，同时打印调用栈
 * 支持终端打印和写入文件，也可以自定义回调
 * observe：生成监听的代理对象
 * getRaw: 获取源对象
 */

const fs = require("fs");
const addr = "D:\\MyWork2\\tracelog.txt";

var cache = []  //用于消除字符串序列化时的循环引用
function clearLoop(key, value){
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

function writeToFile(...args){
    const myDate = new Date();
    fs.appendFileSync(addr, "["+myDate.toLocaleString()+"]"+": ", () => {});
    for (let count = 0; count < args.length; count ++) {
        fs.appendFileSync(addr, JSON.stringify(args[count], clearLoop, 2) + " ", () => {});
    }
    fs.appendFileSync(addr, "\n", () => {});
    cache = [];
    TraceMsg();
}

function GetStack() {
    let err = new Error;
    err.name = 'Trace';
    let stack = err.stack.split("\n    ");
    return stack;
}

function TraceMsg() {
    let traceText = GetStack();
    const myDate = new Date();
    fs.appendFileSync(addr, "["+myDate.toLocaleString()+"]"+":"+"========================================="+"\n", () => {});
    traceText.forEach(function(element){
        fs.appendFileSync(addr, JSON.stringify(element), () => {
            console.log(element);
        });
        fs.appendFileSync(addr, "\n", () => {});
    })
}

function defaultCB(...args) {
    console.log("=====================================")
    console.log(args);
    console.trace();
    console.log("=====================================")
}

// =========================================================================

function observe(obj, callback=defaultCB) {
    return new Proxy(obj, {
        set(target, key, value, receiver) {
            const result = Reflect.set(target, key, value, receiver);
            callback(key, value);
            return result;
        },
        get(target, key, receiver){
            if (key == "RAW") {
                return target;
            }
            return Reflect.get(target, key, receiver);
        }
    })
}
exports.observe = observe;

function getRaw(proxyObj) {
    const raw = proxyObj["RAW"];
    if (!raw) {
        return proxyObj;
    }
    return getRaw(raw);
}
exports.getRaw = getRaw;
