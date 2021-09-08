<?php
class ClientController
{
    public $host = '127.0.0.1';
    public $port = 50000;
    public $count_bytes = 8192;
    public $socket;
    private $token;

    public function __construct()
    {
        if (isset($_SESSION['auth']))
            $this->token = $_SESSION['auth'];
    }

    public function connect()
    {
        // if (!empty($this->socket)) {
            $this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
            if (socket_connect($this->socket, $this->host, $this->port)) {
                echo "Conectado em: " . $this->port . "\n";
            }
        // }
    }

    public function login($username, $password)
    {
        $response = $this->send('POST', '/login', ['username' => $username, 'password' => $password]);
        if ($response->success) {
            $this->token = $response->data->token;
            session_start();
            $_SESSION["auth"] = $this->token;
            return true;
        }
        return $response->error;
    }

    public function logout()
    {
        unset($_SESSION["newsession"]);
        $this->token = null;
        return true;
    }

    public function send($method, $url, $data = null)
    {
        $request = $method . " " . $url . " HTTP/1.1\r\nHost: " . $this->host . "\r\nUser-Agent: ClientController\r\nContent-Type: application/json\r\n";
        if (!empty($this->token))
            $request .= "Authorization: Bearer " . $this->token;
        $request .= "\r\nAccept: */*\r\nContent-Length: " . strlen($request) . "\r\n\r\n";
        if (!empty($data))
            $request .= strval(json_encode($data));

        socket_write($this->socket, $request, strlen($request));
        socket_recv($this->socket, $response, $this->count_bytes, MSG_WAITALL);
        return json_decode($response);
    }

    public function close()
    {
        return socket_close($this->socket);
    }
}
