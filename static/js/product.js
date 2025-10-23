//product.js

$(document).ready(function () {
    const $quantityInput = $('#quantity-input');
    const minQty = parseInt($quantityInput.data('min'), 10) || 1;
    const maxQty = parseInt($quantityInput.data('max'), 10) || 10;
    const stepQty = parseInt($quantityInput.data('step'), 10) || 1;
    const csrftoken = $('meta[name="csrf-token"]').attr('content');

    function clamp(value) {
        return Math.min(maxQty, Math.max(minQty, value));
    }

    function sanitize() {
        const val = parseInt($quantityInput.val(), 10);
        const safe = isNaN(val) ? minQty : clamp(val);
        $quantityInput.val(safe);
        return safe;
    }

    $('#increment-btn').on('click', () => {
        const val = clamp(parseInt($quantityInput.val()) + stepQty);
        $quantityInput.val(val);
    });

    $('#decrement-btn').on('click', () => {
        const val = clamp(parseInt($quantityInput.val()) - stepQty);
        $quantityInput.val(val);
    });

    $('#add-button').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/basket/add/',
            data: {
                productid: $(this).val(),
                productqty: sanitize(),
                csrfmiddlewaretoken: csrftoken,
                action: 'post'
            },
            success: function (json) {
                $('#basket_qty').text(json.qty);
            },
            error: function (xhr, errmsg, err) {
                console.error('Add failed:', errmsg);
            }
        });
    });
});

