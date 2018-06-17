const Modal = (function () {

    const Quantity = {
        /**
         * Inicializa el input quantity
         **/
        init: function (config, context) {
            this.$el = context.querySelector(config.el);

            // Nos ponemos a escuchar cambios en el input de cantidad
            this.$el.addEventListener("input", () => {
                if (this.validate()) {
                    config.onChangeQunatity(this.$el.value);
                }

                this.toggleError();
            });

            return this;
        },

        /**
         * Cambia el valor del input
         **/
        setValue: function (val) {
            this.$el.value = val;

            const e = document.createEvent("HTMLEvents");
            e.initEvent("input", false, true);
            this.$el.dispatchEvent(e);
        },

        /**
         * Valida el input
         **/
        validate: function () {
            this.isValid = this.$el.value > 0;
            return this.isValid;
        },

        /**
         * Muestra/Oculta los errores
         **/
        toggleError: function () {
            const $errorQuantity = this.$el.parentElement
                .querySelector(".help");

            this.$el.classList.toggle('is-danger', !this.isValid);
            $errorQuantity.classList.toggle('is-hidden', this.isValid);
        }
    };

    /**
     * Inicializa el modal de agregar producto
     **/
    function init(config) {
        const $modal = document.querySelector(config.el);
        const $edit = $modal.querySelector('#edit-button');
        const $save = $modal.querySelector('#save-button');

        // Inicializamos el input de cantidad
        const $quantity = Quantity.init({
            el: '#quantity',
            onChangeQunatity: function (quantity) {
                toggleButtons();
                config.onChangeQunatity(quantity);
            }
        }, $modal);

        // Inicializamos el select de productos
        const $select = Select.init({
            el: '#select',
            data: config.products,
            onSelect: function (product) {
                toggleButtons();
                config.onProductSelect(product);
            }
        });

        // Cambiamos el estado de save y edit
        function toggleButtons() {
            const isValid = $quantity.isValid && $select.isValid;

            if (isValid) {
                $edit.removeAttribute('disabled');
                $save.removeAttribute('disabled');
            } else {
                $edit.setAttribute('disabled', 'disabled');
                $save.setAttribute('disabled', 'disabled');
            }
        }

        $save.addEventListener('click', function () {
            config.onAddProduct().catch(function (err) {
                $select.showErrorMsg(err.msg);
                toggleButtons();
            });
        });

        $edit.addEventListener('click', config.onEditProduct);

        const modal = {
            $modal,
            $select,
            $quantity,
            $edit,
            $save,
            $editTitle: $modal.querySelector('#edit-title'),
            $saveTitle: $modal.querySelector('#save-title')
        };

        modal.close = close.bind(modal)
        modal.open = open.bind(modal)
        modal.openEdit = openEdit.bind(modal)

        toggleButtons();
        return modal;
    }

    /**
     * Abre el modal en modo agregar
     **/
    function open() {
        this.$edit.classList.add('is-hidden');
        this.$editTitle.classList.add('is-hidden');

        this.$save.classList.remove('is-hidden');
        this.$saveTitle.classList.remove('is-hidden');

        this.$select.clearSelect();
        this.$select.enable();
        this.$quantity.setValue(1);

        this.$modal.classList.add('is-active');
    }

    /**
     * Abre el modal en modo edicion
     **/
    function openEdit(product) {
        this.$edit.classList.remove('is-hidden');
        this.$editTitle.classList.remove('is-hidden');

        this.$save.classList.add('is-hidden');
        this.$saveTitle.classList.add('is-hidden');

        this.$select.disable();
        this.$select.selectValue(product.id);
        this.$quantity.setValue(product.quantity);

        this.$modal.classList.add('is-active');
    }

    /**
     * Cierra el modal
     **/
    function close() {
        this.$modal.classList.remove('is-active');
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
            nombree.value=nombree;
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
