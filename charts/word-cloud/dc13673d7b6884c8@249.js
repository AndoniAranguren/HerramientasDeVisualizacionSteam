import define1 from "./7a9e12f9fb3d8e06@517.js";

function _2(WordCloud,words,width,invalidation){return(
WordCloud(words, {
  width,
  height: 500,
  invalidation // a promise to stop the simulation when the cell is re-run
})
)}

async function _source(Inputs,FileAttachment,width){return(
Inputs.textarea({
  value: (await FileAttachment("descriptions.txt").text()).trim(),
  rows: 20,
  width
})
)}

function _WordCloud(d3,d3Cloud){return(
function WordCloud(text, {
  size = group => group.length, // Given a grouping of words, returns the size factor for that word
  word = d => d, // Given an item of the data array, returns the word
  marginTop = 0, // top margin, in pixels
  marginRight = 0, // right margin, in pixels
  marginBottom = 0, // bottom margin, in pixels
  marginLeft = 0, // left margin, in pixels
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  maxWords = 250, // maximum number of words to extract from the text
  fontFamily = "sans-serif", // font family
  fontScale = 15, // base font size
  fill = null, // text color, can be a constant or a function of the word
  padding = 0, // amount of padding between the words (in pixels)
  rotate = 0, // a constant or function to rotate the words
  invalidation // when this promise resolves, stop the simulation
} = {}) {
  const words = typeof text === "string" ? text.split(/\W+/g) : Array.from(text);
  
  const data = d3.rollups(words, size, w => w)
    .sort(([, a], [, b]) => d3.descending(a, b))
    .slice(0, maxWords)
    .map(([key, size]) => ({text: word(key), size}));
  
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .attr("width", width)
      .attr("font-family", fontFamily)
      .attr("text-anchor", "middle")
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const g = svg.append("g").attr("transform", `translate(${marginLeft},${marginTop})`);

  const cloud = d3Cloud()
      .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
      .words(data)
      .padding(padding)
      .rotate(rotate)
      .font(fontFamily)
      .fontSize(d => Math.sqrt(d.size) * fontScale)
      .on("word", ({size, x, y, rotate, text}) => {
        g.append("text")
            .datum(text)
            .attr("font-size", size)
            .attr("fill", fill)
            .attr("transform", `translate(${x},${y}) rotate(${rotate})`)
            .text(text);
      });

  cloud.start();
  invalidation && invalidation.then(() => cloud.stop());
  return svg.node();
}
)}

function _words(source,stopwords){return(
source.split(/[\s.]+/g)
  .map(w => w.replace(/^[“‘"\-—()\[\]{}]+/g, ""))
  .map(w => w.replace(/[;:.!?()\[\]{},"'’”\-—]+$/g, ""))
  .map(w => w.replace(/['’]s$/g, ""))
  .map(w => w.substring(0, 30))
  .map(w => w.toLowerCase())
  .filter(w => w && !stopwords.has(w))
)}

function _stopwords(){return(
new Set("i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,say,says,said,shall".split(","))
)}

function _d3Cloud(require){return(
require("d3-cloud@1")
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["descriptions.txt", {url: new URL("././../../data/descriptions.txt", import.meta.url), mimeType: "text/plain", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["WordCloud","words","width","invalidation"], _2);
  main.variable(observer("viewof source")).define("viewof source", ["Inputs","FileAttachment","width"], _source);
  main.variable(observer("source")).define("source", ["Generators", "viewof source"], (G, _) => G.input(_));
  main.variable(observer("WordCloud")).define("WordCloud", ["d3","d3Cloud"], _WordCloud);
  main.variable(observer("words")).define("words", ["source","stopwords"], _words);
  main.variable(observer("stopwords")).define("stopwords", _stopwords);
  main.variable(observer("d3Cloud")).define("d3Cloud", ["require"], _d3Cloud);
  const child1 = runtime.module(define1);
  main.import("howto", child1);
  return main;
}
