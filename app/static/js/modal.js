const Modal = (function () {

    /**
     * Abre el modal
     **/
    function open($modal) {
        const editTitle = document.getElementById('edit-title');
        const saveTitle = document.getElementById('save-title');
        const editButton = document.getElementById('edit-button');
        const saveButton = document.getElementById('save-button');

        $modal.classList.add('is-active');

        editButton.classList.add('is-hidden');
        editTitle.classList.add('is-hidden');
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

        return {
            close: close.bind(null, $modal),
            open: open.bind(null, $modal)
        }
    }

    return {
        init
    }
})();

