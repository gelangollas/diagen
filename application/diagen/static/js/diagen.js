var diagen = diagen || {}

$(function (){

  var storage = null
  var image = null
  var defaultImageLink = "http://127.0.0.1:8000/static/img/default.png";
  var imageLink = null;
  var jqCanvas = $('#canvas')
  var viewport = $(window)
  var jqBody = $('body')
  var lineNumbers = $('#linenumbers')
  var lineMarker = $('#linemarker')
  var accountContent = document.getElementById('account-content');
  var modal = document.getElementById('generate-modal');
  var loginModal = document.getElementById('login-modal');
  var accountModal = document.getElementById('account-modal');
  var registrationModal = document.getElementById('registration-modal');
  var loadAnimation = document.getElementById('load-animation');
  var refreshImageButton = document.getElementById("refreshimage");
  var generateButton = document.getElementById("generatebutton");
  var loginButton = document.getElementById("login-button");
  var registrationBeginButton = document.getElementById("registration-begin-button");
  var registrationButton = document.getElementById("registration-submit");
  var accountButton = document.getElementById("account");
  var settingsToggler = document.getElementById("settingstoggle");
  var generateSubmitButton = document.getElementById("generatesubmit");
  var modalCloseBtn = document.getElementById("closebybtn");
  var imgLink = document.getElementById('savebutton')
  var textarea = document.getElementById('textarea')
  var canvasElement = document.getElementById('canvas')
  var generateSettingsBlock = document.getElementById('generatesettings')
  var canvasPanner = document.getElementById('canvas-panner')
  var canvasTools = document.getElementById('canvas-tools')
  var defaultSource = document.getElementById('defaultGraph').innerHTML
  var textForGenerate = document.getElementById('generatetext')
  var componentTypes = document.getElementById('componenttypes')
  var componentNames = document.getElementById('componentnames')
  var zoomLevel = 0
  var offset = {x:0, y:0}

  var editor = CodeMirror.fromTextArea(textarea, {
    lineNumbers: true,
    matchBrackets: true,
    keyMap: 'sublime'
  });

  document.getElementById('about').style.width = (document.getElementById('tools').offsetWidth+50).toString() + "px"

  canvasPanner.addEventListener('mouseenter', classToggler(jqBody, 'canvas-mode', true))
  canvasPanner.addEventListener('mouseleave', classToggler(jqBody, 'canvas-mode', false))

  setCurrentText(defaultSource)
  setNewImage(defaultImageLink)
  textForGenerate.value = ''

  var editorElement = editor.getWrapperElement()
  window.addEventListener('resize', _.throttle(sourceChanged, 750, {leading: true}))
  editor.on('changes', _.debounce(sourceChanged, 300))
  canvasPanner.addEventListener('wheel', _.throttle(magnify, 50))

  accountButton.addEventListener('click', function(e) {
    loadUserData();
  });
  generateButton.addEventListener('click', function(e) {
    modal.style.display = "block";
    textForGenerate.focus();
  });
  loginButton.addEventListener('click', function(e) {
    loadAnimation.style.display = "block";
    loginModal.style.display = "none";
    autentificateUser();
  });
  registrationBeginButton.addEventListener('click', function(e) {
    loginModal.style.display = "none";
    registrationModal.style.display = "block";
  });
  registrationButton.addEventListener('click', function(e) {
    if(checkUserData()){
      performRegistration();
    }
  });
  modalCloseBtn.addEventListener('click', function(e) {
    modal.style.display = "none";
  });
  settingsToggler.addEventListener('click', function(e) {
    if (generateSettingsBlock.style.display === 'none') {
        generateSettingsBlock.style.display = 'block';
    } else {
        generateSettingsBlock.style.display = 'none';
    }
  });
  generateSubmitButton.addEventListener('click', function(e) {
    modal.style.display = "none";
    loadAnimation.style.display = "block";
    performGenerateDiagram();
  });
  window.addEventListener('click', function(event) {
    var tg = event.target
    if (tg == modal || tg == loginModal || tg == registrationModal || tg == accountModal) {
        tg.style.display = "none";
    }
  });

  initToolbarTooltips()
  initImageDownloadLink(imgLink, canvasElement)

  function classToggler(element, className, state){
    var jqElement = $(element)
    return _.bind(jqElement.toggleClass, jqElement, className, state)
  }


  function magnify(e){
    zoomLevel = Math.min(10, zoomLevel - (e.deltaY < 0 ? -1 : 1))
    sourceChanged()
  }

  diagen.magnifyViewport = function (diff){
    zoomLevel = Math.min(10, zoomLevel + diff)
    sourceChanged()
  }

  diagen.refreshImage = function(){
    buildDiagramFromCode();
  }

  function buildDiagramFromCode(){
    jQuery.ajax({
      url: refreshImageButton.getAttribute("data-url"),
      type: 'POST',
      data: {"code": currentText()},
      dataType: "json",
      cache: false,
      success: function(data){
        if(data.error){
          alert('Произошла ошибка. \n' + data.message);
        }
        else {
          setNewImage(data.image_url);
        }
      }
    });
  }

  function loadUserData(){
    loadAnimation.style.display = "block";
    jQuery.ajax({
      url: '/load_user_data',
      type: 'POST',
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.is_autentificated){
          showUserData(data);
        }
        else {
          loginModal.style.display = "block";
        }
      }
    });
  }

  function performRegistration(){
    registrationModal.style.display = "none";
    loadAnimation.style.display = "block";

    username = document.getElementById("reg-user-name").value
    password = document.getElementById("reg-pass-text").value

    jQuery.ajax({
      url: registrationButton.getAttribute("url"),
      type: 'POST',
      data: {"username": username, "password": password},
      dataType: "json",
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.error){
          alert(data.error_message);
          registrationModal.style.display = "block";
        }
        else {
          alert('Регистрация успешно завершена, теперь вы можете войти в созданный аккаунт.');
          loginModal.style.display = "block";
        }
      }
    });
  }

  function checkUserData(){
    username = document.getElementById("reg-user-name").value
    password = document.getElementById("reg-pass-text").value
    password_repeat = document.getElementById("reg-pass-text-repeat").value
    if(username.length == 0 || password.length == 0){
      alert("Заполните все поля!")
    }
    else if(!(password === password_repeat)){
      alert("Пароли не совпадают.")
    }
    else 
      return true;
    return false;
  }

  function showUserData(data){
    accountContent.innerHTML = data.html_text;
    accountModal.style.display = "block";
  }

  function autentificateUser(){
    username = document.getElementById("logintext").value
    password = document.getElementById("passtext").value
    jQuery.ajax({
      url: loginButton.getAttribute("data-url"),
      type: 'POST',
      data: {"username": username, "password": password},
      dataType: "json",
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.error){
          alert('Произошла ошибка. \n' + data.error_message);
          loginModal.style.display = "block";
        }
        else {
          alert('Вы вошли в аккаунт '+username+'.' );
        }
      }
    });
  }

  function setNewImage(newImageUrl){
    img = new Image();
    img.addEventListener("load", function(){
        image = this
        sourceChanged()
    });
    imageLink = newImageUrl;
    img.src = imageLink;
  }

  diagen.saveCurrentDiagram = function(){
    accountModal.style.display = "none";
    loadAnimation.style.display = "block";

    title = document.getElementById('diagram-title').value
    jQuery.ajax({
      url: document.getElementById('diagram-save').getAttribute("url"),
      type: 'POST',
      data: {"code": currentText(), "title": title},
      dataType: "json",
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.error){
          alert(data.error_message);
          accountModal.style.display = "block";
        }
        else {
          alert(data.message);
        }
      }
    });
  }

  diagen.loadDiagramWithId = function(pk){
    accountModal.style.display = "none";
    loadAnimation.style.display = "block";

    jQuery.ajax({
        url: '/load_user_diagram',
        type: 'POST',
        data: {"pk": pk},
        dataType: "json",
        cache: false,
        success: function(data){
          loadAnimation.style.display = "none";
          if(data.error){
            alert(data.error_message);
          }
          else {
            setCurrentText(data.code)
            setNewImage(data.url)
          }
        }
      });
  }

  diagen.deleteDiagram = function(pk){
    if (confirm('Вы действительно хотити удалить эту диаграмму?')){
      accountModal.style.display = "none";
      loadAnimation.style.display = "block";
      jQuery.ajax({
        url: '/delete_user_diagram',
        type: 'POST',
        data: {"pk": pk},
        dataType: "json",
        cache: false,
        success: function(data){
          loadAnimation.style.display = "none";
          if(data.error){
            alert(data.error_message);
          }
          else {
            loadUserData();
          }
        }
      });
    }
  }

  diagen.resetViewport = function (){
    zoomLevel = 0
    offset = {x: 0, y: 0}
    sourceChanged()
  }

  diagen.toggleSidebar = function (id){
    $(document.getElementById(id)).toggleClass('visible')
  }

  diagen.discardCurrentGraph = function (){
    if (confirm('Вы действительно хотити удалить текущую диаграмму и загрузить пример?')){
      setCurrentText(defaultSource)
      setNewImage(defaultImageLink)
      sourceChanged()
    }
  }

  diagen.exitViewMode = function (){
    window.location = './'
  }

  function performGenerateDiagram(){
    jQuery.ajax({
      url: generateSubmitButton.getAttribute("data-url"),
      type: 'POST',
      data: {
        "text": textForGenerate.value, 
        "component_types": componentTypes.value,
        "component_names": componentNames.value
      },
      dataType: "json",
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.error){
          alert('Произошла ошибка.\n' + data.message);
        }
        else {
          setCurrentText(data.code);
          setNewImage(data.image_url);
        }
      }
    });
  }

  function initImageDownloadLink(link, canvasElement){
    link.addEventListener('click', downloadImage, false);
    function downloadImage(){
      link.href = imageLink;
    }
  }

  function initToolbarTooltips(){
    var tooltip = $('#tooltip')[0]
    $('.tools a').each(function (i, link){
      link.onmouseover = function (){ tooltip.textContent  = $(link).attr('title') }
      link.onmouseout = function (){ tooltip.textContent  = '' }
    })
  }

  function positionCanvas(rect, superSampling, offset){
    var w = rect.width / superSampling
    var h = rect.height / superSampling
    jqCanvas.css({
      top: 300 * (1 - h/viewport.height()) + offset.y,
      left: 150 + (viewport.width() - w)/2 + offset.x,
      width: w,
      height: h
    })
  }

  function setFilename(filename){
    imgLink.download = filename + '.png'
  }

  function reloadStorage(){
    storage = buildStorage(location.hash)
    editor.setValue(storage.read())
    sourceChanged()
    if (storage.isReadonly) storageStatusElement.show()
    else storageStatusElement.hide()
  }

  function currentText(){
    return editor.getValue()
  }

  function setCurrentText(value){
    return editor.setValue(value)
  }

  function drawDiagram(canvas, zoom, sampling){
    var ctx = canvas.getContext("2d");

    canvas.width = image.naturalWidth*zoom;
    canvas.height = image.naturalHeight*zoom;

    ctx.drawImage(image, 0, 0, canvas.width, canvas.height)
    positionCanvas(canvasElement, sampling, offset)
  }

  function sourceChanged(){
    try {
      lineMarker.css('top', -30);
      lineNumbers.toggleClass('error', false)
      var superSampling = window.devicePixelRatio || 1
      var scale = superSampling * Math.exp(zoomLevel/10)

      drawDiagram(canvasElement, scale, superSampling);
    } catch (e){
      var matches = e.message.match('line ([0-9]*)')
      lineNumbers.toggleClass('error', true)
      if (matches){
        var lineHeight = parseFloat($(editorElement).css('line-height'))
        lineMarker.css('top', 3 + lineHeight*matches[1])
      } else {
        throw e
      }
    }
  }
})