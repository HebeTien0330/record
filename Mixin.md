# 2024.03.02

# mixin混入

    “除了传统的面向对象继承方式，还流行一种通过可重用组件创建类的方式，就是联合另一个简单类的代码。 
    你可能在Scala等语言里对mixins及其特性已经很熟悉了，但它在JavaScript中也是很流行的。”

    以上是TypeScript官方对mixin的介绍，第一次看到是还是有点懵逼的。
    记得当时第一次接触typescript，看到满屏的interface却找不到对应实现的方法，非常懵逼。
    组长跟我说了解下mixin，于是就要看到了上面那段官方文档。

    直到现在写了大半年typescript，多多少少对mixin有点理解和感悟，但估计也只是皮毛罢了。

# ts/js的面向对象

    刚开始接触ts/js的面向对象时，发现好像跟Python的面向对象有点不一样。
    ts/js的继承是基于原型链的，当子类需要调用父类方法事，会顺着原型链逐步往上查找，直到原型链最顶端。
    因此ts/js是没有多继承的。
    那如果需要实现使用多个父类的不同方法，该怎么办呢？mixin该派上用场了。

# ts/js的对象方法

    与Python不同，ts/js在对象中的方法更像是一个个作为属性的代码块，代码块所属对象的this指针可以随意变更，
    因此利用这个性质，再结合组合模式的思想，可以通过编写不同组件，
    当某个对象需要某个组件的方法时，将这个对象的方法一一复制到目标对象上，并将this指针指向目标对象，从而实现类似多继承的效果

```javascript
function applyMixins(target, components) {
    components.forEach(component => {
        Object.getOwnPropertyNames(component.prototype).forEach(name => {
            target.prototype[name] = component.prototype[name]
        })
    })
}
```
    示例代码：mixin\mixim-test.js
