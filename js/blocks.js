$("#action-bar").on("click", "#blocks-reload, #block-sort", async event => {
    if ($(event.target).id === "blocks-reload") {
        $("#blocks").load(window.location.href + " #blocks");
    } else if ($(event.target).id === "blocks-sort") {
        await change_sort();
    }
});


let paused = true
let t = setInterval(() => {
    if (!paused) {
        $("#blocks").load(window.location.href + " #blocks");
    }
}, 10000);


$("#auto-reload").change(function() {
    paused = !$(this).is(":checked");
})


$(".block").on("click", ".remove-block, .send-pulse, .toggle", async event => {
    const block = $(event.target).closest(".block")[0];

    if ($(event.target).hasClass("remove-block")) {
        await remove_block(block.dataset.id);
    } else if ($(event.target).hasClass("send-pulse")) {
        await send_signal(block.dataset.id);
    } else if ($(event.target).hasClass("toggle")) {
        await send_signal(block.dataset.id, true);
    }
});


async function remove_block(block_id) {
    fetch("/blocks/remove",
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({block_id: block_id})
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                $("#blocks").load(window.location.href + " #blocks");
            }
        });
}


async function send_signal(id, persist=false) {
    fetch("/blocks/signal",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                block_id: id,
                persist: persist
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data) {
                alert("Something went wrong!");
            }
        });
}


async function change_sort(){
    const blockList = document.getElementById("blocks");
    const blocks = Array.from(blockList.children);

    const sortOption = document.getElementById("block-sort").value;

    switch (sortOption) {
        case "block_id": {
            blocks.sort((a, b) => {
                const idA = parseInt(a.id.split("-")[1]);
                const idB = parseInt(b.id.split("-")[1]);
                return idA - idB;
            });
            break;
        }
        case "owner": {
            blocks.sort((a, b) => {
                const ownerA = parseInt(a.getAttribute("data-owner"));
                const ownerB = parseInt(b.getAttribute("data-owner"));
                return ownerA - ownerB;
            });
            break;
        }
        default: {
            alert("There was an error: invalid sorting option");
        }
    }

    blocks.forEach(block => {
        blockList.appendChild(block);
    });
}