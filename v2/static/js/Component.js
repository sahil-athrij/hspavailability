document.componentRegistry = {};
document.nextId = 0;

export class Component {
    constructor(component = 'Component', data = {}) {
        this._id = ++document.nextId;
        document.componentRegistry[this._id] = this;
        this.selector = component
        this.elem = document.querySelector(this.selector);

        for (var att, i = 0, atts = this.elem.attributes, n = atts.length; i < n; i++) {
            att = atts[i];
            data[att.nodeName] = att.nodeValue
        }


        this.data = ObservableSlim.create(data, true, (changes) => {
            console.log(changes)
            if (changes[0].type !== 'add') {
                this.elem.innerHTML = this.render()
            }
            if (changes[0].type === 'add') {
                console.log('hello')
                var wrapper = document.createElement('update');
                wrapper.innerHTML = this.update();
                this.elem.appendChild(wrapper)
            }
            this.final()
        });
        this.elem.innerHTML = this.render()
    }

    update() {
        return ``
    }

    render() {
        return ``
    }

    final() {
    }
}

export function access(id) {
    return `document.componentRegistry[${id}]`
}
