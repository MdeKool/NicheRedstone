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


async function remove_block(block_id) {
    let blockId = document.getElementById("remove-block-id").value;
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
            console.log(data);
            if (data.success) {
                // document.getElementById("block-{{ id }}").remove();
                // TODO: REMOVE BLOCK WITH BLOCK_ID FROM BLOCKS
            }
        });
}