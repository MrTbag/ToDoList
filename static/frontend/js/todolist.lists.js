function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

$(document).ready(function (){
    let api_url = 'http://127.0.0.1:8000/api/todolist/v3/todo-lists/'
    $("#btn").click(function(){
        $.ajax({
            type: 'GET',
            url: api_url,
            success: function(response){
                console.log('success', response.results)
                $.each(response.results, function (i, list){

                    $("#lists").append("<li><a href=\"" + list.id + "\">" + list.name + "</a></li>");
                })
                $("#btn").remove();
            }
        });
    });

    $("#submit").click(function(){
        $.ajax({
            type: 'POST',
            url: api_url,
            headers: {
                    'X-CSRFToken': getCookie('csrftoken')
            },
            data: {
                "name": $("#id_name").val(),
                "description": $("#id_description").val(),
                "tasks": $("#id_tasks").val(),
            },
            success: function(response){
                setTimeout(() => {
                    window.location.replace("http://127.0.0.1:8000/todolists/created-successfully/");
                }, 100);
            }
        });
    });

});