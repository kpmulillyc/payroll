$(function(){
    	$("#btn").click(function(){
            $.getJSON('/addEmployee',{
            marriage: $("input[name=optionsRadios]:checked").val(),
            gender: $("input[name=optionsRadios2]:checked").val(),
            type: $("input[name=optionsRadios3]:checked").val(),
            idnum: $("#idnum").val(),
            chinese: $("#chinese").val(),
            english: $("#english").val(),
            address: $("#address").val(),
            home: $("#home").val(),
            mobile: $("#mobile").val(),
            salary: $("#salary").val(),
            title: $("#title").val(),
            remarks: $("#remarks").val(),
            success: alert("good")
            });
        });
    });