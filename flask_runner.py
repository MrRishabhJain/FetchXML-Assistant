from flask import Flask, jsonify, request
from runner import run_thread

# Initialize the Flask app
app = Flask(__name__)


# Define a route to expose the function with a query parameter
@app.route('/fetch-xml-assistant', methods=['GET'])
def get_assistant_response():
    # Get the 'input' query parameter from the request
    prompt = request.args.get('prompt', default='')
    resp = run_thread(prompt)
    response = {"response": resp}
    # Return the response as JSON
    return jsonify(response)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)