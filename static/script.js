let page = 1;

const grid = document.getElementById("grid");
const pageNo = document.getElementById("pageNo");

function createGrid() {
    grid.innerHTML = "";
    for (let i = 0; i < 100; i++) {
        const cell = document.createElement("div");
        cell.className = "cell";
        grid.appendChild(cell);
    }
}

async function loadAds() {
    createGrid();

    const res = await fetch('/get_ads/' + page);
    const ads = await res.json();

    const cells = document.getElementsByClassName("cell");

    ads.forEach(ad => {
        const img = document.createElement("img");
        img.src = "/" + ad[0];
        img.onclick = () => window.open(ad[1], "_blank");
        cells[ad[2]].appendChild(img);
    });

    pageNo.innerText = "Grid Page: " + page;
}

document.getElementById("adForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let urlInput = this.querySelector('input[name="url"]');

    if (!urlInput.value.startsWith("http")) {
        urlInput.value = "https://" + urlInput.value;
    }

    const formData = new FormData(this);

    await fetch('/add_ad', {
        method: 'POST',
        body: formData
    });

    this.reset();
    loadAds();
});

function nextPage() {
    page++;
    loadAds();
}

function prevPage() {
    if (page > 1) {
        page--;
        loadAds();
    }
}

loadAds();
