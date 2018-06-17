$(function(){
    var total = $('#backgrounds img').length;
    var counter = 1;


        function cycle(){
            // Makes old backgrounds appear beneath new ones
            $('#backgrounds img').css('z-index','1')
            // Set it to display and opacity 0 so we get the effect
            $('#backgrounds img:nth-child('+counter+')').css({'opacity':'0','display':'block','z-index':'2'})

            // Fade the background in
            $('#backgrounds img:nth-child('+counter+')').animate({'opacity':'1'},1500)

            // increase the counter
            counter++

            // make sure we're working within the quantity of images we have
            if( counter > total ){ counter = 1 }
        }
        cycle();
        setInterval(function(){cycle()},6000);

        //$('#footer').css('position','fixed');

})