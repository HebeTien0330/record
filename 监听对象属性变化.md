# 2024.03.02

    当代码量逐渐增多时，模块与模块间、对象与对象间的关系会变得非常复杂，
    因此很有可能会出现对象的属性在某个时刻被修改，却难以定位修改的代码位置。
    如何快速定位对象的属性何时被修改？这是一个值得思考的问题。

# Python

    在Python的对象中存在一个__setattr__魔法方法，
    当给一个对象的属性赋值时，实质上是通过这个魔法方法将变量值以键值对形式存放在__dict__中，
    因此我们可以修改需要监听的类的__setattr__方法，从而实现监控对象属性的赋值操作

```python
class Test:

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if check(key):      # check是对key的相关检查条件
            print(f"object {self} attribute {key} has been changed")
```

# javascript

    js存在一个叫代理对象的东西，用户可以通过代理对象间接地操作原始对象的底层，如对象属性的get和set等;
    具体实现需要了解js对象的：属性描述符、Proxy和Reflect，有空再去细究一下
    之前自己写了一个监听对象属性变化的脚本，需要注意：
    1、通过new Proxy对需要监听的对象建立新的代理对象
    2、通过在代理对象中构建一个RAW字段，指向原始对象，当取消监听时可以由此将代理对象恢复成原始对象

```javascript
function observe(obj, callback=cb) {
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
```

    完整脚本：observation/observation.js
