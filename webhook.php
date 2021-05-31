<html>

<head>
    <title>Receive Trades</title>

</head>

<body>
    <h1>Receive Webhooks</h1>

    <div id="webhook"></div>

    <?php 
    $json = file_get_contents('php://input');
    $data =  json_decode('$json');
    echo $data;
    ?>

</body>
</html>

 