// FUNCION PARA REALIZAR VALIDACIONES
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
        })
    })() 

    //VALIDACION EXTENSION DE TELEFONO
    document.getElementById('telefono').onkeypress =
      function (e) {
        var ev = e || window.event;
        if(ev.charCode < 48 || ev.charCode > 57) {
          return false; // not a digit
        } else if(this.value * 10 + ev.charCode - 48 > this.max) {
           return false;
        } else {
           return true;
        }
      }

    //VALIDACION EXTENSION DE rut
    document.getElementById('rut').onkeypress =
    function (e) {
      var ev = e || window.event;
      if(ev.charCode < 48 || ev.charCode > 57) {
        return false; // not a digit
      } else if(this.value * 10 + ev.charCode - 48 > this.max) {
         return false;
      } else {
         return true;
      }
    }



    function buscaEmpleado() {
        // Declare variables
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("myTable");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
            }
        }
        }
    

      
   