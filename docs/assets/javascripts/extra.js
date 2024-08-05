(async function(){
  const readtime = document.querySelector(".readtime")
  
  const request = await fetch(location.href)

  readtime.innerHTML += `${(await request.text()).length} chars`
})()
