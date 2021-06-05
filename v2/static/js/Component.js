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
        this.data = ObservableSlim.create(data, true, () => {
            this.elem.innerHTML = this.render()
        });
        console.log(this.elem)
        this.elem.innerHTML = this.render()
    }

    render() {
        return ``
    }
}
export function access (id){
    return  `document.componentRegistry[${id}]`
}
