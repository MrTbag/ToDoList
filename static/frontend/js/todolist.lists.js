$(document).ready(function (){
    $("#btn").click(function(){
        $.ajax({
            url: 'http://127.0.0.1:8000/api/todolist/v3/todo-lists/',
            type: 'get',
            success: function(response){
                console.log('success', response.results)
                $.each(response.results, function (i, list){
                    $("#lists").append("<li><a href=\"{% url 'frontend:list_detail' %}\">" + list.name + "</a></li>");
                })
                $("#btn").remove();
            }
        })
    });
});