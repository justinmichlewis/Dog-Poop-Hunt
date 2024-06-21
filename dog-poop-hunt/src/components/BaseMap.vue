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

const route = useRoute();
const router = useRouter();

const map = ref();
let userLocation = ref([] as any[]);
let updateMap = ref(false);

const userMarkerIcon = L.icon({
  iconUrl: "/marker-user.png",
  iconSize: [32, 32],
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

watch(
  () => [props.markers, userLocation],
  ([newMarkers, newLocation]) => {
    console.log("PropsMarkers", props.markers);
    console.log("New markers", newMarkers);
    console.log("New location1", newLocation.value);
    if (
      (newMarkers === undefined ||
        newLocation?.value.length === 0 ||
        newLocation?.value === undefined) &&
      !updateMap.value
    ) {
      console.log(
        "No markers or location",
        newMarkers,
        newLocation?.value,
        newLocation?.value.length,
        updateMap.value
      );
    } else {
      console.log("Updating map");
      console.log(
        "Passed IF",
        newMarkers,
        newLocation?.value,
        newLocation?.value.length,
        updateMap.value
      );
      addMarkers(newMarkers as [Marker]);

      L.marker(newLocation?.value, {
        icon: userMarkerIcon,
      })
        .bindPopup("You are here")
        .addTo(map.value);

      const bounds = findBounds(props.markers as [Marker]);

      //Add user's location to bounds
      bounds.push(newLocation?.value);

      setBounds(bounds);
    }
  }
);

watch(userLocation, (newLocation) => {
  console.log("New location2", newLocation.value);
  if (updateMap.value) {
    addMarkers(props.markers as [Marker]);

    L.marker(userLocation.value, {
      icon: userMarkerIcon,
    })
      .bindPopup("You are here")
      .addTo(map.value);

    const bounds = findBounds(props.markers as [Marker]);

    //Add user's location to bounds
    bounds.push(userLocation.value);

    setBounds(bounds);
  }
  // You can perform any actions here based on the change
});

onMounted(async () => {
  console.log(route.name);
  route.name === "details"
    ? (updateMap.value = true)
    : (updateMap.value = false);
  initalizeMap();
  await getLocation().then((location) => {
    userLocation.value = location;
  });
});

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
    L.marker([marker.latitude, marker.longitude])
      .addTo(map.value)
      .bindPopup(composePopUpContent(marker));
  });
};

const composePopUpContent = (marker: Marker) => {
  const button = document.createElement("button");
  button.textContent = "Details";
  button.addEventListener("click", () => handlePopUpButtonClick(marker));

  const popupContent = document.createElement("div");
  popupContent.innerHTML = `
          <h3>${marker.description}</h3>
          <p>Age ${marker.age}</p>
        `;
  popupContent.appendChild(button);
  return popupContent;
};

const handlePopUpButtonClick = (marker: Marker) => {
  console.log(marker);
  router.push({ name: "details", query: marker });
};

const findBounds = (markers: [Marker]) => {
  return markers.map((marker: Marker) => [marker.latitude, marker.longitude]);
};

const setBounds = (bounds: []) => {
  if (bounds.length > 0) {
    let b = new L.LatLngBounds(bounds);
    map.value.fitBounds(b);
  }
};

const getCurrentPosition = async () => {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject);
  });
};
const getLocation = async () => {
  try {
    return await getCurrentPosition().then((position: any) => {
      return [position.coords.latitude, position.coords.longitude];
    });
  } catch (error) {
    console.error(error);
    return [0, 0];
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
