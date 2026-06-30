document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".like-btn").forEach(button => {

        button.addEventListener("click", function (e) {

            e.preventDefault();

            fetch(this.href)
                .then(response => response.json())
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

});