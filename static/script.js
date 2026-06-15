async function fetchMobiles() {

    let minPrice =
        document.getElementById("minPrice").value;

    let maxPrice =
        document.getElementById("maxPrice").value;

    let ram =
        document.getElementById("ram").value;

    let storage =
        document.getElementById("storage").value;

    let url = "/mobiles?";

    if (minPrice)
        url += `min_price=${minPrice}&`;

    if (maxPrice)
        url += `max_price=${maxPrice}&`;

    if (ram)
        url += `ram=${ram}&`;

    if (storage)
        url += `storage=${storage}`;

    let response = await fetch(url);

    let result = await response.json();

    let mobileList =
        document.getElementById("mobileList");

    mobileList.innerHTML = "";

    // No Mobile Found
    if (result.status === "not_found") {

        mobileList.innerHTML = `
            <div class="not-found">

                <h2>
                    No Mobile Found
                </h2>

                <p>
                    No mobile available for this
                    RAM, Storage and Price combination.
                </p>

            </div>
        `;

        return;
    }

    // Display Mobiles
    result.data.forEach(mobile => {

        mobileList.innerHTML += `

            <div class="card">
                        <img
    src="${mobile.image}"
    alt="${mobile.model}"
    class="mobile-img"
>
                <h2>${mobile.model}</h2>

                <p>
                    Price : ₹${mobile.price}
                </p>

                <p>
                    RAM : ${mobile.ram} GB
                </p>

                <p>
                    Storage : ${mobile.storage} GB
                </p>

                <a
                    href="${mobile.link}"
                    target="_blank"
                    class="view-btn"
                >
                    View Product
                </a>
                

            </div>

        `;
    });
}