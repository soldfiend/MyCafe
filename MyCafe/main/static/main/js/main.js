document.addEventListener("DOMContentLoaded", function () {
    var profileDropdown = document.getElementById("profile-dropdown");
    var avatar = document.querySelector(".avatar");

    avatar.addEventListener("click", function (e) {
        e.stopPropagation();
        profileDropdown.style.display = "block";
    });

    document.addEventListener("click", function () {
        profileDropdown.style.display = "none";
    });

    profileDropdown.addEventListener("click", function (e) {
        e.stopPropagation();
    });
});
