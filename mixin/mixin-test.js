/**
 * mixin 测试
 */

function applyMixins(target, components) {
    components.forEach(component => {
        Object.getOwnPropertyNames(component.prototype).forEach(name => {
            target.prototype[name] = component.prototype[name]
        })
    })
}

const Human = function (name, height, weight) {

    this.name = name;
    this.height = height;
    this.weight = weight;

}

Human.prototype.talk = function() {
    console.log(`${this.name} is talking`)
}

const MoveComponent = function() {

}

MoveComponent.prototype.walk = function() {
    console.log(`${this.name} is walking`);
}

MoveComponent.prototype.run = function() {
    console.log(`${this.name} is running`);
}


function main() {
    const man = new Human("Mike", 170, 60);
    man.talk()
    applyMixins(Human, [MoveComponent])
    man.walk()
}

main()