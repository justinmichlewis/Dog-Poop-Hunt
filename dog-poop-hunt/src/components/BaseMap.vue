<template>
  <div>
    <div v-if="fullHeight" id="mapContainer" class="map-style-full"></div>
    <div v-else="fullHeight" id="mapContainer" class="map-style-half"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import "leaflet/dist/leaflet.css";
import type { LatLngExpression } from "leaflet";
import L, { Marker } from "leaflet";

import { useGeolocation } from "@vueuse/core";

const { coords, locatedAt, error, resume, pause } = useGeolocation();

const route = useRoute();
const router = useRouter();

const map = ref();
let userLocation = ref([] as any[]);
let userMarkerHistory: Marker | null = null;
let markersOnMap: Marker[] = [];

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

interface IMarker {
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

const emit = defineEmits(["map-loaded"]);

watch(coords, (newCoords) => {
  userLocation.value = [newCoords.latitude, newCoords.longitude];

  //Remove previous user marker if exists
  if (userMarkerHistory !== null) {
    map.value.removeLayer(userMarkerHistory);
  }
  let userMarker = L.marker(
    [newCoords.latitude, newCoords.longitude] as LatLngExpression,
    {
      icon: userMarkerIcon,
    }
  )
    .bindPopup("You are here")
    .addTo(map.value);

  userMarkerHistory = userMarker;
});

watch(
  () => [props.markers, coords.value],
  ([newMarkers, newCoords], [oldMarkers, oldCoords]) => {
    if (newMarkers?.length !== 0 && newCoords?.accuracy !== 0) {
      console.log("ALL DATA LOADED", newMarkers, newCoords);

      addMarkers(newMarkers as [IMarker]);

      const bounds = findBounds(props.markers as [IMarker]);

      //Add user's location to bounds
      bounds.push(userLocation.value);

      setBounds(bounds);
      emit("map-loaded", true);
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
  //If coming from details page, markers are already loaded, so add markers to the map on mount, else watcher will pick up markers when loaded from map page
  if (router.currentRoute.value.name === "details") {
    addMarkers([route.query as unknown as IMarker]);
  }
});

const initalizeMap = () => {
  //Initalize map add add it to div with id mapContainer
  map.value = L.map("mapContainer").setView([40.381093, -118.850076], 5);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map.value);
};

const addMarkers = (markers: [IMarker]) => {
  markers.forEach((marker: IMarker) => {
    console.log("EXISTS,", markerExists(String(marker.poopId)));
    if (markerExists(String(marker.poopId))) return;
    markersOnMap.push(
      L.marker([marker.latitude, marker.longitude], {
        icon: poopMarkerIcon,
        id: String(marker.poopId),
      })
        .addTo(map.value)
        .bindPopup(composePopUpContent(marker))
    );
  });
};

function markerExists(id: string) {
  return markersOnMap.some((marker) => marker.options.id === id);
}

const composePopUpContent = (marker: IMarker) => {
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

const handlePopUpButtonDetailsClick = (marker: IMarker) => {
  console.log(marker);
  router.push({ name: "details", query: marker });
};

const handlePopUpButtonNavigateClick = (marker: IMarker) => {
  console.log("Navigate to", marker);
};

const handlePopUpButtonPickUpClick = (marker: IMarker) => {
  console.log("Pick up", marker);
};

const findBounds = (markers: [IMarker]) => {
  return markers.map((marker: IMarker) => [marker.latitude, marker.longitude]);
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
