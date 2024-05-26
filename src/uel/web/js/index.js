async function showTextNode(node, duration = 2.5) {
  const dom = node.hide();
  const raw = dom.html().trim();
  await Promise.resolve();
  dom.html("").fadeIn(500);
  const doms = Array.from(raw).map((v) =>
    `<span>${v}<span>`).map($).map((v) => v
    .hide()).map((v) => v.appendTo(dom));
  const promises = [];
  let idx = 0;
  for (const $elemnt of doms) {
    const timeout = duration / raw.length;
    promises.push(new Promise(
      (resolve, reject) =>
      {
        setTimeout(() => {
          $elemnt.fadeIn(725);
          resolve();
        }, timeout * 1000);
      }
    ));
    if (promises.length > 2) {
      await Promise.all(promises);
      promises.length = 0;
    }
    idx ++;
  }
  await Promise.all(promises);
  return node; // 方便链式调用
}
async function showInitialHeaderAnimations() {
  await showTextNode($(".header-text"));
}
async function showHtmlTextNode(node, duration) {
  const html = node.html();
  await showTextNode(node, duration);
  node.html(html);
  return node
}
async function showInitialBodyAnimations() {
  showHtmlTextNode($(".text"), 1.5)
}
$(function() {
  (async () => {

    $(".container,header,footer").css("display", "block")
    showInitialHeaderAnimations();
    showInitialBodyAnimations();
  })()
});