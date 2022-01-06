 $('[data-toggle="tooltip"]').tooltip();

function switchMode() {
    $.ajax({
        type: "GET",
        url: '/switchmode',
        success: function (response) {
            location.reload();
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Switching mode',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong!',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function triggerCall() {
    $.ajax({
        type: "GET",
        url: '/momalert',
        success: function (response) {
            var mothersday = new Date("5/9/2021");
            var todaysDate = new Date();
            if (mothersday.setHours(0, 0, 0, 0) == todaysDate.setHours(0, 0, 0, 0)) {
                toggleConfetti();
                Swal.fire({
                    position: 'top',
                    icon: 'success',
                    title: '母亲节快乐！',
                    showConfirmButton: false,
                    timer: 10000,
                    backdrop: false,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })
            } else {
                Swal.fire({
                    position: 'top',
                    icon: 'success',
                    title: '叫了宝宝了!',
                    showConfirmButton: false,
                    timer: 5000,
                    backdrop: false,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })
            }
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: '出问题了！',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function ambience(type) {
    $.ajax({
        type: "GET",
        url: '/ambience?v=' + type,
        success: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Ambience set.',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong!',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function flip(relay) {
    $.ajax({
        type: "GET",
        url: '/flip?v=' + relay,
        success: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Relay set.',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong!',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function signal(type) {
    $.ajax({
        type: "GET",
        url: '/signal?v=' + type,
        success: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Signal sent.',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong!',
                showConfirmButton: false,
                timer: 5000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}
