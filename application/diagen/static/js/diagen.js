var diagen = diagen || {}

$(function (){

  var storage = null
  var image = null
  var defaultImageLink = "http://127.0.0.1:8000/static/diagrams/default.png";
  var imageLink = null;
  var jqCanvas = $('#canvas')
  var viewport = $(window)
  var jqBody = $('body')
  var lineNumbers = $('#linenumbers')
  var lineMarker = $('#linemarker')
  var modal = document.getElementById('modal');
  var loadAnimation = document.getElementById('load-animation');
  var refreshImageButton = document.getElementById("refreshimage");
  var generateButton = document.getElementById("generatebutton");
  var generateSubmitButton = document.getElementById("generatesubmit");
  var modalCloseBtn = document.getElementById("closebybtn");
  var imgLink = document.getElementById('savebutton')
  var textarea = document.getElementById('textarea')
  var canvasElement = document.getElementById('canvas')
  var canvasPanner = document.getElementById('canvas-panner')
  var canvasTools = document.getElementById('canvas-tools')
  var defaultSource = document.getElementById('defaultGraph').innerHTML
  var textForGenerate = document.getElementById('generatetext')
  var zoomLevel = 0
  var offset = {x:0, y:0}

  var editor = CodeMirror.fromTextArea(textarea, {
    lineNumbers: true,
    matchBrackets: true,
    keyMap: 'sublime'
  });

  setCurrentText(defaultSource)
  setNewImage(defaultImageLink)

  var editorElement = editor.getWrapperElement()
  window.addEventListener('resize', _.throttle(sourceChanged, 750, {leading: true}))
  editor.on('changes', _.debounce(sourceChanged, 300))
  canvasPanner.addEventListener('wheel', _.throttle(magnify, 50))
  generateButton.addEventListener('click', function(e) {
    modal.style.display = "block";
  });
  modalCloseBtn.addEventListener('click', function(e) {
    modal.style.display = "none";
    textForGenerate.value = "";
  });

  generateSubmitButton.addEventListener('click', function(e) {
    modal.style.display = "none";
    loadAnimation.style.display = "block";
    performGenerateDiagram();
  });
  window.addEventListener('click', function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        textForGenerate.value = "";
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
          alert('Произошла ошибка.');
        }
        else {
          setNewImage(data.image_url);
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

  diagen.resetViewport = function (){
    zoomLevel = 0
    offset = {x: 0, y: 0}
    sourceChanged()
  }

  diagen.toggleSidebar = function (id){
    var sidebars = ['reference', 'about']
    _.each(sidebars, function (key){
      if (id !== key) $(document.getElementById(key)).toggleClass('visible', false)
    })
    $(document.getElementById(id)).toggleClass('visible')
  }

  diagen.discardCurrentGraph = function (){
    if (confirm('Вы действительно хотити удалить текущую диаграмму и загрузить пример?')){
      setCurrentText(defaultSource)
      setNewImage(defaultImageLink)
      sourceChanged()
    }
  }

  diagen.saveViewModeToStorage = function (){
    var question = 
      'Do you want to overwrite the diagram in ' +
      'localStorage with the currently viewed diagram?'
    if (confirm(question)){
      storage.moveToLocalStorage()
      window.location = './'
    }
  }

  diagen.exitViewMode = function (){
    window.location = './'
  }

  function performGenerateDiagram(){
    jQuery.ajax({
      url: generateSubmitButton.getAttribute("data-url"),
      type: 'POST',
      data: {"text": textForGenerate.value},
      dataType: "json",
      cache: false,
      success: function(data){
        loadAnimation.style.display = "none";
        if(data.error){
          alert('Произошла ошибка.');
        }
        else {
          setCurrentText(data.code);
          setNewImage(data.image_url);
        }
      }
    });
  }

  // Adapted from http://meyerweb.com/eric/tools/dencoder/
  function urlEncode(unencoded) {
    return encodeURIComponent(unencoded).replace(/'/g,'%27').replace(/"/g,'%22')
  }

  function getImageUrl(){
    //TODO: send code to server and get answer

    return "http://s.plantuml.com/imgp/16a-class-diagram-011.png"
  }

  function generateDiagramAndLoadImage(){
    jQuery.ajax();
  }

  function urlDecode(encoded) {
    return decodeURIComponent(encoded.replace(/\+/g, ' '))
  }

  function setShareableLink(str){
    var base = '#view/'
    linkLink.href = base + urlEncode(str)
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