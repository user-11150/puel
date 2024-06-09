async function show(element, duration) {
  const dom = element[0]
  dom.style.transform = "scale(3,3) translate(0px, 120px)"
  await gsap.to(dom, {
    transform: "scale(0.8,0.8)", duration: duration * (2/3)
  })
  await gsap.to(dom, {
    transform: "", duration: duration * (1/3)
  })
}
$(function() {
  const body = $(document.body);


  show(body, 1);
});