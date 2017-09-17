console.log("loaded");
var globalObject = {
    lectureRating: 0
};
var authToken = localStorage.getItem('authToken');

if (authToken !== null) {
    globalObject.authToken = authToken;
}

var ratingMap = {
    star5: 5,
    star4half: 4.5,
    star4: 4,
    star3half: 3.5,
    star3: 3,
    star2half: 2.5,
    star2: 2,
    star1half: 1.5,
    star1: 1,
    starhalf: 0.5
};

let d = new Date();
let m = d.getMonth() + 1;
globalObject.currentMonth = m;

$('button#student.btn.btn-success.login').click(function () {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/login',
        data: {
            'userType': $(this).attr('id'),
            'userName': $('input#studentUsername').val(),
            'password': $('input#studentPassword').val(),
            'firstName': 'Harshit',
            'lastName': 'Jain',
            'email': 'iit2016060@iiita.ac.in'
        },
        success: function (data) {
            localStorage.setItem('authToken', data.authToken);
            globalObject.authToken = data.authToken;
            window.location.href = "http://127.0.0.1:8000/student";
        },
        error: function (error) {
            console.log(error);
        }
    })
});

$('button#professor.btn.btn-success.login').click(function () {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/login',
        data: {
            'userType': $(this).attr('id'),
            'userName': $('input#professorUsername').val(),
            'password': $('input#professorPassword').val(),
            'firstName': 'Doctor',
            'lastName': 'Who',
            'email': 'drwho@find.me.com'
        },
        success: function (data) {
            localStorage.setItem('authToken', data.authToken);
            globalObject.authToken = data.authToken;
            window.location.href = "http://127.0.0.1:8000/professor";
        },
        error: function (error) {
            console.log(error);
        }
    })
});

if (window.location.href.split('/').reverse()[0] == 'student') {
    document.addEventListener('DOMContentLoaded', function () {
        $.ajax({
            type: 'GET',
            dataType: 'json',
            headers: {
                'authorization-token': globalObject.authToken
            },
            url: 'http://127.0.0.1:8000/api/students',
            success: function (data) {
                $('div#course-wrapper').empty();
                data.coursesTaken.forEach(function (element) {
                    var box = document.createElement("div");
                    box.setAttribute('class', 'col-sm-4 col-lg-4 col-md-5');
                    var thumbnail = document.createElement('div');
                    thumbnail.className = 'thumbnail';
                    thumbnail.innerHTML += "<center><div class='caption'><h3>" + element.course_code + "</h3><h5>" + element.course_name +
                        "</h5><button id='" + element.course_code + "' class='btn btn-success view-student-attendance'>View Attendance</button></div></center>";
                    $(box).append(thumbnail);
                    $('div#course-wrapper').append(box);
                }, this);
            }
        })
    })
}

if (window.location.href.split('/').reverse()[0] == 'professor') {
    document.addEventListener('DOMContentLoaded', function () {
        $.ajax({
            type: 'GET',
            dataType: 'json',
            headers: {
                'authorization-token': globalObject.authToken
            },
            url: "http://127.0.0.1:8000/api/faculty/course",
            success: function (data) {
                console.log(data);
                data.forEach(function (element) {
                    var box = document.createElement("div");
                    box.setAttribute('class', 'col-sm-4 col-lg-4 col-md-5');
                    var thumbnail = document.createElement('div');
                    thumbnail.className = 'thumbnail';
                    thumbnail.innerHTML += `<center>
                    <div class="caption">
                        <h3>` + element.course_name + `</h3>
                        <h4 id="courseCode">` + element.course_code + `</h4>
                    </div>
                    <!-- View Token -->
                    <div class="caption">
                        <button id="generateTokens" class="btn btn-primary" data-toggle="modal" data-target="#myModalNorm" data-coursecode="` + element.course_code + `">
                            Generate Tokens
                        </button>
                        <br>

                    </div>
                </center>`;
                    $(box).append(thumbnail);
                    $('div#course-wrapper.row').append(box);
                }, this);
            }
        })
    })
}

$('button#add-course-professor.btn.btn-success').click(function() {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/faculty/course",
        data: {
            "course": $('input#add-course-courseId.form-control').val()
        },
        success: function (data) {
            $('p#error-message').text(data);
        },
        error: function (error) {
            $('p#error-message').text(data);
        }
    })
});

$('button#remove-course-professor.btn.btn-danger').click(function() {
    $.ajax({
        type: 'DELETE',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/faculty/course",
        data: {
            "course": $('input#add-course-courseId.form-control').val()
        },
        success: function (data) {
            $('p#error-message').text(data);
        },
        error: function (error) {
            $('p#error-message').text(data);
        }
    })
});

$('button#add-course-student.btn.btn-success').click(function() {
    $.ajax({
        type: 'PUT',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/student/course",
        data: {
            "course": $('input#add-course-courseId.form-control').val(),
            "semester": $('input#add-course-semester.form-control').val(),
            "section": $('input#add-course-section.form-control').val()
        },
        success: function (data) {
            $('p#error-message').text(data);
        },
        error: function (error) {
            $('h4#error-message').text(data);
        }
    })
});

$('button#remove-course-student.btn.btn-danger').click(function() {
    $.ajax({
        type: 'DELETE',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/student/course",
        data: {
            "course": $('input#add-course-courseId.form-control').val(),
            "semester": $('input#add-course-semester.form-control').val(),
            "section": $('input#add-course-section.form-control').val()
        },
        success: function (data) {
            console.log(data);
            $('h4#error-message').text(data);
        },
        error: function (error) {
            console.log(error);
            $('h4#error-message').text(error);
        }
    })
});

$('button#update-student.btn.btn-success').click(function() {
    $.ajax({
        type: 'PUT',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/students",
        data: {
            "name": $('input#student-name.form-control').val(),
            "email": $('input#student-email.form-control').val(),
            "currentSemester": $('input#student-semester.form-control').val(),
            "graduationYear": $('input#student-graduation-year.form-control').val()
        },
        success: function (data) {
            console.log(data);
            $('h4#error-message').text(data);
        },
        error: function (error) {
            console.log(error);
            $('h4#error-message').text(data);
        }
    })
});

$('button#course-attendance.btn.btn-primary').on('click', function () {
    let course = $('input#attendance-courseId.form-control').val();
    let section = $('input#attendance-section.form-control').val();
    let month = $('input#attendance-month.form-control').val();
    globalObject.currentMonth = month;
    $.ajax({
        type: 'GET',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/attendance/course?course=" + course + "&section=" + section + "&month=" + month,
        success: function (data) {
            $('p#error-message').text("");
            let htmlString = `<center><h3>` + course.toUpperCase() + `</h3></center><center><h4>` + data.rating + `</h4></center>

    <table class="table table-hover">
        <thead>
        <tr>
            <th>Enrolment No.</th>
            <th>Name</th>
            <th colspan="12">
                <center>Attendance</center>

            </th>
        </tr>
        <tr>
            <th></th>
            <th></th>`
            data.payload[0].attendanceData.forEach(function (element) {
                htmlString += "<th>" + element.date.slice(0, 5) + "</th>"
            });

            htmlString += `<th></th>

        </tr>
        <tr>
        <th></th>
            <th></th>`;
            data.payload[0].attendanceData.forEach(function (element) {
                htmlString += "<th>" + element.lecture_type + "</th>"
            });
            htmlString += `<th></th>
        
        </tr>
        </thead>
        <tbody>`
            data.payload.forEach(function (element) {
                htmlString += `<tr>
            <td>` + element.enrollmentNo.toUpperCase() + `</td>
            <td>` + element.name + `</td>`;
                element.attendanceData.forEach(function (attendance) {
                    if (attendance.is_present) {
                        htmlString += `<td>P</td>`
                    } else {
                        htmlString += `<td>A</td>`
                    }
                });
            });
            htmlString += `</tbody>
    </table>`;
            $('div#course-attendance-wrapper.container.table-responsive.table-hover').html(htmlString);
        },
        error: function (error) {
            $('div#course-attendance-wrapper').empty();
            $('p#error-message').text(error.responseText);

        }
    })
});


$('button#increase-token.btn.btn-primary').click(function () {
    $.ajax({
        type: 'PUT',
        dataType: 'json',
        headers: {
            'authorization-token': globalObject.authToken
        },
        url: "http://127.0.0.1:8000/api/attendance-tokens",
        data: {
            "token": $('input#attendance-token.form-control').val(),
            "increaseBy": $('input#attendance-count.form-control').val()
        },
        success: function (data) {
            $(this).addClass("disable");
            $('p#error-message').text(data);
        },
        error: function (error) {
            $('p#error-message').text(data);
        }
    })
});

$('button#getTokens').click(function () {
    var lectureType, noOfLectures;

    if (document.getElementById('lab').checked) {
        lectureType = 'lab';
    } else {
        lectureType = 'theory';
    }

    if (document.getElementById('1-hour').checked || document.getElementById('lab-hour').checked) {
        noOfLectures = 1;
    } else if (document.getElementById('2-hour').checked) {
        noOfLectures = 2;
    }

    var dateTime = $('input#datetimepicker5.form-control').val();
    var date = dateTime.split(" ")[0].split("/").reverse().join("-");
    var time = dateTime.split(" ")[1];
    var hours = time.split(":")[0];
    //it is pm if hours from 12 onwards
    var suffix = (hours >= 12) ? 'PM' : 'AM';

    //only -12 from hours if it is greater than 12 (if not back at mid night)
    hours = (hours > 12) ? hours - 12 : hours;

    //if 00 then it is 12 am
    hours = (hours == '00') ? 12 : hours;

    time = hours + ":" + time.split(":")[1] + suffix;
    // console.log(date);
    // console.log(time);
    // console.log(noOfLectures);
    // console.log(lectureType);
    // console.log($('input#section.form-control').val().toUpperCase());
    // console.log($('input#courseId.form-control').val());
    // console.log($('input#totalStudents.form-control').val());
    // console.log($('input#token.form-control').val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/attendance-tokens',
        data: {
            "course": $('input#courseId.form-control').val(),
            'section': $('input#section.form-control').val().toUpperCase(),
            'date': date,
            'time': time,
            'noOfLectures': noOfLectures,
            'lectureType': lectureType,
            'totalStudents': $('input#totalStudents.form-control').val(),
            'noOfTokens': $('input#token.form-control').val()
        },
        headers: {
            'authorization-token': globalObject.authToken
        },
        success: function (data) {
            $('#myModalNorm').modal('hide');
            $('div#all-tokens-wrapper.row').empty();
            data.forEach(function (element) {
                let box = document.createElement("div");
                box.setAttribute('class', 'col-md-6 col-md-offset-3 col-sm-12');
                box.innerHTML += "<center><h3>" + element.token + " - " + element.token_issued + "</h3></center>";
                $('div#all-tokens-wrapper.row').append(box);
            }, this);

        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('button#mark-attendance.btn.btn-success').click(function () {
    $.ajax({
        type: 'PUT',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/attendance/student',
        data: {
            'attendanceToken': $('input#token.form-control').val(),
            'course': $('input#course.form-control').val(),
            'rating': ratingMap[globalObject.lectureRating],
            'feedback': $('input#feedback.form-control').val()
        },
        headers: {
            'authorization-token': globalObject.authToken
        },
        success: function (data) {
            $('h4#error-message').text(data.responseText);
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('input.star-rating').click(function () {
    globalObject.lectureRating = $(this).attr('id');
});

$('button#log-out.btn.btn-warning').click(function() {
    $.ajax({
        type: 'PUT',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/logout',
        headers: {
            'authorization-token': globalObject.authToken
        },
        success: function (data) {
            localStorage.removeItem('authToken');
            window.location.replace("http://127.0.0.1:8000");
        },
        error: function (error) {
            $('h4#error-message').text(error);
        }
    });
});

$('#course-wrapper').on("click", "button.btn.btn-success.view-student-attendance", function () {
    globalObject.course = $(this).attr("id");
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: "http://127.0.0.1:8000/api/attendance/student?course=" + $(this).attr("id"),
        headers: {
            'authorization-token': globalObject.authToken
        },
        success: function (data) {
            console.log(data);
            $('div#attendance-wrapper').empty();
            var htmlString = `<center>
            <h3 id="course-name">` + globalObject.course + `</h4>
        </center>
        <div class="row>">
            <center><h4 class="col-lg-6 col-sm-12">Total lectures : ` + data.totalLectures + `</h5></center>
            <center><h4 class="col-lg-6 col-sm-12">Lectures Attended : ` + data.lecturesAttended + `</h5></center>
        </div>
        <div class="row">
            <div class="col-lg-12 col-sm-12">`;

            if (data.percentage.substring(0, data.percentage.length - 1) < 50) {
                htmlString += `<div id="attendance-bar" class="w3-container w3-padding-small w3-center w3-red" style="width: ` + data.percentage + `;">` + data.percentage + `</div>`;
            } else if (data.percentage.substring(0, data.percentage.length - 1) < 75) {
                htmlString += `<div id="attendance-bar" class="w3-container w3-padding-small w3-center w3-yellow" style="width: ` + data.percentage + `;">` + data.percentage + `</div>`;
            } else {
                htmlString += `<div id="attendance-bar" class="w3-container w3-padding-small w3-center w3-green" style="width: ` + data.percentage + `;">` + data.percentage + `</div>`;
            }

            htmlString += `</div>
        </div>
        <div class="row" id="attendance-details">`;
            data.attendance.forEach(function (element) {
                htmlString += `<div class="col-lg-3 col-sm-12">
                    <center><div class="thumbnail">
                    <div class="container-fluid">
                            <div class="caption">
                                <h4>` + element.date + `</h4>
                                <h4>` + element.time + `</h4 >
                                <div class="row">
                                    <div class="col-lg-6 col-sm-6">` + element.no_of_lectures + ` Lectures</div>
                                    <div class="col-lg-6 col-sm-6">` + element.lecture_type + `</div>
                                </div>`;
                if (element.is_present === true) {
                    htmlString += `<h3 style="color: green;">Present</h3></div></div></div></center></div>`;
                } else {
                    htmlString += `<h3 style="color: red;">Absent</h3></div></div></div></center></div>`;
                }
            })

            htmlString += `</div>
        </div>`;
            $('div#attendance-wrapper').append(htmlString);
        },
        error: function (error) {
            $('h4#error-message').text(error);
        }
    });
});