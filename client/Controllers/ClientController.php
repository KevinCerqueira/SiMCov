<?php

class ClientController
{
    public $host = '127.0.0.1';
    public $port = [50000, 60000];
    public $count_bytes = 8192;
    public $socket;
    private $token;

    public function __construct()
    {
        if (isset($_SESSION['auth']))
            $this->token = $_SESSION['auth'];
    }

    private function connect(bool $udp = false)
    {

        $this->socket = socket_create(AF_INET, $udp ? SOCK_DGRAM : SOCK_STREAM, $udp ? SOL_UDP : SOL_TCP);

        socket_connect($this->socket, $this->host, $this->port[$udp ? 1 : 0]);
    }

    private function close()
    {
        return socket_close($this->socket);
    }

    public function send(bool $udp, string $method, string $url, array $data = null)
    {
        $request = $method . " " . $url . " HTTP/1.1\r\nHost: " . $this->host . $this->port[$udp ? 1 : 0] . "\r\nUser-Agent: ClientController\r\nContent-Type: application/json\r\n";
        if (!empty($this->token))
            $request .= "Authorization: Bearer " . $this->token;
        $request .= "\r\nAccept: */*\r\nContent-Length: " . strlen($request) . "\r\n\r\n";
        if (!empty($data))
            $request .= strval(json_encode($data));


        $response = socket_write($this->socket, $request, strlen($request));
        if (!$udp)
            socket_recv($this->socket, $response, $this->count_bytes, MSG_WAITALL);
        $this->close();
        return json_decode($response);
    }
    public function login($username, $password)
    {
        $this->connect();
        $response = $this->send(false, 'POST', '/login', ['username' => $username, 'password' => $password]);
        if ($response->success) {
            $this->token = $response->data->token;
            $_SESSION["auth"] = $this->token;
            return $response;
        }
        return $response;
    }

    public function logout()
    {
        unset($_SESSION["auth"]);
        $this->token = null;
        return true;
    }

    public function updateAttribute(int $id_patient, string $att, $value)
    {
        $this->connect($udp = true);
        return $this->send(true, 'PATCH', "/update" . '/' . $att, ['id' => $id_patient, 'value' => $value]);
    }

    public function getListPriority()
    {
        $this->connect();
        return $this->send(false, 'GET', "/get/list/priority");
    }

    public function registerPatient($nome, $idade, $sexo)
    {
        $this->connect();
        return $this->send(false, 'POST', '/register/patient', ['nome' => $nome, 'idade' => $idade, 'sexo' => $sexo]);
    }
}
