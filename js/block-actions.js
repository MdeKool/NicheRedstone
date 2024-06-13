async function add_block() {
    fetch("/blocks/add",
        {
            method: "PUT"
        })
        .then(response => response.text())
        .then(html => {
            const block_list = document.getElementById("blocks");
            block_list.insertAdjacentHTML("beforeend", html);
        });
}


async function remove_block(blockId) {
    // let blockId = document.getElementById("remove-block-id").value;
    fetch("/blocks/remove",
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({blockId: blockId})
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById(`block-${blockId}`).remove();
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
    }

    blocks.forEach(block => {
        blockList.appendChild(block);
    });
}