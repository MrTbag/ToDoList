$(document).ready(function (){
    $("#btn").click(function(){
        $.ajax({
            url: 'http://127.0.0.1:8000/todolist/v3/todo-lists/',
            type: 'get',
            success: function(response){
                console.log('success', response.results)
                $.each(response.results, function (i, list){
                    $("#lists").append("<li>" + list.name + "</li>");
                })
                $("#btn").remove();
            }
        })
    });
});