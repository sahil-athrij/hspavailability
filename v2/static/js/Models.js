class MarkerObject extends ModelObject {

    id;
    Phone;
    size;
    financial_rating;
    avg_cost;
    covid_rating;
    beds_available;
    care_rating;
    oxygen_rating;
    ventilator_availability;
    oxygen_availability;
    icu_availability;
    lat;
    lng;
    datef;
    added_by_id;
    images;
    name;
    fields;
    excluded_fields;

    constructor(data, baseUrl) {

        super(data, baseUrl);
        this.fields = ["id", "Phone", "size", "financial_rating", "avg_cost", "covid_rating", "beds_available", "care_rating",
            "oxygen_rating", "ventilator_availability", "oxygen_availability", "icu_availability", "lat", "lng", "images",
            "display_address","name", "datef"]
        this.excluded_fields = ['image', 'added_by_id']
        this.getData()

    }

}

/**
 * @tutorial
 * usage of Models Class
 * inherit  make your ModelObject class as the marker defined above,
 * give the Model Class the Base location of the API view of the model , then give the Object Class
 */

Marker = new Model('/marker/', MarkerObject)

/**
 * usage of get , gets the model , this case the marker and you can use the data like this
 */

Marker.get(id = 5, kwargs = {}).then(function (marker) {
    console.log(marker)
})

/**
 * usage of filter , filter the model , this case the marker and you can use the data like this
 * put your filter inside filter
 */
Marker.filter(kwargs = {oxygen_availability__gte: 0}).then(function (markerList) {

})

/**
 * Similarly create exists as well as able to edit the data as well
 */
Marker.get(id = 5).then(function (marker) {
    console.log(marker)
    console.log(marker.id)
    console.log(marker.name)
    marker.size = 1
    marker.save()
})

class ReviewObject extends ModelObject {
    id;
    marker_id;
    financial_rating;
    avg_cost;
    covid_rating;
    care_rating;
    oxygen_rating;
    beds_available;
    ventilator_availability;
    oxygen_availability;
    icu_availability;
    comment;
    written_by_id;
    datef;
    day;
    images;
    fields;
    excluded_fields;
    Phone;


    constructor(data, baseUrl) {

        super(data, baseUrl);
        this.fields = ["id", "marker", "financial_rating", "avg_cost", "covid_rating", "beds_available", "care_rating",
            "oxygen_rating", "ventilator_availability", "oxygen_availability", "icu_availability", "comment", "datef",
            "images", "day",]
        this.excluded_fields = ['image', 'written_by_id']
        this.getData()

    }
}

Review = new Model('/review/', ReviewObject)

class susObject extends ModelObject {
    id;
    marker;
    comment;
    created_by;
    datef;

    constructor(data, baseUrl) {
        super(data, baseUrl);
        this.fields = ["id", "marker", "comment", "created_by", "datef"]
        this.getData()
    }
}

Sus = new Model('/suspicious/', susObject)