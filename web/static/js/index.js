
$(function() {
  setTimeout(
    () => {
      // 每秒钟自动刷新一次，以便于调试
      location.reload()
    },
    1
  )
  $("*").each(function(){
    $(this).css(
      "text-shadow",
      `1px 1px 1px ${$(val).css("color") || "#121212"}`
    )
  })
});