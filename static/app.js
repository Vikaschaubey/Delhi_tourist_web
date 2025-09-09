let map, marker;
let rotating = true;
let rotateRAF = null;

// Initialize Map
function initMap() {
  map = new mappls.Map("map", {
    center: [28.59033, 77.22712],
    zoom: 10,
    pitch: 40,
    bearing: 0
  });

  // Start rotation
  function rotateCamera(ts) {
    if (!rotating) return;
    map.setBearing((ts / 100) % 360);
    rotateRAF = requestAnimationFrame(rotateCamera);
  }

  map.on("load", () => rotateCamera(0));
}

// Show marker from list
function showMarker(lat, lng, eloc, name, build, build_name, metro_station) {
  const resultBox = document.getElementById("result");

  // Stop rotation
  rotating = false;
  if (rotateRAF) cancelAnimationFrame(rotateRAF);

  // Remove old marker
  if (marker) marker.remove();

  // Add new marker
  marker = new mappls.Marker({
    map,
    position: { lat, lng },
    icon_url: "https://apis.mapmyindia.com/map_v3/1.png"
  });

  // Fly to new location
  map.flyTo({
    center: [lng, lat],
    zoom: 16,
    pitch: 45,
    bearing: 0,
    speed: 0.9,
    curve: 1.2
  });

  // Show info in right panel
  resultBox.innerHTML = `
    <b>${name}</b><br>
    <strong>Latitude:</strong> ${lat}<br>
    <strong>Longitude:</strong> ${lng}<br>
    <strong>eLoc:</strong> ${eloc}<br>
    <strong>Manufactured Date:</strong> ${build}<br>
    <strong>Built By:</strong> ${build_name}<br>
    <strong>Nearest Metro Station:</strong> ${metro_station}
    
  `;

  // Resume rotation after 3s
  setTimeout(() => {
    rotating = true;
    document.getElementById("toggleRotationBtn").innerText = "⏸ Pause Rotation";
    rotateRAF = requestAnimationFrame(function step(ts) {
      if (!rotating) return;
      map.setBearing((ts / 100) % 360);
      rotateRAF = requestAnimationFrame(step);
    });
  }, 3000);
}

// Toggle rotation
function toggleRotation() {
  const btn = document.getElementById("toggleRotationBtn");
  rotating = !rotating;

  if (rotating) {
    btn.innerText = "⏸ Pause Rotation";
    rotateRAF = requestAnimationFrame(function step(ts) {
      if (!rotating) return;
      map.setBearing((ts / 100) % 360);
      rotateRAF = requestAnimationFrame(step);
    });
  } else {
    btn.innerText = "▶ Continue Rotation";
    if (rotateRAF) cancelAnimationFrame(rotateRAF);
  }
}

// Spacebar shortcut
document.addEventListener("keydown", function(e) {
  if (e.code === "Space") {
    e.preventDefault();
    toggleRotation();
  }
});

document.getElementById("touristForm").addEventListener("submit", function(e){
    // Example: You can add custom validation here
    const lat = parseFloat(this.latitude.value);
    const lon = parseFloat(this.longitude.value);

    if(lat < -90 || lat > 90 || lon < -180 || lon > 180){
        e.preventDefault();
        alert("Please enter valid latitude and longitude values.");
    }
});

document.getElementById("deleteForm").addEventListener("submit", function(e){
    const elocValue = this.eloc.value.trim();
    if(elocValue === ""){
        e.preventDefault();
        alert("Please enter an ELOC value to delete.");
    }
});

