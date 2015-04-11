$('document').ready(function() {
  $('.scroll-link').click(function(e) {
    e.preventDefault();
    var to = $(this).attr('href');
    $('html, body').animate({ scrollTop: $(to).offset().top }, 800);
  });
	
	$(window).resize(function() {
		$('body').scrollspy('refresh');
	});

  var BIG_DAY = new Date(2015, 9, 10, 16);
  var msLeft = BIG_DAY.getTime() - Date.now();
  $('#days-left').text(Math.floor(msLeft / 86400000) + ' ');

  $('.glyphicon-remove').click(function(e) {
  	e.preventDefault();
  	$(this).parent().parent().remove();
  });

  $('#add-guest-link').click(function(e) {
  	e.preventDefault();
  	var $row = $('.table tr:last-child').clone(true);
  	$('.glyphicon-remove', $row).css('visibility', 'visible');
  	$('input', $row).val('');
  	$('select', $row).val('Yes');
  	$('.table').append($row);
  });

  $('#rsvp-button').click(function() {
  	$('#rsvp-button').prop('disabled', true).text('Working...')

  	var data = {};
  	var dataIndex = 0;
  	$('form tr').each(function(index) {
  		if (index > 0) {
  			var firstName = $(this).find('.first-name').val();
  			var lastName = $(this).find('.last-name').val();
  			var attending = $(this).find('.attending').val() == 'Yes';
        var shuttle = $(this).find('.shuttle').val() == 'Yes';
        var attendingBeach = $(this).find('.attending-beach').val() == 'Yes';
        var attendingAquarium = $(this).find('.attending-aquarium').val() == 'Yes';
        var allergies = $(this).find('.allergies').val();
  			if (firstName != '' || lastName != '') {
  				data['first_name_' + dataIndex] = firstName;
  				data['last_name_' + dataIndex] = lastName;
  				data['attending_' + dataIndex] = attending;
          data['shuttle_' + dataIndex] = shuttle;
          data['attending_beach_' + dataIndex] = attendingBeach;
          data['attending_aquarium_' + dataIndex] = attendingAquarium;
          data['allergies_' + dataIndex] = allergies;
  				dataIndex++;
  			}
  		}
  	});
    data.hotel = $('form .hotel').val();
  	data.comment = $('form textarea').val();

  	$.post('/rsvp', data, function() {
  		$('#rsvp-button').text('Done!').removeClass('btn-default').addClass('btn-success');
      $('#add-guest-link').remove();
      $('form tr').each(function(index) {
        if (index > 0) {
          var firstName = $(this).find('.first-name').val();
          var lastName = $(this).find('.last-name').val();
          var attending = $(this).find('.attending').val();
          var shuttle = $(this).find('.shuttle').val()
          var attendingBeach = $(this).find('.attending-beach').val();
          var attendingAquarium = $(this).find('.attending-aquarium').val();
          var allergies = $(this).find('.allergies').val();
          if (firstName != '' || lastName != '') {
            $(this).html(
              '<td>' + firstName + '</td>' +
              '<td>' + lastName + '</td>' +
              '<td>' + attending + '</td>' +
              '<td>' + shuttle + '</td>' +
              '<td>' + attendingBeach + '</td>' +
              '<td>' + attendingAquarium + '</td>' +
              '<td>' + allergies + '</td>'
            );
          } else {
            $(this).remove();
          }
        }
      });
      var $hotelInput = $('form .hotel');
      var hotel = $hotelInput.val();
      var $hotelInputContainer = $hotelInput.parent();
      $hotelInput.remove();
      $hotelInputContainer.append($('<span>' + hotel + '</span>'));

      var $textArea = $('form textarea');
      var comment = $textArea.val();
      var $textAreaContainer = $textArea.parent();
      $textArea.remove();
      $textAreaContainer.append($('<p>' + comment + '</p>'));
  	});
  });
});