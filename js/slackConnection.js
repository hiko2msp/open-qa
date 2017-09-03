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
    startload();
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
      stopload();
    }).fail(function(data, textStatus, errorThrown) {
      console.log('trigger error');
      console.log(data);
      console.log(textStatus);
      console.log(errorThrown);
      stopload();
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

function startload() {
    var loader_h = $('#loader').height();
    $('.loader-wrap').css('display', 'none');
    $('#loader-bg ,#loader').css('display', 'block');
    $('#loader').css({
        'height' : loader_h + 'px',
        'margin-top' : '-' + loader_h + 'px'
    });
    console.log('start loading');
}

function stopload() {
    $('.loader-wrap').css('display', 'block');
    $('#loader-bg').delay(900).fadeOut(800);
    $('#loader').delay(600).fadeOut(300);
    console.log('stop loading');
}

$(window).load(function() {
    $('#loader-bg').delay(900).fadeOut(800);
    $('#loader').delay(600).fadeOut(300);
    $('.loader-wrap').css('display', 'block');
});
