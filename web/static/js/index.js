
$(function() {
  curser()
});

function curser(){
  const $curser = $("<img>")
                   .css("position", "absolute")
                   .css("width", "32px")
                   .css("border-radius", "50%")
                   .css("display", "none")
                   .attr("src", '/imgs/curser.jpg')
                   .appendTo(document.body)
  
  const curser = $curser[0]
  
  document.ontouchmove = function(e){
    $curser.css("display", "block")
    $curser.css("top", e.pageY - curser.clientHeight / 2)
    $curser.css("left", e.pageX - curser.clientWidth / 2)
  }

  document.onmousemove = document.ontouchmove
}
