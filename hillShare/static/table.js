$(document).ready(function() {
var table = $('#table').DataTable( {
	"order":[],
	"columnDefs":[{
	"targets":'no-sort',
	"oderable":false,	
	}]
} );

setInterval( function () {
    $.getJSON($SCRIPT_ROOT+"/table",
	{},
	      // user paging is no

function(data){		

    console.log(data);
	
    $('#table').DataTable().destroy();  
    $('#table').DataTable({
	    
	    "ajax":data, 

}
	     );
	     }, 10000 );
}
);
