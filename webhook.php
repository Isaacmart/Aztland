<html>

<head>
    <title>Receive Trades</title>

</head>

<body>
    <h1>Receive Webhooks</h1>

    <div id="webhook"></div>

    <?php 
    
    $new_json = file_get_contents('php://input');
    $data =  json_decode('$new_json');
    echo $data;

    ?>

</body>
</html>

 