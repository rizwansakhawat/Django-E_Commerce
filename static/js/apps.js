/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.7
Version: 2.1.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v2.1/frontend/e-commerce/
    ----------------------------
        APPS CONTENT TABLE
    ----------------------------
    
    <!-- ======== GLOBAL SCRIPT SETTING ======== -->
    01. Handle Fixed Header Option
    02. Handle Page Container Show
    03. Handle Pace Page Loading Plugins
    04. Handle Tooltip Activation
    05. Handle Theme Panel Expand
    06. Handle Theme Page Control
    07. Handle Payment Type Selection
    08. Handle Checkout Qty Control
    09. Handle Product Image
	
    <!-- ======== APPLICATION SETTING ======== -->
    Application Controller
*/



/* 01. Handle Fixed Header Option
------------------------------------------------ */
var handleHeaderFixedTop = function() {
    if ($('#header[data-fixed-top="true"]').length !== 0) {
        $(window).on('scroll', function() {
            if ($('body').scrollTop() >= 40) {
                $('body').css('padding-top', '76px');
                $('#header').addClass('header-fixed');
            } else {
                $('#header').removeClass('header-fixed');
                $('body').css('padding-top', '0');
            }
        });
    }
};


/* 02. Handle Page Container Show
------------------------------------------------ */
var handlePageContainerShow = function() {
    $('#page-container').addClass('in');
};


/* 03. Handle Pace Page Loading Plugins
------------------------------------------------ */
var handlePaceLoadingPlugins = function() {
    Pace.on('hide', function(){
        setTimeout(function() {
            $('.pace').addClass('hide');
        },500);
    });
};


/* 04. Handle Tooltip Activation
------------------------------------------------ */
var handleTooltipActivation = function() {
    if ($('[data-toggle=tooltip]').length !== 0) {
        $('[data-toggle=tooltip]').tooltip();
    }
};


/* 05. Handle Theme Panel Expand
------------------------------------------------ */
var handleThemePanelExpand = function() {
    $('[data-click="theme-panel-expand"]').live('click', function() {
        var targetContainer = '.theme-panel';
        var targetClass = 'active';
        if ($(targetContainer).hasClass(targetClass)) {
            $(targetContainer).removeClass(targetClass);
        } else {
            $(targetContainer).addClass(targetClass);
        }
    });
};


/* 06. Handle Theme Page Control
------------------------------------------------ */
var handleThemePageControl = function() {
    
    if ($.cookie && $.cookie('theme')) {
        if ($('.theme-list').length !== 0) {
            $('.theme-list [data-theme]').closest('li').removeClass('active');
            $('.theme-list [data-theme="'+ $.cookie('theme') +'"]').closest('li').addClass('active');
        }
        var cssFileSrc = '/static/css/theme/' + $.cookie('theme') + '.css';
        $('#theme').attr('href', cssFileSrc);
    }
    
    $('.theme-list [data-theme]').live('click', function() {
        var cssFileSrc = '/static/css/theme/' + $(this).attr('data-theme') + '.css';
        $('#theme').attr('href', cssFileSrc);
        $('.theme-list [data-theme]').not(this).closest('li').removeClass('active');
        $(this).closest('li').addClass('active');
        $.cookie('theme', $(this).attr('data-theme'));
    });
};


/* 07. Handle Payment Type Selection
------------------------------------------------ */
var handlePaymentTypeSelection = function() {
    $('[data-click="set-payment"]').click(function(e) {
        e.preventDefault();
        
        var targetLi = $(this).closest('li');
        var targetValue = $(this).attr('data-value');
        $('[data-click="set-payment"]').closest('li').not(targetLi).removeClass('active');
        $('[data-id="payment-type"]').val(targetValue);
        $(targetLi).addClass('active');
    });
};


/* 08b. Handle Pakistan Region Selects (Country/State/City)
------------------------------------------------ */
var handlePakistanRegionSelects = function() {
    var countrySel = document.getElementById('country-select');
    var stateSel = document.getElementById('state-select');
    var citySel = document.getElementById('city-select');
    if (!countrySel || !stateSel || !citySel) {
        return;
    }

    var regions = {
        "Pakistan": {
            "Punjab": ["Lahore","Faisalabad","Rawalpindi","Gujranwala","Multan","Sialkot","Bahawalpur","Sargodha","Sheikhupura","Gujrat","Jhelum","Rahim Yar Khan","Kasur"],
            "Sindh": ["Karachi","Hyderabad","Sukkur","Larkana","Nawabshah","Mirpur Khas","Jacobabad","Shikarpur","Dadu"],
            "Khyber Pakhtunkhwa": ["Peshawar","Abbottabad","Mardan","Swat","Kohat","Dera Ismail Khan","Haripur"],
            "Balochistan": ["Quetta","Gwadar","Khuzdar","Turbat","Chaman","Sibi"],
            "Islamabad Capital Territory": ["Islamabad"],
            "Gilgit-Baltistan": ["Gilgit","Skardu","Hunza"],
            "Azad Jammu and Kashmir": ["Muzaffarabad","Mirpur","Kotli","Rawalakot"]
        }
    };

    function clearOptions(sel) {
        while (sel.options.length > 0) {
            sel.remove(0);
        }
    }

    function addOption(sel, value, text) {
        var opt = document.createElement('option');
        opt.value = value;
        opt.text = text;
        sel.add(opt);
    }

    function populateStates(country, presetState, presetCity) {
        clearOptions(stateSel);
        clearOptions(citySel);
        addOption(stateSel, '', 'Select State / Province');
        addOption(citySel, '', 'Select City');
        var states = regions[country];
        if (!states) { return; }
        Object.keys(states).forEach(function(state) { addOption(stateSel, state, state); });
        if (presetState && states[presetState]) {
            stateSel.value = presetState;
            populateCities(country, presetState, presetCity);
        }
    }

    function populateCities(country, state, presetCity) {
        clearOptions(citySel);
        addOption(citySel, '', 'Select City');
        var states = regions[country];
        if (!states) { return; }
        var cities = states[state] || [];
        cities.forEach(function(city) { addOption(citySel, city, city); });
        if (presetCity && cities.indexOf(presetCity) >= 0) {
            citySel.value = presetCity;
        }
    }

    var savedCountry = countrySel.value || 'Pakistan';
    var savedState = stateSel.value || '';
    var savedCity = citySel.value || '';

    countrySel.value = savedCountry;
    populateStates(savedCountry, savedState, savedCity);

    countrySel.addEventListener('change', function() {
        populateStates(countrySel.value, '', '');
    });
    stateSel.addEventListener('change', function() {
        populateCities(countrySel.value, stateSel.value, '');
    });
};


/* 08. Handle Checkout Qty Control
------------------------------------------------ */
var handleQtyControl = function() {
    $('[data-click="increase-qty"]').click(function(e) {
        e.preventDefault();
        var targetInput = $(this).attr('data-target');
        var targetValue = parseInt($(targetInput).val()) + 1;  
        
        $(targetInput).val(targetValue);
        updateCartTotal();
        saveQuantityToServer($(targetInput));
    });
    $('[data-click="decrease-qty"]').click(function(e) {
        e.preventDefault();
        var targetInput = $(this).attr('data-target');
        var targetValue = parseInt($(targetInput).val()) - 1;  
            targetValue = (targetValue < 0) ? 0 : targetValue;
        $(targetInput).val(targetValue);
        updateCartTotal();
        saveQuantityToServer($(targetInput));
    });
    
    // Handle manual quantity input changes
    $('.qty-input').on('change', function() {
        updateCartTotal();
        saveQuantityToServer($(this));
    });
};

/* Save Quantity to Server
------------------------------------------------ */
var saveQuantityToServer = function($qtyInput) {
    var itemId = $qtyInput.attr('id').replace('qty-', '');
    var quantity = parseInt($qtyInput.val());
    
    if (isNaN(quantity) || quantity < 1) {
        quantity = 1;
        $qtyInput.val(quantity);
    }
    
    // Send AJAX POST to update database
    $.ajax({
        url: '/cart/update-quantity/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        }),
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(response) {
            if (response.success) {
                // Update the display
                $qtyInput.val(response.quantity);
                updateCartTotal();
            }
        },
        error: function() {
            console.error('Failed to update quantity');
        }
    });
};

/* Get CSRF Cookie
------------------------------------------------ */
var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

/* Update Cart Total
------------------------------------------------ */
var updateCartTotal = function() {
    var cartSubtotal = 0;
    
    // Get unit prices from each row and recalculate
    $('table.table-cart tbody tr').each(function() {
        var $row = $(this);
        var $priceCell = $row.find('.cart-price');
        var $qtyInput = $row.find('.cart-qty-input input');
        var $totalCell = $row.find('.cart-total');
        
        if ($priceCell.length && $qtyInput.length && $totalCell.length) {
            var priceText = $priceCell.text().replace('$', '').trim();
            var price = parseFloat(priceText);
            var quantity = parseInt($qtyInput.val());
            var itemTotal = price * quantity;
            
            // Update the item total
            $totalCell.text('$' + itemTotal.toFixed(2));
            
            // Add to cart subtotal
            cartSubtotal += itemTotal;
        }
    });
    
    // Update cart summary
    var cartSummaryValue = cartSubtotal.toFixed(2);
    $('.summary-row .value').each(function() {
        var $summaryValue = $(this);
        if ($summaryValue.prev('.field').text() === 'Cart Subtotal' || 
            $summaryValue.prev('.field').text() === 'Total') {
            $summaryValue.text('$' + cartSummaryValue);
        }
    });
};


/* 09. Handle Product Image
------------------------------------------------ */
var handleProductImage = function() {
    $('[data-click="show-main-image"]').click(function(e) {
        e.preventDefault();
        
        var targetContainer = '[data-id="main-image"]';
        var targetImage = '<img src="'+ $(this).attr('data-url') +'" />';
        var targetLi = $(this).closest('li');
        
        $(targetContainer).html(targetImage);
        $(targetLi).addClass('active');
        $('[data-click="show-main-image"]').closest('li').not(targetLi).removeClass('active');
    });
};


/* Application Controller
------------------------------------------------ */
var App = function () {
	"use strict";
	
	return {
		//main function
		init: function () {
		    handleHeaderFixedTop();
		    handlePageContainerShow();
		    handlePaceLoadingPlugins();
            handleTooltipActivation();
            handleThemePanelExpand();
            handleThemePageControl();
            handlePaymentTypeSelection();
            handleQtyControl();
            handleProductImage();
                        handlePakistanRegionSelects();
		}
  };
}();