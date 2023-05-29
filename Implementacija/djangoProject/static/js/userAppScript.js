if (window.location.href === "http://127.0.0.1:8000/user/registerUser") {
    document.querySelector('#userRegistration').addEventListener('submit', function (event) {
        event.preventDefault();

        const birthdateInput = document.getElementById('birthdate');
        const birthdate = new Date(birthdateInput.value);

        const ageInMilliseconds = Date.now() - birthdate.getTime();

        const ageInYears = new Date(ageInMilliseconds).getUTCFullYear() - 1970;

        if (ageInYears < 18) {
            swal("Morate imati 18 godina da biste se registrovali", "", "warning");
        } else {
            document.querySelector('#userRegistration').submit();
        }
    });
}

