

$(document).ready(function () {

    get_data();

});


function get_data() {


    //alert("Sdfsdfsd");


    $.ajax({
        url : '/home/' ,
        type : 'post' ,
        dataType: 'json',

        success : function (response) {

                $('#google_loader').css('opacity' ,  '0');
                var i;

                for (i=0; i<response.data.length ; i++){

                    var main_div = $('#main_div');

                    var div = $('<div class="panel panel-primary" style="margin-top: 2em" id="Question' + (i+1) + '"></div>');
                    //div.css('id' , 'Question' + (i+1));
                    var panel_heading = $('<div class="panel-heading" style="font-size: 1.5em;"></div>');
                    panel_heading.html('Question'+ (i+1));
                    div.append(panel_heading);


                    var panel_body = $('<div class="panel-body">');
                    var question = $('<p style="font-size: 1.3em;"></p>');
                    question.html(response.data[i].question);

                    var form = $('<form id="'+ 'Answer' + (i+1) + '"></form>');

                    //alert('Answer' + (i+1));

                    var label1 = $('<label class="radio-inline"><input type="radio" name="optradio" value="' + response.data[i].choice1 + '">' + response.data[i].choice1 + '</label>');
                    var label2 = $('<label class="radio-inline"><input type="radio" name="optradio" value="' + response.data[i].choice2 +  '">'+ response.data[i].choice2 + '</label>');
                    var label3 = $('<label class="radio-inline"><input type="radio" name="optradio" value="' + response.data[i].choice3 + '">'+ response.data[i].choice3 + '</label> <input type="hidden" id="Length" value="' + response.data.length + '">');
                    var label4 = $('<label class="radio-inline"><input type="radio" name="optradio" value="' + response.data[i].choice4 +'">'+ response.data[i].choice4 + '</label> <input type="hidden" id="id" value="' + response.data[i].id + '">');


                    panel_body.append(question);
                   // panel_body.append(checkbox);
                    form.append(label1);
                    form.append(label2);
                    form.append(label3);
                    form.append(label4);

                    panel_body.append(form);

                    div.append(panel_body);


                    main_div.append(div)



                }

                 $('#submit_button').css('opacity' , '1');

                var deadline = new Date(Date.parse(new Date()) +  30 * 60 *   1000);
                initializeClock('clockdiv', deadline);

                //var submit = $('<button type="submit" class="btn btn-success btn-lg" id="submit_button" style="margin-bottom: 2em;">Submit</button>');

                //main_div.append(submit);

        } ,

        fail : function () {


            alert("eeee");

        } ,

    });

}




$('#submit_button').click(function (event) {

    //alert("clicked");
    event.preventDefault();

    $('#myModal').modal('show');});


$('#Confirm_submit').click(function (event) {

     var data = update_score('confirm_submit');
    $.ajax({
        url: '/score_calculate/',
        type: 'post',

        dataType: 'json',
        data: {
            'data[]' : data
        },
        success: function (response) {


            //alert("jjjjj");
            $('#google_loader').css('opacity' , 0 );

            window.location = '/login'

            //alert("timeout");

        },

        fail: function () {

        }


    });
});


function update_score(s) {


    //alert("clicked");
    //alert(s);

    if ( s=='confirm_submit'){
        $('#myModal').modal('toggle');
        $('#google_loader').css('opacity' , 1 );
        $('#google_loader').css('z-index' , 9999 );
    }
    else{
        $('#myModal2').modal('toggle');
    }


    //event.preventDefault();

    // $('#myModal').modal('show');

     var length = $('#Length').val();
    var data = [];


    for (var i = 0; i < length; i++) {

        var obj = []

        var id_field = $('#Question' + (i + 1) + ' #id').val();
        var choice = $('input[name=optradio]:checked', '#Answer' + (i + 1)).val();
        //alert(choice);
        //alert(id_field)

        //alert($('input[name=optradio]:checked', '#Answer' + (i + 1)).val());

        obj.push(id_field)
        obj.push(choice)
        data.push(obj)

    }

    return data;
    //alert(data);





}


function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  //var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  //var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
   // 'days': days,
   // 'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime) {
  var clock = document.getElementById(id);
  //var daysSpan = clock.querySelector('.days');
  //var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    //daysSpan.innerHTML = t.days;
    //hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total < 0) {
      clearInterval(timeinterval);
         minutesSpan.innerHTML = ('00');
        secondsSpan.innerHTML = ('00');

       var data = update_score('timeout');

       $.ajax({
        url: '/score_calculate/',
        type: 'post',

        dataType: 'json',
        data: {
            'data[]' : data
        },
        success: function (response) {


            //alert("jjjjj");
            $('#google_loader').css('opacity' , 0 );

            // window.location = '/login'

            //alert("timeout");

        },

        fail: function () {

        }


    });


    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}







