const THRESHOLD = 300;

function timeAgo(ts) {
    if (!ts) return "never";
    const sec = Math.floor(Date.now() / 1000) - ts;
    if (sec < 60) return sec + " seconds ago";
    if (sec < 3600) return Math.floor(sec / 60) + " minutes ago";
    if (sec < 86400) return Math.floor(sec / 3600) + " hours ago";
    return Math.floor(sec / 86400) + " days ago";
}

function fetchData() {
    fetch('/data')
        .then(res => res.json())
        .then(data => {
            document.getElementById('temp').innerText = data.temp;
            document.getElementById('moist').innerText = data.moist;

            const status = document.getElementById('status');
            const lastEl = document.getElementById('last_watered');

            lastEl.innerText = 'Last watered: ' + (data.last_watered ? timeAgo(data.last_watered) : 'never');

            if (data.moist < THRESHOLD) {
                status.innerText = 'Last watered ' + (data.last_watered ? timeAgo(data.last_watered) : 'never');
                status.className = "alert";

                if (!window.alertShown) {
                    alert("Your plant needs water!");
                    window.alertShown = true;
                }
            } else {
                status.innerText = "✅ Plant is healthy";
                status.className = "good";
                window.alertShown = false;
            }
        });
}

setInterval(fetchData, 1000);
