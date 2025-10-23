// basket.js

$(document).ready(function () {
    const csrftoken = $('meta[name="csrf-token"]').attr('content');

    function toggleEmptyState(isEmpty) {
        $('#basket-empty').toggleClass('d-none', !isEmpty);
        $('#basket-items').toggleClass('d-none', isEmpty);
        $('#basket-summary').toggleClass('d-none', isEmpty);
    }

    // DELETE ITEM
    $(document).on('click', '.delete-button', function (e) {
        e.preventDefault();
        const prodid = $(this).data('index');
        $.ajax({
            type: 'POST',
            url: '/basket/delete/',
            data: {
                productid: prodid,
                csrfmiddlewaretoken: csrftoken,
                action: 'post'
            },
            success: function (json) {
                const item = $('.product-item[data-index="' + prodid + '"]');
                item.addClass('removed');
                setTimeout(() => item.remove(), 300);

                $('#subtotal').text(json.subtotal);
                $('#basket_qty').text(json.qty);

                if (parseInt(json.qty, 10) === 0) {
                    toggleEmptyState(true);
                }
            },
            error: function (xhr, errmsg, err) {
                console.error('Delete failed:', errmsg);
            }
        });
    });

    // UPDATE ITEM
    $(document).on('click', '.update-button', function (e) {
        e.preventDefault();
        const prodid = $(this).data('index');
        const input = $('#qty' + prodid);
        let quantity = parseInt(input.val(), 10);
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
        }

        $.ajax({
            type: 'POST',
            url: '/basket/update/',
            data: {
                productid: prodid,
                productqty: quantity,
                csrfmiddlewaretoken: csrftoken,
                action: 'post'
            },
            success: function (json) {
                $('#basket_qty').text(json.qty);
                $('#subtotal').text(json.subtotal);

                if (json.removed) {
                    const item = $('.product-item[data-index="' + prodid + '"]');
                    item.addClass('removed');
                    setTimeout(() => item.remove(), 300);

                    if (parseInt(json.qty, 10) === 0) {
                        toggleEmptyState(true);
                    }
                    return;
                }

                input.val(json.item_qty);
                $('.item-total[data-index="' + prodid + '"]').text(json.item_total);

                const breakdown = $('.item-breakdown[data-index="' + prodid + '"]');
                if (breakdown.length) {
                    if (parseInt(json.item_qty, 10) > 1) {
                        breakdown.text(json.item_qty + ' × £' + json.item_price + ' each');
                    } else {
                        breakdown.text('£' + json.item_price);
                    }
                }
            },
            error: function (xhr, errmsg, err) {
                console.error('Update failed:', errmsg);
            }
        });
    });
});