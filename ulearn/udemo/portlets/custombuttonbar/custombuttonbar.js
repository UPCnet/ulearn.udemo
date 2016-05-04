$(document).ready(function (event) {

  // Escondemos los componentes al cargar la pagina
	$('.portlet-subscribed-news').hide();

  // Cuando clicamos a la paginación de noticias,
  if(window.location.href.indexOf("b_start") > -1){
    $('#maxui-widget-container').hide();
    $('.portlet-subscribed-news').show();

    $('#menusup .active').removeClass('active');
    $('#menusup').children().children().children().next().addClass('active')
  }

	// Para mostrar o esconder los portlets cuando cambiamos en el menu
	$('.portaltype-plone-site a[data-target="#corporatiu"]').on('show', function (e) {
	  $('#maxui-widget-container').show();
    $('.portlet-subscribed-news').hide();
	});

	$('.portaltype-plone-site a[data-target="#mynews"]').on('show', function (e) {
	  $('.portlet-subscribed-news').show();
	  $('#maxui-widget-container').hide();
	});

	$('.portaltype-plone-site a[data-target="#mycomunities"]').on('show', function (e) {
	  $('.portlet-subscribed-news').hide();
	  $('#maxui-widget-container').hide();
	});

  $('.portaltype-plone-site a[data-toggle="tab"]').on('show', function (e) {

        var targetid = $(this).data('target');
        var remote = $(targetid).data('remote');
        if (remote) {
            $(targetid).load(portal_url + "/" + remote, function (event) {
                $('.sortablelist').mixitup({layoutMode: 'list'});
            });
        }
        $('#menusup .active').removeClass('active');
        $(e.target.parentElement.parentElement).addClass('active');
    });

});
