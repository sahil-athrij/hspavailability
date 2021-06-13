import {Component} from "../Component.js";
import {StarInput} from "./StarInput.js";

class SearchCards extends Component {
    oxy;
    aff;
    con;
    cov;

    constructor(component, data = {}) {
        super(component, data)
        this.oxy = new StarInput(`#oxy${this.data.id}`)
        this.aff = new StarInput(`#aff${this.data.id}`)
        this.con = new StarInput(`#con${this.data.id}`)
        this.cov = new StarInput(`#cov${this.data.id}`)

    }

    render() {
        return `
<div class="card card-left neumorphic_input card-margin bg-grey">
    <img src="/static/images/hospital.svg" class="card-img-top  p-2 p-md-4"/>
    <div class="card-body card-body-left widget-49 bg-white w-100">
        <h5 class="card-title card-title-left" >${this.data.name}</h5>
        <h6 class="card-title card-title-left" >${this.data.display_address}</h6>
        ${
            this.data.Phone === '0000000000' ? '' : `<h6 class="card-title card-title-left" ><a
                href="tel:${this.data.Phone}">${this.data.Phone}</a></h6>`
        }
        
        
        
        <h6 class="card-title card-title-left" >
            <a href="/details/${this.data.id}"
               class=""> ${this.data.comment_count} Reviews</a>
        </h6>
        <div class="widget-49-meeting-points  row">
            <starInput id="oxy${this.data.id}"  class="col-6" label="Oxygen Care" content="Quality Rating for Oxyen Care" disabled="disabled"  value="${this.data.oxygen_rating}"></starInput>
            <starInput id="aff${this.data.id}"  class="col-6" extra_class="financial" label="Affordability" content="Affordability of the hospital .higher is expensive" disabled="disabled" value=${this.data.financial_rating}  ></starInput>
        </div>
        <div class="widget-49-meeting-points  row">
         <starInput id="con${this.data.id}"  class="col-6"  label="Convenience" content="Convenience of Getting Care (higher is Better) the ease with dealing with Administrative" disabled="disabled" value=${this.data.care_rating}></starInput>
         <starInput id="cov${this.data.id}"  class="col-6"  label="Covid Care" content="Quality of Covid Care (higher is better)" disabled="disabled"  value=${this.data.covid_rating}  ></starInput>
        </div>
        <div class="widget-49-meeting-points mt-2 row">
            <div class="col">Average Cost : <span >${this.data.avg_cost}</span> Rs</div>
            <div class="col">Oxygen Availability : <span >${this.data.oxygen_availability}</span> %
            </div>
        </div>
        <div class="widget-49-meeting-points my-2 row">
            <div class="col">Ventilator Availability : <span >${this.data.ventilator_availability}</span> %
            </div>
            <div class="col">ICU Availability : <span>${this.data.icu_availability}</span> %
            </div>
        </div>
        <h6 class="card-title card-title-left" id="{{ id }}title">
            <a href="/details/${this.data.id}?review=true"
               class="text-warning"><i class="fa fa-star"></i> Add Review</a>
        </h6>
         <div class="d-flex d-flex justify-content-between">
           
            <a href="/details/${this.data.id}"  class="btn input-right input-left bg-dark btn-dark">More Info</a>
            <a target="_blank" href="https://www.google.com/maps/search/${this.data.name}/@${this.data.lat},${this.data.lng},19.88z">
                <i class="fa fa-map-marker"></i> Route Map
            </a>
        </div>
       
    </div>
</div>`;
    }
}

export class SearchResultList extends Component {
    superList = [];

    constructor(component, data = {}) {
        super(component, data)


    }

    update() {
        return `${this.data.list.slice(-10).map((marker) => {
            return `<SearchCards class='seachCard${marker.id}'></SearchCards>`
        }).join('')}`

    }

    render() {
        return `${this.data.list.map((marker) => {
            return `<SearchCards class='seachCard${marker.id}'></SearchCards>`
        }).join('')}`
    }

    final() {
        this.superList.push(...this.data.list.slice(-10).map(marker => {
                return new SearchCards(`.seachCard${marker.id}`, {...marker})
            }
        ))
    }
}

