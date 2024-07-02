const add_btn = document.getElementById("task-add");
add_btn.addEventListener("click", async () => {
    await add_overlay();
});

const new_sub_task_btns = document.getElementsByClassName("new-sub-task");
Array.from(new_sub_task_btns).forEach(el => {
    el.addEventListener("click", () => add_overlay( parseInt(el.id.slice(5, 6)) ) );
});


async function add_overlay(parent = null) {
    fetch("/plans/new",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
        }).then(response => response.text())
        .then(prompt => {
            const overlay = document.createElement("div")
            overlay.id="overlay"
            overlay.className = "overlay"
            overlay.innerHTML = prompt;
            document.body.appendChild(overlay);
            overlay.offsetHeight;
            overlay.classList.add("visible");

            const cancel_btn = document.getElementById("cancel-create-task-btn");
            cancel_btn.addEventListener("click", async () => {
                overlay.classList.remove("visible");
                overlay.addEventListener("transitionend", () => {
                    document.body.removeChild(overlay);
                })
            });

            const create_task_btn = document.getElementById("create-task-btn");
            create_task_btn.addEventListener("click", async () => {
                const inputs = document.getElementsByClassName("task-inputs");
                let new_task_name = inputs[0].querySelector("input").value;
                let new_task_description = inputs[1].querySelector("textarea").value;
                await add_task(new_task_name, new_task_description, parent);
            });
        });
}


async function add_task(name, desc, parent = null) {
    fetch("/plans/new", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            task_name: name,
            task_description: desc,
            task_parent: parent,
        })
    }).then(response => response.json())
    .then(data => {
        if (data["success"]) {
            const overlay = document.getElementById("overlay");
            overlay.classList.remove("visible");
            overlay.addEventListener("transitionend", () => {
                document.body.removeChild(overlay);
            })

            const snackbar = document.getElementById("snackbar");
            snackbar.innerHTML = "&#x2714; Successfully added task!";
            snackbar.classList.add("show");

            setTimeout(function () {
                snackbar.classList.remove("show");
                snackbar.innerHTML = "";
            }, 3000);

            $( "#task-list" ).load(window.location.href + " #task-list" );
        } else {
            const prompt = document.getElementById("prompt");
            const btns = document.getElementById("task-btns");
            const e_message = document.createElement("div");
            e_message.innerHTML = "<p>&#x26A0; Something went wrong!</p>";
            prompt.insertBefore(e_message, btns);
        }
    })
}