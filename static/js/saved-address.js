/* Handle Saved Address Selection
------------------------------------------------ */
$(document).ready(function() {
    var $select = $('#saved-address-select');
    
    var applyAddress = function() {
        var selectedOption = $(this).find('option:selected');
        
        if (selectedOption.val()) {
            // Get data from selected option
            var fullName = selectedOption.data('full-name') || '';
            var nameParts = fullName.split(' ');
            var firstName = nameParts[0] || '';
            var lastName = nameParts.slice(1).join(' ') || '';
            var phone = selectedOption.data('phone') || '';
            var area = phone.replace(/[^0-9+]/g, '').slice(0, 4);
            
            // Get address values
            var country = selectedOption.data('country') || 'Pakistan';
            var state = selectedOption.data('state') || '';
            var city = selectedOption.data('city') || '';
            
            // Populate form fields
            $('input[name="first_name"]').val(firstName);
            $('input[name="last_name"]').val(lastName);
            $('input[name="area_code"]').val(area);
            $('input[name="primary_phone"]').val(phone);
            $('input[name="address_1"]').val(selectedOption.data('address1') || '');
            $('input[name="address_2"]').val(selectedOption.data('address2') || '');
            $('input[name="zip_code"]').val(selectedOption.data('zip') || '');
            
            // Use native JavaScript to set values for country, state, city to work with handlePakistanRegionSelects
            var countrySelect = document.getElementById('country-select');
            var stateSelect = document.getElementById('state-select');
            var citySelect = document.getElementById('city-select');
            
            if (countrySelect && stateSelect && citySelect) {
                // Set country
                countrySelect.value = country;
                
                // Manually trigger the population of states
                var changeEvent = new Event('change', { bubbles: true });
                countrySelect.dispatchEvent(changeEvent);
                
                // Wait for states to populate, then set state
                setTimeout(function() {
                    stateSelect.value = state;
                    // Trigger state change to populate cities
                    stateSelect.dispatchEvent(new Event('change', { bubbles: true }));
                    
                    // Wait for cities to populate, then set city
                    setTimeout(function() {
                        citySelect.value = city;
                        citySelect.dispatchEvent(new Event('change', { bubbles: true }));
                    }, 100);
                }, 100);
            }
            
            // Scroll to form smoothly
            $('html, body').animate({
                scrollTop: $('input[name="first_name"]').offset().top - 100
            }, 500);
        } else {
            // Clear form if no address selected
            $('input[name="first_name"]').val('');
            $('input[name="last_name"]').val('');
            $('input[name="area_code"]').val('');
            $('input[name="primary_phone"]').val('');
            $('input[name="address_1"]').val('');
            $('input[name="address_2"]').val('');
            $('input[name="zip_code"]').val('');
        }
    };
    
    // Apply when user selects
    $select.on('change', applyAddress);
    
    // Auto-select default address on load
    var $defaultOption = $select.find('option[data-default="true"]').first();
    if ($defaultOption.length) {
        setTimeout(function() {
            $defaultOption.prop('selected', true);
            applyAddress.call($select);
        }, 500); // Wait for apps.js to initialize
    }
});

