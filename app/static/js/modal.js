const Modal = (function () {

    /**
     * Abre el modal
     **/
    function open($modal,productoID,tipo) {
       
        const editTitle = document.getElementById('edit-title');
        const saveTitle = document.getElementById('save-title');
        const editButton = document.getElementById('edit-button');
        const saveButton = document.getElementById('save-button');
        const sel = document.getElementById('select-prod');
        const preUnitario = document.getElementById('preUnitario');
        const nom = document.getElementById('nombre');
      


        $modal.classList.add('is-active');

        saveButton.classList.add('is-hidden');
        saveTitle.classList.add('is-hidden');
        editButton.classList.add('is-hidden');
        editTitle.classList.add('is-hidden');
        preUnitario.classList.add('is-hidden');
        sel.classList.add('is-hidden');
        nom.classList.add('is-hidden');
       


        switch(tipo){
            case "E" :
            llenado(productoID);

             nom.classList.remove('is-hidden');
             editButton.classList.remove('is-hidden');
             editTitle.classList.remove('is-hidden');
             preUnitario.classList.remove('is-hidden');
             
            API.getOrderProduct(1,productoID).then(function(r){onChangeQunatity(r);});
           
            break;

            case "A":
             sel.classList.remove('is-hidden');
             saveButton.classList.remove('is-hidden');
             saveTitle.classList.remove('is-hidden');
             preUnitario.classList.remove('is-hidden');

             break;
             default:
                console.log("error")
        }

       
    }

    /**
     * Cierra el modal
     **/
    function close($modal) {
        $modal.classList.remove('is-active');
    }

    /**
     * Inicializa el modal de agregar producto
     **/
    function init(config) {
        const $modal = document.querySelector(config.el);

        // Inicializamos el select de productos
        Select.init({
            el: '#select',
            data: config.products,
            onSelect: config.onProductSelect
        });

        // Nos ponemos a escuchar cambios en el input de cantidad
        $modal.querySelector('#quantity')
            .addEventListener('input', function () {
                config.onChangeQunatity(this.value)
            });

        $modal.querySelector('#save-button')
            .addEventListener('click', config.onAddProduct);

        $modal.querySelector('#edit-button')
            .addEventListener('click', config.onEditProduct);
        


        return {
            close: close.bind(null, $modal),
            open: open.bind(null, $modal)
        }
    }
    function llenado(productoID) //Completa el modal
    {
        const nombree= document.getElementById('select-prod').options[productoID].innerText;
        const select = document.getElementById('select-prod');
        const unitario = document.getElementById('preUnit');
        const precioT = document.getElementById('total-price');
        const cant = document.getElementById('quantity');
        
        API.getOrderProduct(1,productoID).then(function (result)
        {
            nombre.value=nombree;
            select.value=productoID;
            unitario.value=result["price"];
            cant.value=result["quantity"];
            precioT.innerHTML = "Precio total: $ "+ result['totalPrice'];

        });
    }

    return {
        init
    }
})();
