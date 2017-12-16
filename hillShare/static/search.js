/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
$(document).ready(function() {
    // create a data table from existing html table
    table = $('#table1').DataTable();
   
    $('#table1 tbody').on('click', 'tr', function () {
        var rowthis = this; 
        var row = table.row( this ).data();  
	console.log(row[0])                
        $.getJSON($SCRIPT_ROOT + '/request1',
	
        {name: row[0]},
        function(data) {                          
        
        }
        );
        
        
    });

}); 

  