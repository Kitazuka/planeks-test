$(document).ready(function(){

    $("#generate_data").click(function(){

        var csrf = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "",
            type: "post",
            data: {
                rows: $("form").rows,
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                $("#table").append("<tr>" +
                    "<th scope='col'>" + response.dataset.id + "</th>" +
                    "<th>" + response.dataset.created + "</th>" +
                    "<th><span class='btn btn-secondary btn-sm pe-none' aria-pressed='false'>" + response.dataset.status + "</span></th>" +

                    "</tr>")
            }
        });
    });
});