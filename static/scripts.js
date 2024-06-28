$(document).ready(function() {
    $('#birthDetailsForm').on('submit', function(event) {
        event.preventDefault();
        $('#loading').show();
        $('#result').hide();

        let dateOfBirth = $('#dateOfBirth').val();
        let timeOfBirth = $('#timeOfBirth').val();
        let placeOfBirth = $('#placeOfBirth').val();

        $.ajax({
            url: '/calculate-vedic-astrological-sign',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                date_of_birth: dateOfBirth,
                time_of_birth: timeOfBirth,
                place_of_birth: placeOfBirth
            }),
            success: function(response) {
                setTimeout(function() { // Add a delay before showing the result
                    $('#loading').hide();
                    $('#vedicSign').text(response.vedic_astrological_sign);
                    $('#result').show();
                }, 2000); // 2000 milliseconds = 2 seconds
            },
            error: function(xhr, status, error) {
                setTimeout(function() { // Add a delay before showing the error
                    $('#loading').hide();
                    $('#vedicSign').text('Error calculating the sign. Please try again.');
                    $('#result').show();
                    console.error('Error:', error);
                    console.error('Status:', status);
                    console.error('Response:', xhr.responseText);
                }, 2000); // 2000 milliseconds = 2 seconds
            }
        });
    });
});
