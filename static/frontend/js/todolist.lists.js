$(document).ready(function (){
    $('#btn').click(function(){
        $.ajax({
            url: 'http://127.0.0.1:8000/todolist/v3/todo-lists/',
            type: 'get',
            data: {
                button_text: $(this).text()
            },
            success: function(response){
                $("#btn").text(response.list)
            }
        })
    })
})