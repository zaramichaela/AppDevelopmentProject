
$(document).ready(function() {
    $('#dtBasicExample').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    } );
    $('.dataTables_length').addClass('bs-select');
} );

//
//$(document).ready(function () {
//$('#dtBasicExample').DataTable();
//
//});
