# Foreign content

foreign content is a like a Swiss Army knife for breaking parsers and sanitizers.

The HTML parser can create a DOM tree with elements of three namespaces:

- HTML namespace (http://www.w3.org/1999/xhtml)
- SVG namespace (http://www.w3.org/2000/svg)
- MathML namespace (http://www.w3.org/1998/Math/MathML)

By default, all elements are in HTML namespace; however if the parser encounter `<svg>` or `<math>` element, then it switchs to SVG and MathML namespace respectively. and both these namespace make foreign content.

In foreign content markup is parsed differently than in ordinary HTML. this can be most clearly shown on parsing of `<style>` element, In HTML namespace, `<style>` can only contain text; no descendants, and HTML entities are not decoded. the same is not true in foreign content: foreign content `<style>` can have child elements, and entities are decoded.

Consider the following markup:

```html
<style>ABC</style><svg><style><a>ABC
```

It's parsed into the following DOM tree:

```example
<html style>
  #text: "<a>ABC"
<svg svg>
  <svg style>
    <svg a>
      #text: "ABC"
```

> NOTE: all elements in DOM tree from there will contain a namespace. so `html style` means that it is a <style> element in HTML namespace.

Moving on, it may be tempting to make a certain observation. That is: if we are inside `svg` or `math` namespace, there all element will be these namespace too. but this is not true, There are certain elements in HTML spec called _MathML text integration points and HTML integration point_. and the children of these elements have HTML namespace.

```html
<math>
  <style></style>
  <mtext><style></style></mtext
></math>
```

It's parsed into the following DOM tree:

```example
<math math>
  <math style>
    <math mtext>
      <html style>
```

Note the style element in `mtext` is in HTML namespace. and this is because `mtext` is **MathML text integration points** and makes the parser switch namespaces.

MathML text integration points are:

- math mi
- math mo
- math mn
- math ms

HTML integration points are:

- math annotation-xml if it has attribute called encoding whose value is equal to either text/html or application/xhtml+xml
- svg foreignObject
- svg desc
- svg title

The HTML specification says that children of MathML text integration points are by default in HTML namespace with two exceptions: `mglyph` and `malignmark` and this only happens if they are a direct child of MathML text integration points

```html
<math>
  <mtext>
    <mglyph></mglyph>
    <a><mglyph></mglyph></a></mtext
></math>
```

into:

```example
<math math>
<math mtext>
  <math mglyph>
  <html a>
    <html mglyph>
```

Notice that `mglyph` that is a direct child of `mtext` is in MathML namespace, while the one that is child of `a` element is in HTML namespace.

## Rules of thumb for determine element's namespace

- Current element is in the namespace of its parent unless conditions from the points below are met.
- If current element is `<svg>` or `<math>` and parent is HTML namespace, then current element is in these namespace respectively.
- If parent of current element is an HTML integration point, then current element is in HTML namespace unless it's `<svg>` or `<math>`.
- If parent of current element is a MathML integration point, then current element is in HTML namespace unless it's `<svg>` `<math>` `<mglyph>` `<malignmark>`
- If current element is one of `<b>` `<big>` `<blockquote>` `<body>` `<br>` `<center>` `<code>` `<dd>` `<div>` `<dl>` `<dt>` `<em>` `<embed>` `<h1> - <h6>` `<head>` `<hr>` `<i>`, `<img>`, `<li>`, `<listing>`, `<menu>`, `<meta>`, `<nobr>`, `<ol>`, `<p>`, `<pre>`, `<ruby>`, `<s>`, `<small>`, `<span>`, `<strong>`, `<strike>`, `<sub>`, `<sup>`, `<table>`, `<tt>`, `<u>`, `<ul>`, `<var>` or `<font>` with color, face or size attributes defined, then all element on the stack are closed until a MathML text integration point, HTML integration point or element in HTML namespace is seen. then, the current element is also in HTML namespace.

```html
<form><math><mtext></form><form><malignmark><style></math><img src onerror=alert(1)>
```

keypoint is parse this DOM will exist nest `<form>` cause `<malignmark>` is not the direct child of the MathML integration point, so that children of `<mtext>` will in HTML namespace, so `<img ...` will be text of `<style>`. But, when this DOM tree serializing to `innerHTML` the nest `<form>` will not create (cause form cannot nested), so `<malignmark>` will be direct child of `<mtext>` and its in Math namespace include all children of it. _Now, the magic happens here, the `<style>` in math namespace is foreign content which can have child element_.
