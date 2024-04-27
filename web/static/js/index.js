
$(function() {
  curser()
});

function curser(){
  const $curser = $("<img>")
                   .css("position", "absolute")
                   .css("top", "-200px")
                   .css("left", "-200px")
                   .css("width", "32px")
                   .css("border-radius", "50%")
                   .attr("src", '/imgs/curser.jpg')
                   .appendTo(document.body)
  
  const curser = $curser[0]
  
  document.onmousemove = function(e){
    $curser.css("top", e.pageY - curser.clientHeight / 2)
    $curser.css("left", e.pageX - curser.clientWidth / 2)
  }

  document.ontouchmove = function(e){
    for(const touch of e.touches){
      this.onmousemove(touch)
    }
}
}
