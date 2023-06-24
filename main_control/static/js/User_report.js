const btn1 = document.getElementById('health_btn');

btn1.addEventListener('click', function () {
    const healthStatusImg = document.getElementById("health_");
    const date_inp = document.getElementById("date_input1");
    console.log(date_inp);
    const url = "/api/get_health_status/" + date_inp.value;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const newUrl = data.new_url;
            healthStatusImg.setAttribute("src", newUrl);
        })
        .catch(error => {
            console.error(error);
        });
})


const btn2 = document.getElementById("ecg_img_btn");
btn2.addEventListener('click', function () {
    const date_inp = document.getElementById('date_input2');
    const time_inp = document.getElementById("time-input");
    const ecg_image = document.getElementById('ecg_');
    const url = "/api/get_ecg_image/" + date_inp.value + "/" + time_inp.value;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const newUrl = data.ecg_image;
            ecg_image.setAttribute("src", newUrl);
            const datetime = data.datetime;
            const heartrate = data.heart_beat;
            const heartbeatElem = document.querySelector('.ecg_heartbeat h4');
            heartbeatElem.textContent = `Heartbeat: ${heartrate}`;
            const datimele = document.querySelector(".date_time");
            datimele.textContent = `Date and Time:${datetime}`;
        })

})

let checkbox_state = 0;

document.getElementById("go_live").addEventListener('change', function () {
    checkbox_state = 1 - checkbox_state;
})

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

document.getElementById("go_live_btn").addEventListener('click', async function () {
    while (checkbox_state) {
        console.log("1 Iteration done")
        let currentDate = new Date();
        let year = currentDate.getFullYear().toString();
        let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
        let day = currentDate.getDate().toString().padStart(2, '0');
        let hour = currentDate.getHours().toString().padStart(2, '0');
        let minute = currentDate.getMinutes().toString().padStart(2, '0');
        const date_inp = year + '-' + month + '-' + day;
        const time_inp = hour + ':' + minute;
        const ecg_image = document.getElementById('ecg_');
        const url = "/api/get_ecg_image/" + date_inp + "/" + time_inp;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const newUrl = data.ecg_image;
                ecg_image.setAttribute("src", newUrl);
                const datetime = data.datetime;
                const heartrate = data.heart_beat;
                const heartbeatElem = document.querySelector('.ecg_heartbeat h4');
                heartbeatElem.textContent = `Heartbeat: ${heartrate}`;
                const datimele = document.querySelector(".date_time");
                datimele.textContent = `Date and Time:${datetime}`;
            })
        await sleep(20000);

    }
})


// The Leaflet map Object
var map = L.map('map').setView([29.86340, 77.89744], 16);

// The API Key provided is restricted to JSFiddle website
// Get your own API Key on https://myprojects.geoapify.com
var myAPIKey = "1d990312698943509820797edb76395f";

// Retina displays require different mat tiles quality
var isRetina = L.Browser.retina;

var baseUrl = "https://maps.geoapify.com/v1/tile/osm-bright/{z}/{x}/{y}.png?apiKey={apiKey}";
var retinaUrl = "https://maps.geoapify.com/v1/tile/osm-bright/{z}/{x}/{y}@2x.png?apiKey={apiKey}";

// Add map tiles layer. Set 20 as the maximal zoom and provide map data attribution.
L.tileLayer(isRetina ? retinaUrl : baseUrl, {
    attribution: 'Powered by <a href="https://www.geoapify.com/" target="_blank">Geoapify</a> | <a href="https://openmaptiles.org/" rel="nofollow" target="_blank">© OpenMapTiles</a> <a href="https://www.openstreetmap.org/copyright" rel="nofollow" target="_blank">© OpenStreetMap</a> contributors',
    apiKey: myAPIKey,
    maxZoom: 20,
    id: 'osm-bright',
}).addTo(map);
L.marker([29.86340, 77.89744]).addTo(map)
    .bindPopup('Live Location')
    .openPopup();
