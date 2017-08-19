function getContent() {
  $.ajax({
    type: "GET",
    url: "/content",
    dataType: 'html',
    processData: false,
    contentType: false,
  }).done(function(data) {
    console.log('content ok');
    $('#pattern_list').html(data);
  }).fail(function(data, textStatus, errorThrown) {
    console.log('content error');
  });
};
$(function() {
  $(document).on('click', '.add-btn', function(event) {
    event.preventDefault();
    console.log('add clicked');
    $.ajax({
      type: "POST",
      url: "/add",
      data: $('form.add-form').serialize(),
    }).done(function(data) {
      console.log('add ok');
      getContent();
    }).fail(function(data, textStatus, errorThrown) {
      console.log('add error');
      console.log(data);
      console.log(textStatus);
      console.log(errorThrown);
    });
  });
  $(document).on('click', '.delete-btn', function(event) {
    event.preventDefault();
    console.log('delete clicked');
    $.ajax({
      type: "POST",
      url: "/delete",
      data: $(this).parent().serialize(),
    }).done(function(data) {
      console.log('delete ok');
      getContent();
    }).fail(function(data, textStatus, errorThrown) {
      console.log('delete error');
      console.log(data);
      console.log(textStatus);
      console.log(errorThrown);
    });
  });
  $(document).on('click', '.trigger-btn', function(event) {
    event.preventDefault();
    console.log('trigger clicked');
    $.ajax({
      type: "POST",
      url: "/trigger",
    }).done(function(data) {
      console.log('trigger ok');
      var text = $('.trigger-btn').text();
      if (text == 'bot起動') {
        $('.trigger-btn').text('bot停止');
      } else {
        $('.trigger-btn').text('bot起動');
      }
    }).fail(function(data, textStatus, errorThrown) {
      console.log('trigger error');
      console.log(data);
      console.log(textStatus);
      console.log(errorThrown);
    });
  });
  $(document).on('click', '.register-btn', function(event) {
    event.preventDefault();
    console.log('register btn clicked');
    $.ajax({
      type: "POST",
      url: "/register_token",
      data: $(this).parent().parent().serialize(),
    }).done(function(data) {
      console.log('register ok');
      $('.trigger-btn').prop('disabled', false);
    }).fail(function(data, textStatus, errorThrown) {
      console.log('register error');
      console.log(data);
      console.log(textStatus);
      console.log(errorThrown);
    });
  });
});
