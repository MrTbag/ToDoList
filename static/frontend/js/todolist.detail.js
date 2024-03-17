function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

$(document).ready(function (){
    let todolist = $("#todolist");
    let api_url = `http://127.0.0.1:8000/api/todolist/v3/todo-lists/${todolist.data("id")}/`;
    $("#detail-btn").click(function(){
        $.ajax({
            url: api_url,
            type: 'get',
            success: function(){
                $("#details").append("<h3>Details: </h3>\n" +
                        "    <ul>\n" +
                        "        <li><p>Description: " + todolist.data("description") + "</p></li>\n" +
                        "        <li><p>Date Published: " + todolist.data("pubdate") + "</p></li>\n" +
                        "    </ul>");
                $("#detail-btn").remove();
            },
            cache: false,
        })
    });

    $("#delete-btn").click(function(){
        $.ajax({
            url: api_url,
            type: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(){
                $("#delete-response").text("Deleted successfully")
                setTimeout(function (){
                    window.location.replace("http://127.0.0.1:8000/tickapp/todolists/");
                }, 1000)
            },
            cache: false,
        })
    });

    $("#save").click(function(){
        $.ajax({
            type: 'PUT',
            url: api_url,
            headers: {
                    'X-CSRFToken': getCookie('csrftoken')
            },
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                "name": $("#id_name").val(),
                "description": $("#id_description").val(),
                "tasks": $("#id_tasks").val(),
            }),
            success: function(){
                setTimeout(() => {
                    window.location.replace('http://127.0.0.1:8000/tickapp/todolists/');
                }, 1000);
            },
            cache: false,
        });
    });
});