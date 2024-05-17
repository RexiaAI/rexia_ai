# streaming_response_handler.py
class StreamingResponseHandler:
    """Handler for streaming responses."""

    def get_streaming_response(self, response_stream: iter):
        """
        Get a streaming response from the given response stream.

        Parameters:
        response_stream (iter): The response stream to get the response from.

        Returns:
        streaming_response (str): The streaming response.
        """
        streaming_response = ""
        for response in response_stream:
            streaming_response += response.delta
            yield streaming_response# streaming_response_handler.py
