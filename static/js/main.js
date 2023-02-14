$(document).ready(function(){

    $("#generate_data_form").submit(function(e){

        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
            url: "/post/ajax/dataset/",
            type: "post",
            data: serializedData,
            success: function(response) {
                $("#generate_data_form").trigger('reset');
                $("#table").append("<tr>" +
                    "<th scope='col'>" + response.dataset.id + "</th>" +
                    "<th class='fw-normal'>" + response.dataset.created + "</th>" +
                    "<th><span class='btn btn-success btn-sm pe-none' aria-pressed='false'>" + response.dataset.status + "</span></th>" +
                    `<th><a href="${response.dataset.url}" download class="text-decoration-none fw-normal">` + "Download" + "</a></th>" +
                    "</tr>")
            }
        });
    });
});
