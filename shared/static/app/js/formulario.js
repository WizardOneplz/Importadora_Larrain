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

    //VALIDACION EXTENSION DE stock
    document.getElementById('stock').onkeypress =
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

      //VALIDACION EXTENSION DE stock
    document.getElementById('precio').onkeypress =
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

    

      
   