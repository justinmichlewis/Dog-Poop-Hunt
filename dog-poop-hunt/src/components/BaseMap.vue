<template>
  <div>
    <div v-if="fullHeight" id="mapContainer" class="map-style-full"></div>
    <div v-else="fullHeight" id="mapContainer" class="map-style-half"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import { useGeolocation } from "@vueuse/core";

const { coords, locatedAt, error, resume, pause } = useGeolocation();

const router = useRouter();

const map = ref();
let userLocation = ref([] as any[]);

const userMarkerIcon = L.icon({
  iconUrl: "/marker-user.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const poopMarkerIcon = L.icon({
  iconUrl: "/poop.png",
  iconSize: [42, 42],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

interface Marker {
  poopId: number;
  latitude: number;
  longitude: number;
  description: string;
  age: number;
}

const props = defineProps({
  fullHeight: Boolean,
  markers: Object,
});

watch(coords, (newCoords) => {
  userLocation.value = [newCoords.latitude, newCoords.longitude];

  loadMapData(props.markers as [Marker], userLocation.value);
});

watch(
  () => [props.markers, userLocation],
  ([newMarkers, newLocation]) => {
    if (
      newMarkers === undefined ||
      newLocation?.value.length === 0 ||
      newLocation?.value === undefined
    ) {
    } else {
      loadMapData(newMarkers as [Marker], newLocation.value);
    }
  }
);

//Catch error for location services
watch(error, (newError) => {
  console.log("New error:", newError);
  // Perform actions based on the error change
});

onMounted(async () => {
  initalizeMap();
});

const loadMapData = (markers: [Marker], userLocation: any) => {
  addMarkers(markers as [Marker]);
  console.log("LMD - User location", userLocation);
  console.log("LMD - new Markers", markers);
  L.marker(userLocation, {
    icon: userMarkerIcon,
  })
    .bindPopup("You are here")
    .addTo(map.value);

  const bounds = findBounds(props.markers as [Marker]);
  console.log("Bounds", bounds);

  //Add user's location to bounds
  bounds.push(userLocation);
  console.log("Bounds with user location", bounds);

  setBounds(bounds);
};

const initalizeMap = () => {
  //Initalize map add add it to div with id mapContainer
  map.value = L.map("mapContainer").setView([40.381093, -118.850076], 5);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map.value);
};

const addMarkers = (markers: [Marker]) => {
  markers.forEach((marker: Marker) => {
    L.marker([marker.latitude, marker.longitude], {
      icon: poopMarkerIcon,
    })
      .addTo(map.value)
      .bindPopup(composePopUpContent(marker));
  });
};

const composePopUpContent = (marker: Marker) => {
  const buttonDetails = document.createElement("button");
  buttonDetails.textContent = "Details";
  buttonDetails.addEventListener("click", () =>
    handlePopUpButtonDetailsClick(marker)
  );

  const buttonNavigate = document.createElement("button");
  buttonNavigate.textContent = "Navigate";
  // buttonNavigate.style.background = "blue";
  buttonNavigate.addEventListener("click", () =>
    handlePopUpButtonNavigateClick(marker)
  );

  const buttonPickUp = document.createElement("button");
  buttonPickUp.textContent = "Pick Up";
  buttonPickUp.addEventListener("click", () =>
    handlePopUpButtonPickUpClick(marker)
  );

  const popupContent = document.createElement("div");
  popupContent.innerHTML = `
          <h3>${marker.description}</h3>
          <p>Age ${marker.age}</p>
        `;
  popupContent.appendChild(buttonDetails);
  popupContent.appendChild(buttonNavigate);
  popupContent.appendChild(buttonPickUp);
  return popupContent;
};

const handlePopUpButtonDetailsClick = (marker: Marker) => {
  console.log(marker);
  router.push({ name: "details", query: marker });
};

const handlePopUpButtonNavigateClick = (marker: Marker) => {
  console.log("Navigate to", marker);
};

const handlePopUpButtonPickUpClick = (marker: Marker) => {
  console.log("Pick up", marker);
};

const findBounds = (markers: [Marker]) => {
  console.log("FB - Markers", markers);
  return markers.map((marker: Marker) => [marker.latitude, marker.longitude]);
};

const setBounds = (bounds: []) => {
  if (bounds.length > 0) {
    let b = new L.LatLngBounds(bounds);
    map.value.fitBounds(b);
  }
};
</script>

<style scoped>
#mapContainer {
  width: 100vw;
}
.map-style-full {
  height: 100vh;
  width: 100vw;
}
.map-style-half {
  height: 50vh;
  width: 100vw;
}
</style>
