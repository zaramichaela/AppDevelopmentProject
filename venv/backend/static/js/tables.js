

    $(document).ready(function() {
var oTable = $('#dtBasicExample').DataTable( {
        dom: 'Blfrtip',
        buttons: [
       {

           text: 'COPY',
           extend: 'copyHtml5',
           exportOptions: {
                columns: ':visible:not(.action)'
            }
       },
       {
           text: 'EXCEL',
           extend: 'excelHtml5',
           exportOptions: {
                columns: ':visible:not(.action)'
            }
       },
        {
           text: 'CSV',
           extend: 'csvHtml5',
           exportOptions: {
                columns: ':visible:not(.action)'
            }
       },
           {
           text: 'PDF',
           extend: 'pdfHtml5',
           exportOptions: {
                columns: ':visible:not(.action)'
            }
       },

    ]
    } );
$('#dtBasicExample').DataTable();
} );
