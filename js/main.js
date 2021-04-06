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

    function sweetAlertExample() {
        $.ajax({
            type: "GET",
            url: '/momalert',
            success: function (response) {
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