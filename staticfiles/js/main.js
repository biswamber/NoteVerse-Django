document.addEventListener("DOMContentLoaded", () => {

    /* =======================
       LIKE AJAX
    ======================== */

    document.querySelectorAll(".like-btn").forEach(btn => {

        btn.addEventListener("click", function (e) {

            e.preventDefault();

            fetch(this.href)

                .then(r => r.json())

                .then(data => {

                    this.querySelector(".like-count").innerText =
                        data.total_likes;

                    if (data.liked) {

                        this.classList.remove("btn-outline-danger");
                        this.classList.add("btn-danger");

                    } else {

                        this.classList.remove("btn-danger");
                        this.classList.add("btn-outline-danger");

                    }

                });

        });

    });

    /* =======================
       BOOKMARK AJAX
    ======================== */

    document.querySelectorAll(".bookmark-btn").forEach(btn => {

        btn.addEventListener("click", function (e) {

            e.preventDefault();

            fetch(this.href)

                .then(r => r.json())

                .then(data => {

                    const text = this.querySelector(".bookmark-text");

                    if (data.saved) {

                        this.classList.remove("btn-outline-warning");
                        this.classList.add("btn-warning");

                        text.innerText = "★ Saved";

                    } else {

                        this.classList.remove("btn-warning");
                        this.classList.add("btn-outline-warning");

                        text.innerText = "☆ Save";

                    }

                });

        });

    });

});


/* =======================
   FOLLOW AJAX
======================= */

const followBtn = document.getElementById("follow-btn");

if (followBtn) {

    followBtn.addEventListener("click", function (e) {

        e.preventDefault();

        fetch(this.href)

            .then(res => res.json())

            .then(data => {

                document.getElementById("followers-count").innerText =
                    data.followers;

                if (data.followed) {

                    followBtn.innerText = "Unfollow";

                    followBtn.classList.remove("btn-primary");

                    followBtn.classList.add("btn-danger");

                }

                else {

                    followBtn.innerText = "Follow";

                    followBtn.classList.remove("btn-danger");

                    followBtn.classList.add("btn-primary");

                }

            });

    });

}


/* =======================
   DARK MODE
======================= */

const themeBtn = document.getElementById("theme-toggle");

if (themeBtn) {

    if (localStorage.getItem("theme") == "dark") {

        document.body.classList.add("dark-mode");

        themeBtn.innerHTML = "☀️";

    }

    themeBtn.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

            themeBtn.innerHTML = "☀️";

        }

        else {

            localStorage.setItem("theme", "light");

            themeBtn.innerHTML = "🌙";

        }

    });

}


/* =======================
   LIVE SEARCH
======================= */

const searchBox = document.querySelector("input[name='q']");

const searchResults = document.getElementById("search-results");

if (searchBox) {

    searchBox.addEventListener("keyup", () => {

        let query = searchBox.value;

        if (query.length < 2) {

            searchResults.innerHTML = "";

            return;

        }

        fetch(`/live-search/?q=${query}`)

            .then(res => res.json())

            .then(data => {

                searchResults.innerHTML = "";

                data.forEach(note => {

                    searchResults.innerHTML += `

<a href="/note/${note.id}/"

class="list-group-item list-group-item-action">

${note.title}

</a>

`;

                });

            });

    });

}

/* =======================
   SHARE NOTE
======================= */

document.querySelectorAll(".share-btn").forEach(btn => {

    btn.addEventListener("click", function(e){

        e.preventDefault();

        const url =
        window.location.origin + this.dataset.url;

        navigator.clipboard.writeText(url);

        const oldText = this.innerHTML;

        this.innerHTML = "✅ Copied";

        setTimeout(()=>{

            this.innerHTML = oldText;

        },2000);

    });

});