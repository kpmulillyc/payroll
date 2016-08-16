$(function(){
    	$("#btn").click(function(){
            $.ajax({
            url: "/addEmployee",
            type: 'POST',
            data: {
            marriage: $("input[name=optionsRadios]:checked").val(),
            gender: $("input[name=optionsRadios2]:checked").val(),
            type: $("input[name=optionsRadios3]:checked").val(),
            eDate: $("#datepicker").val(),
            probation: $("input[name=optionsPro]:checked").val(),
            pd: $("#pd").val(),
            pm: $("#pm").val() * 28,
            idnum: $("#idnum").val(),
            chinese: $("#chinese").val(),
            english: $("#english").val(),
            address: $("#address").val(),
            home: $("#home").val(),
            mobile: $("#mobile").val(),
            salary: $("#salary").val(),
            title: $("#title").val(),
            remarks: $("#remarks").val()
            },
            success: function(data){
            alert(data.bbb);
          },
            });
        });
    });

  $( function() {
    $( "#datepicker" ).datepicker({
      dateFormat: "yy-mm-dd",
	  changeMonth: true,
      changeYear: true,
      showOn: "button",
      buttonImage: "../static/img/calendar.gif",
      buttonImageOnly: true,
      buttonText: "Select date"
    });
  } );

  $(function(){
	$("#pro").hide();
		$('#yes').click(function(){
	 	$("#pro").show();
	 	});
	 	$('#no').click(function(){
	 	$("#pro").hide();
	 	});
  });