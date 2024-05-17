# streaming_response_handler.py
class StreamingResponseHandler:
    def get_streaming_response(self, response_stream):
        streaming_response = ""
        for response in response_stream:
            streaming_response += response.delta
            yield streaming_response