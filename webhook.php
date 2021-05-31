<html>

<head>
    <title>Receive Trades</title>

</head>

<body>
    <h1>Receive Webhooks</h1>

    <div id="$data"></div>
    <?php
    
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // fetch RAW input
    $json = file_get_contents('php://input');

    // decode json
    $object = json_decode($json);

    // expecting valid json
    if (json_last_error() !== JSON_ERROR_NONE) {
        die(header('HTTP/1.0 415 Unsupported Media Type'));
    }

    /**
     * Do something with object, structure will be like:
     * $object->accountId
     * $object->details->items[0]['contactName']
     */
    // dump to file so you can see
    file_put_contents('callback.test.txt', print_r($object, true));
    }
    ?>


</body>
</html>

 