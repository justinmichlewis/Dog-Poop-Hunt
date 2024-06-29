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
import type { LatLngExpression } from "leaflet";
import L, { Marker } from "leaflet";
import { useGeolocation } from "@vueuse/core";
import { deletePoop } from "../services/api";
import { getDistance } from "@/services/getdistance";
import { useUserStore } from "@/stores/user";
import "leaflet/dist/leaflet.css";

const { coords, error } = useGeolocation();

const route = useRoute();
const router = useRouter();

const userStore = useUserStore();

const map = ref();
let userLocation = ref([] as any[]);
let poopMarkersOnMap: Marker[] = [];
let userMarkerHistory: Marker | null = null;
let userMarkerPlaced: Boolean = false;
let userMarker: Marker | null = null;

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

const poopMarkerGoldIcon = L.icon({
  iconUrl: "/poop-gold.png",
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
  placedUserId: number;
}

const props = defineProps({
  fullHeight: Boolean,
  markers: Object,
  updateMap: Number,
});

const emit = defineEmits(["map-loaded", "coords"]);

watch(coords, (newCoords) => {
  userLocation.value = [newCoords.latitude, newCoords.longitude];
  userStore.lat = newCoords.latitude;
  userStore.lon = newCoords.longitude;
  emit("coords", userLocation.value);
  //If user marker already exists, update it's position
  if (userMarkerPlaced) {
    userMarker?.setLatLng([newCoords.latitude, newCoords.longitude]);
  } else {
    userMarker = L.marker(
      [newCoords.latitude, newCoords.longitude] as LatLngExpression,
      {
        icon: userMarkerIcon,
      }
    )
      .bindPopup("You are here")
      .addTo(map.value);
    //If user marker is placed, set userMarkerPlaced to true so new marker is not created when coords change
    !userMarkerPlaced ? (userMarkerPlaced = true) : false;
  }

  userMarkerHistory = userMarker;
});

watch(
  () => [props.markers, coords.value, props.updateMap],
  ([newMarkers, newCoords, newUpdateMap]) => {
    if (
      (newMarkers?.length !== 0 && newCoords?.accuracy !== 0) ||
      newUpdateMap
    ) {
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
    if (markerExists(String(marker.poopId))) return;
    if (userStore.id === marker.placedUserId) {
      poopMarkersOnMap.push(
        L.marker([marker.latitude, marker.longitude], {
          icon: poopMarkerGoldIcon,
          id: String(marker.poopId),
        })
          .addTo(map.value)
          .bindPopup(composePopUpContent(marker))
      );
    } else {
      poopMarkersOnMap.push(
        L.marker([marker.latitude, marker.longitude], {
          icon: poopMarkerIcon,
          id: String(marker.poopId),
        })
          .addTo(map.value)
          .bindPopup(composePopUpContent(marker))
      );
    }
  });
};

function markerExists(id: string) {
  return poopMarkersOnMap.some((marker) => marker.options.id === id);
}

const composePopUpContent = (marker: IMarker) => {
  const buttonDetails = document.createElement("button");
  buttonDetails.textContent = "Details";
  buttonDetails.style.marginRight = "10px";
  buttonDetails.addEventListener("click", () =>
    handlePopUpButtonDetailsClick(marker)
  );

  const buttonPickUp = document.createElement("button");
  buttonPickUp.textContent = "Pick Up";
  buttonPickUp.addEventListener("click", () =>
    handlePopUpButtonPickUpClick(marker)
  );

  const popupContent = document.createElement("div");
  popupContent.innerHTML = `
          <h3>${marker.description}</h3>
          <p>Distance: ${getDistance(
            marker.latitude,
            marker.longitude,
            userLocation.value[0],
            userLocation.value[1]
          )} mi
          Age: ${marker.age} 
          Bounty: ${marker.bounty}</p>
        `;
  popupContent.appendChild(buttonDetails);
  popupContent.appendChild(buttonPickUp);

  return popupContent;
};

const handlePopUpButtonDetailsClick = (marker: IMarker) => {
  console.log(marker);
  router.push({ name: "details", query: marker });
};

const handlePopUpButtonPickUpClick = (markerPickedUp: IMarker) => {
  try {
    deletePoop(markerPickedUp.poopId, userStore.id);

    const m = poopMarkersOnMap.find(
      (marker) => marker.options.id === String(markerPickedUp.poopId)
    );
    map.value.removeLayer(m);
  } catch (error) {
    console.log("Error deleting poop", error);
  }
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

const markPoop = () => {
  console.log("Marking poop");
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
