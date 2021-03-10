import socket
import time


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):

        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.connection = socket.create_connection((self.host, self.port), self.timeout)
        except socket.error as err:
            print("Connection error: ", err)
            raise ClientError(err)

    def _send(self, request):

        request = request.encode("utf-8")

        try:
            self.connection.sendall(request)
        except socket.error as err:
            print("Send data error: ", err)
            raise ClientError(err)

    def _read(self):

        answer = b""

        while not answer.endswith(b"\n\n"):
            try:
                answer += self.connection.recv(1024)
            except socket.error as err:
                print("Read data error: ", err)
                raise ClientError(err)

        return answer.decode("utf-8")

    def put(self, key, value, timestamp=None):

        timestamp = timestamp or int(time.time())
        request = "put {} {} {}\n".format(key, value, timestamp)
        self._send(request)
        answer = self._read()

        if answer == "ok\n\n":
            return None
        else:
            raise ClientError("Server returned an error")

    def get(self, key):

        request = "get {}\n".format(key)
        self._send(request)
        status, data = self._read().split("\n", 1)
        data = data.strip()
        metrics_dict = {}

        if status != "ok":
            raise ClientError("Server returned an error")

        if data == '':
            return metrics_dict

        try:
            for metric in data.split("\n"):
                key, val, timestamp = metric.split()
                if key not in metrics_dict:
                    metrics_dict[key] = [(int(timestamp), float(val))]
                else:
                    metrics_dict[key].append((int(timestamp), float(val)))
        except Exception as err:
            print("Server returned invalid data")
            raise ClientError(err)

        for key in metrics_dict.keys():
            val = metrics_dict[key]
            val.sort(key=lambda i: i[0])
            metrics_dict[key] = val

        return metrics_dict
