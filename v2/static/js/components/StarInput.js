/** @jsx jsxToDom */
import {access, Component} from "../Component.js";

export class StarInput extends Component {
    extra_class;

    constructor(component, data = {}) {
        super(component, data)
    }

    setValue(value) {
        this.data.value = value
    }


    render() {
        return `
        <div class="col my-2  ${this.data.col}">
            <label for="{{ name }}" class="">${this.data.label}
            <a data-toggle="popover"
               href="javascript:void(0)"
               data-bs-trigger="focus"
               title="${this.data.label}"
               data-bs-content="${this.data.content}">
                <i class="fa fa-info-circle text-dark" aria-hidden="true"></i>
            </a>
            </label>
            <div class="star-rating col">
        
                <div id="${this.data.id}" class="form-check-inline">
                    <div class="rate ${this.data.extra_class}">
                        
                        <output class="ot mx-2" id="${this.data.id}_output">
                            ${this.data.value}
                        </output>
                        ${[5, 4, 3, 2, 1].map((i) => {
            return `
                            <input type="radio" 
                                id="${this.data.id}${i}" 
                                value="${i}" name="${this.data.id}"
                                ${parseInt(this.data.value) === i ? 'checked' : ''}
                                ${this.data.disabled}
                                oninput="${access(this._id)}.setValue(this.value)">
                            <label for="${this.data.id}${i}"></label>`
        }).join('')}
                    </div>
                </div>
            </div>
        </div>
        `
    }

    final() {
        $('[data-toggle="popover"]').popover();
    }
}

