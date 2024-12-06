import unittest
import requests

class TestBackendEndpoints(unittest.TestCase):

    BASE_URL = "http://localhost:5000"  # Modify this as necessary

    def test_start_thread_and_send_message(self):
        # Step 1: Ping /start_thread to get thread_id
        start_thread_url = f"{self.BASE_URL}/start_thread"
        start_response = requests.post(start_thread_url)
        self.assertEqual(start_response.status_code, 200)
        
        # Parse the thread_id from the JSON response
        thread_data = start_response.json()
        self.assertIn('thread_id', thread_data)
        thread_id = thread_data['thread_id']

        # Step 2: Ping /send_message with the appropriate data
        send_message_url = f"{self.BASE_URL}/send_message"
        message_data = {
            'thread_id': thread_id,
            'message': 'Hello, this is a test message!'
        }

        # Instead of parsing as JSON, read the raw stream text
        with requests.post(send_message_url, json=message_data, stream=True) as send_response:
            self.assertEqual(send_response.status_code, 200)

            # Iterate over the stream content (line by line)
            for line in send_response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"Streamed chunk: {decoded_line}")

                    # You can add assertions here based on expected output
                    # Example: check if the data contains expected text
                    self.assertTrue("data:" in decoded_line or "event: end" in decoded_line)

if __name__ == '__main__':
    unittest.main()

